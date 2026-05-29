from collections import deque

class SMACalculator:
    def __init__(self, symbol: str, period: int):
        self.symbol = symbol
        self.period = period
        self.window = deque(maxlen=period)
        self.current_sma = None

    def update(self, price: float) -> float | None:
        # 1. append price to window
        # 2. if window is full (len == period), calculate average
        # 3. store in self.current_sma and return it
        # 4. if not full yet, return None
        self.window.append(price)
        if len(self.window)==self.period:
            self.current_sma = round(sum(self.window)/len(self.window),4)
        return self.current_sma
if __name__ == "__main__":
    sma = SMACalculator("AAPL", 3)
    print(sma.update(100))  
    print(sma.update(101))  
    print(sma.update(102))  
    print(sma.update(103))  