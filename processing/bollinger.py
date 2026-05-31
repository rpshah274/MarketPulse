from collections import deque
import statistics

class BollingerBandsCalculator:
    def __init__(self, symbol: str, period: int = 20, num_std: float = 2.0):
        self.symbol = symbol
        self.period = period
        self.num_std = num_std
        self.window = deque(maxlen=period)

    def update(self, price: float) -> dict | None:
        # 1. append price to window
        # 2. if window not full return None
        # 3. calculate middle = sum(window) / period
        # 4. calculate std = statistics.stdev(window)
        # 5. upper = middle + num_std * std
        # 6. lower = middle - num_std * std
        # 7. return dict with upper, middle, lower
        self.window.append(price)
        if len(self.window) < self.period:
            return None
        middle = sum(self.window) / self.period
        std = statistics.stdev(self.window)
        upper = middle + self.num_std * std
        lower = middle - self.num_std * std
        return {
            "upper": round(upper, 2),
            "middle": round(middle, 2),
            "lower": round(lower, 2)
        }
if __name__ == "__main__":
    bb_calculator = BollingerBandsCalculator("AAPL", period=5, num_std=2)
    prices = [150, 152, 151, 153, 155, 154, 156]
    for price in prices:
        result = bb_calculator.update(price)
        print(f"Price: {price}, Bollinger Bands: {result}")