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
    def get_latest(self, indicator: str , symbol: str)-> float | None:
        key = f"ts:{indicator}:{symbol}"
        # use self.client.execute_command to call TS.GET : key
        try:
            result = self.client.execute_command("TS.GET", key)
            if result:
                return result[1]
            return None
        except Exception:
            return None
        # result = self.client.execute_command("TS.GET", key)
        # if result is None:
        #     return None
        # return result[1]
    def write_bar(self, bar):
        symbol = bar.symbol
        ts = int(time.time() * 1000)
        self.client.execute_command("TS.ADD", f"ts:bar:open:{symbol}", ts, bar.open)
        self.client.execute_command("TS.ADD", f"ts:bar:high:{symbol}", ts, bar.high)
        self.client.execute_command("TS.ADD", f"ts:bar:low:{symbol}", ts, bar.low)
        self.client.execute_command("TS.ADD", f"ts:bar:close:{symbol}", ts, bar.close)
        self.client.execute_command("TS.ADD", f"ts:bar:volume:{symbol}", ts, bar.volume)
if __name__ == "__main__":
    import sys
    sys.path.append("D:/MarketPulse")
    writer = RedisTimeSeriesWriter()
    writer.write("vwap", "AAPL", 150.67)
    print("VWAP written to Redis TimeSeries")