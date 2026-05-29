import redis
import time

class RedisTimeSeriesWriter:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def write(self, indicator: str, symbol: str, value: float, timestamp_ms: int = None):
        key = f"ts:{indicator}:{symbol}"
        ts = timestamp_ms or int(time.time() * 1000)
        # use self.client.execute_command to call TS.ADD : key, timestamp, value
        self.client.execute_command("TS.ADD", key, ts, value)
if __name__ == "__main__":
    import sys
    sys.path.append("D:/MarketPulse")
    writer = RedisTimeSeriesWriter()
    writer.write("vwap", "AAPL", 150.67)
    print("VWAP written to Redis TimeSeries")