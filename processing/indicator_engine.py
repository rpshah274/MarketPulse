import sys
sys.path.append("D:/MarketPulse")

from processing.vwap import VWAPCalculator
from processing.sma import SMACalculator
from processing.ema import EMACalculator
from processing.rsi import RSICalculator
from processing.macd import MACDCalculator
from processing.bollinger import BollingerBandsCalculator
from storage.timeseries_writer import RedisTimeSeriesWriter
from ingestion.models import Trade

class IndicatorEngine:
    def __init__(self, symbols: list[str]):
        self.ts_writer = RedisTimeSeriesWriter()
        self.vwap_calculators = {}
        self.sma_calculators = {}
        self.ema_calculators = {}
        self.rsi_calculators = {}
        self.macd_calculators = {}
        self.bollinger_calculators = {}
        for symbol in symbols:
            self.vwap_calculators[symbol] = VWAPCalculator(symbol)
            self.sma_calculators[symbol] = SMACalculator(symbol, period=20)
            self.ema_calculators[symbol] = EMACalculator(symbol, period=20)
            self.rsi_calculators[symbol] = RSICalculator(symbol, period=14)
            self.macd_calculators[symbol] = MACDCalculator(symbol)
            self.bollinger_calculators[symbol] = BollingerBandsCalculator(symbol, period=20)
    def process(self, trade: Trade):
        # 1. get the VWAPCalculator for trade.symbol
        # 2. call update() with trade.price and trade.size
        # 3. write the result to Redis TimeSeries
        vwap_calculator = self.vwap_calculators.get(trade.symbol)
        if vwap_calculator:
            vwap = vwap_calculator.update(trade.price, trade.size)
            self.ts_writer.write("vwap", trade.symbol, vwap)
        sma_calculator = self.sma_calculators.get(trade.symbol)
        if sma_calculator:
            sma = sma_calculator.update(trade.price)
            if sma is not None:
                self.ts_writer.write("sma20", trade.symbol, sma)
        ema_calculator = self.ema_calculators.get(trade.symbol)
        if ema_calculator:
            ema = ema_calculator.update(trade.price)
            if ema is not None:
                self.ts_writer.write("ema20", trade.symbol, ema)
        rsi_calculator = self.rsi_calculators.get(trade.symbol)
        if rsi_calculator:
            rsi = rsi_calculator.update(trade.price)
            if rsi is not None:
                self.ts_writer.write("rsi", trade.symbol, rsi)
        macd_calculator = self.macd_calculators.get(trade.symbol)
        if macd_calculator:
            macd = macd_calculator.update(trade.price)
            if macd is not None:
                self.ts_writer.write("macd", trade.symbol, macd['macd'])
                self.ts_writer.write("macd_signal", trade.symbol, macd['signal'])
                self.ts_writer.write("macd_histogram", trade.symbol, macd['histogram'])
        bollinger_calculator = self.bollinger_calculators.get(trade.symbol)
        if bollinger_calculator:
            bb = bollinger_calculator.update(trade.price)
            if bb is not None:
                self.ts_writer.write("bb_upper", trade.symbol, bb['upper'])
                self.ts_writer.write("bb_middle", trade.symbol, bb['middle'])
                self.ts_writer.write("bb_lower", trade.symbol, bb['lower'])
if __name__ == "__main__":
    engine = IndicatorEngine(["AAPL", "TSLA"])
    trade = Trade(symbol="AAPL", price=150.0, size=100, exchange="N", timestamp="2026-05-28T09:30:00Z")
    engine.process(trade)
    print("Indicator processed")