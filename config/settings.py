from dotenv import load_dotenv
from pathlib import Path
import os

# load the .env file
load_dotenv(Path(__file__).parent / ".env" )

# read from environment
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# WebSocket URL
WS_URL = WS_URL = "wss://stream.data.alpaca.markets/v2/test" #"wss://stream.data.alpaca.markets/v2/iex" #
