import sys
sys.path.append("D:/MarketPulse")
from storage.stream_writer import RedisStreamWriter
from processing.indicator_engine import IndicatorEngine
from ingestion.models import Trade
from websockets.asyncio.client import connect
import json
from config.settings import ALPACA_API_KEY, ALPACA_SECRET_KEY, WS_URL

class AlpacaClient:
    def __init__(self, api_key: str, secret_key: str, symbols: list[str]):
        self.api_key = api_key
        self.secret_key = secret_key
        self.ws_url = WS_URL
        self.symbols = symbols

    async def connect(self):
        self.connection = await connect(self.ws_url)
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

    async def receive(self,writer,engine):
        while True:
            message = await self.connection.recv()
            data = json.loads(message)
            for item in data:
                if item['T'] == 't':  # trade message
                    if item['T'] == 't':
                        trade = Trade.from_raw(item)
                        writer.write_trade(trade)
                        engine.process(trade)
                        print(f"Written: {trade.symbol} @ {trade.price} | VWAP: {engine.vwap_calculators[trade.symbol].current_vwap:.2f}")
                # elif item['T'] == 'b':  # bar message
                #     pass

async def main():
    symbols = ["FAKEPACA"] #["AAPL", "TSLA"] 
    writer = RedisStreamWriter()
    engine = IndicatorEngine(symbols)

    client = AlpacaClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, symbols)
    await client.connect()
    await client.subscribe()
    await client.receive(writer,engine)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())