from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent / ".env", override=True)

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

USE_TEST_STREAM = os.getenv("USE_TEST_STREAM", "true").lower() == "true"

if USE_TEST_STREAM:
    WS_URL = "wss://stream.data.alpaca.markets/v2/test"
    SYMBOLS = ["FAKEPACA"]
else:
    WS_URL = "wss://stream.data.alpaca.markets/v2/iex"
    SYMBOLS = [
        "AAPL", "TSLA", "MSFT", "GOOGL", "AMZN",
        "NVDA", "META", "NFLX", "AMD", "INTC",
        "BABA", "JPM", "BAC", "WMT", "DIS",
        "UBER", "LYFT", "SPOT", "COIN", "PLTR"
    ]