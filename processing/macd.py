import sys
sys.path.append("D:/MarketPulse")

from processing.ema import EMACalculator
class MACDCalculator:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ema_12 = EMACalculator(symbol, period=12)
        self.ema_26 = EMACalculator(symbol, period=26)
        self.signal_ema = EMACalculator(symbol, period=9)
        self.current_macd = None
        self.current_signal = None
        self.current_histogram = None

    def update(self, price: float) -> dict | None:
        ema_12_value = self.ema_12.update(price)
        ema_26_value = self.ema_26.update(price)
        if ema_12_value is not None and ema_26_value is not None:
            self.current_macd = round(ema_12_value - ema_26_value, 4)
            signal_value = self.signal_ema.update(self.current_macd)
            # calculate histogram if signal_value is not None
            if signal_value is not None:
                self.current_signal = signal_value
                self.current_histogram = round(self.current_macd - self.current_signal, 4)
                return {
                    "macd": self.current_macd,
                    "signal": self.current_signal,
                    "histogram": self.current_histogram
                }

if __name__ == "__main__":
    macd_calculator = MACDCalculator("AAPL")
    prices = [150, 152, 151, 153, 155, 154, 156, 158, 157, 159, 
          160, 161, 162, 163, 165, 164, 166, 168, 167, 169,
          170, 171, 172, 170, 168, 167, 169, 171, 173, 175,
          174, 176, 178, 177, 179]
    for price in prices:
        result = macd_calculator.update(price)
        print(f"Price: {price}, MACD Result: {result}")