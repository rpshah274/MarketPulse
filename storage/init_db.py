import sys
sys.path.append("D:/MarketPulse")

from storage.database import engine, Base
from storage.models import TradeRecord, IndicatorSnapshot

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

if __name__ == "__main__":
    init_db()