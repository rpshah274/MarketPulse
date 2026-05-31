import sys
sys.path.append("D:/MarketPulse")

from storage.database import SessionLocal
from storage.models import TradeRecord
from ingestion.models import Trade

class DBWriter:
    def write_trade(self, trade: Trade):
        db = SessionLocal()
        try:
            # create a TradeRecord object from the Trade dataclass
            record = TradeRecord(
                symbol=trade.symbol,
                price=trade.price,
                size=trade.size,
                exchange=trade.exchange,
                timestamp=trade.timestamp
            )
            db.add(record)
            db.commit()
        finally:
            db.close()

if __name__ == "__main__":
    writer = DBWriter()
    trade = Trade(symbol="FAKEPACA", price=134.56, size=3, exchange="N", timestamp="2026-05-29T00:00:00Z")
    writer.write_trade(trade)
    print("Trade written to PostgreSQL")