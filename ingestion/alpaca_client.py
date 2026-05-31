import sys
import time
sys.path.append("D:/MarketPulse")

from storage.timeseries_writer import RedisTimeSeriesWriter 
from storage.stream_writer import RedisStreamWriter
from storage.db_writer import DBWriter
from processing.indicator_engine import IndicatorEngine
from ingestion.models import Trade
from monitoring.metrics import trades_processed, processing_latency, websocket_connected
from websockets.asyncio.client import connect
from prometheus_client import start_http_server
import json
from config.settings import ALPACA_API_KEY, ALPACA_SECRET_KEY, WS_URL, SYMBOLS

class AlpacaClient:
    def __init__(self, api_key: str, secret_key: str, symbols: list[str]):
        self.api_key = api_key
        self.secret_key = secret_key
        self.ws_url = WS_URL
        self.symbols = symbols

    async def connect(self):
        self.connection = await connect(self.ws_url)
        websocket_connected.set(1)
        # server sends a welcome message upon connection
        welcome = await self.connection.recv() 
        print(welcome)
        await self.authenticate()

    async def authenticate(self):
        auth_message = {
            "action": "auth",
            "key": self.api_key,
            "secret": self.secret_key
        }
        await self.connection.send(json.dumps(auth_message))
        # read the response to authentication
        response = await self.connection.recv()
        print(response) 

    async def subscribe(self):
        subscribe_message = {
            "action": "subscribe",
            "trades": self.symbols,
            "bars": self.symbols
        }
        await self.connection.send(json.dumps(subscribe_message))
        response = await self.connection.recv()
        print(response)

    async def receive(self,writer,engine,db_writer,ts_writer):
        while True:
            message = await self.connection.recv()
            data = json.loads(message)
            for item in data:
                if item['T'] == 't':  # trade message
                    start = time.time()
                    trade = Trade.from_raw(item)
                    writer.write_trade(trade)
                    engine.process(trade)
                    db_writer.write_trade(trade)
                    duration = time.time() - start
                    trades_processed.labels(symbol=trade.symbol).inc()
                    processing_latency.labels(symbol=trade.symbol).observe(duration)
                    print(f"Written: {trade.symbol} @ {trade.price}")
                elif item['T'] == 'b':  # bar message
                    from ingestion.models import Bar
                    bar = Bar.from_raw(item)
                    ts_writer.write_bar(bar)
                    print(f"Bar: {bar.symbol}  O:{bar.open} H:{bar.high} L:{bar.low} C:{bar.close} V:{bar.volume}")

async def main():
    start_http_server(8001)
    writer = RedisStreamWriter()
    db_writer = DBWriter()
    ts_writer = RedisTimeSeriesWriter()
    engine = IndicatorEngine(SYMBOLS)

    client = AlpacaClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, SYMBOLS)
    await client.connect()
    await client.subscribe()
    await client.receive(writer,engine,db_writer,ts_writer)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())