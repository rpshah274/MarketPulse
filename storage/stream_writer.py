import sys
sys.path.append("D:/MarketPulse")

import redis
from ingestion.models import Trade

class RedisStreamWriter:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def write_trade(self, trade: Trade):
        stream_name = f"trades:{trade.symbol}"
        # XADD adds an entry to the stream
        self.client.xadd(
            stream_name,
            {
                'symbol': trade.symbol,
                'price': str(trade.price),
                'size': str(trade.size),
                'exchange': trade.exchange,
                'timestamp': trade.timestamp
            }
        )
if __name__ == "__main__":
    from ingestion.models import Trade
    writer = RedisStreamWriter()
    trade = Trade(symbol='FAKEPACA', price=134.56, size=3, exchange='N', timestamp='2026-05-27T21:09:17Z')
    writer.write_trade(trade)
    print("Trade written to Redis Stream")