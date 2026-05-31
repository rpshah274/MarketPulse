import sys
sys.path.append("D:/MarketPulse")
import time
from fastapi import FastAPI
from storage.timeseries_writer import RedisTimeSeriesWriter
from storage.database import SessionLocal
from storage import models as db_models
from sqlalchemy.orm import Session
from fastapi import Depends
from starlette.routing import Mount
from starlette.applications import Starlette

app = FastAPI(title="MarketPulse API", version="1.0.0")
from prometheus_client import make_asgi_app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

ts = RedisTimeSeriesWriter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    # return status ok and a timestamp
    return {"status": "ok", "timestamp": int(time.time() * 1000)}
@app.get("/indicators/{symbol}/sma")
def get_sma(symbol: str):
    sma = ts.get_latest("sma20", symbol)
    if sma is None:
        return {"symbol": symbol, "sma": None, "message": "No data available"}
    return {"symbol": symbol, "sma": sma}

@app.get("/indicators/{symbol}/ema")
def get_ema(symbol: str):
    ema = ts.get_latest("ema20", symbol)
    if ema is None:
        return {"symbol": symbol, "ema": None, "message": "No data available"}
    return {"symbol": symbol, "ema": ema}

@app.get("/indicators/{symbol}/macd")
def get_macd(symbol: str):
    macd = ts.get_latest("macd", symbol)
    signal = ts.get_latest("macd_signal", symbol)
    histogram = ts.get_latest("macd_histogram", symbol)
    return {"symbol": symbol, "macd": macd, "signal": signal, "histogram": histogram}

@app.get("/indicators/{symbol}/bollinger")
def get_bollinger(symbol: str):
    return {
        "symbol": symbol,
        "upper": ts.get_latest("bb_upper", symbol),
        "middle": ts.get_latest("bb_middle", symbol),
        "lower": ts.get_latest("bb_lower", symbol)
    }

@app.get("/indicators/{symbol}/vwap")
def get_vwap(symbol: str):
    # query Redis TimeSeries for ts:vwap:{symbol}
    vwap = ts.get_latest("vwap", symbol)
    if vwap is None:
        return {"symbol": symbol, "vwap": None, "message": "No data available"}
    return {"symbol": symbol, "vwap": vwap}

@app.get("/indicators/{symbol}/rsi")
def get_rsi(symbol: str):
    # same pattern as vwap
    rsi = ts.get_latest("rsi", symbol)
    if rsi is None:
        return {"symbol": symbol, "rsi": None, "message": "No data available"}
    return {"symbol": symbol, "rsi": rsi}

@app.get("/indicators/{symbol}")
def get_all_indicators(symbol: str):
    # call get_latest for each indicator
    indicators = ["vwap", "rsi", "sma20", "ema20", "macd", "bb_upper", "bb_middle", "bb_lower"]
    # return dict with all values
    result = {"symbol": symbol}
    for ind in indicators:
        value = ts.get_latest(ind, symbol)
        result[ind] = value
    # indicators: vwap, rsi, sma20, ema20, macd, bb_upper, bb_middle, bb_lower
    return result

@app.get("/symbols")
def get_symbols(db: Session = Depends(get_db)):
    # Implement logic to retrieve list of available symbols from the database
    results = db.query(db_models.TradeRecord.symbol).distinct().all()
    return {"symbols": [r[0] for r in results]}

@app.get("/trades/{symbol}")
def get_trades(symbol: str, db: Session = Depends(get_db)):
    trades = db.query(db_models.TradeRecord).filter(db_models.TradeRecord.symbol == symbol).order_by(db_models.TradeRecord.timestamp.desc()).limit(100).all()
    return {"symbol": symbol, "trades": [
    {
        "id": t.id,
        "symbol": t.symbol,
        "price": t.price,
        "size": t.size,
        "exchange": t.exchange,
        "timestamp": t.timestamp,
        "created_at": str(t.created_at)
    } for t in trades
]}

@app.get("/indicators/{symbol}/{indicator}/history")
def get_indicator_history(symbol: str, indicator: str, minutes: int = 15):
    import time
    end_ts = int(time.time() * 1000)
    start_ts = end_ts - (minutes * 60 * 1000)
    key = f"ts:{indicator}:{symbol}"
    try:
        result = ts.client.execute_command("TS.RANGE", key, start_ts, end_ts)
        return {
            "symbol": symbol,
            "indicator": indicator,
            "data": [{"timestamp": r[0], "value": r[1]} for r in result]
        }
    except Exception:
        return {"symbol": symbol, "indicator": indicator, "data": []}