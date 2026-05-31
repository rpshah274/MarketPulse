class RSICalculator:
    def __init__(self, symbol: str, period: int = 14):
        self.symbol = symbol
        self.period = period
        self.gains = []
        self.losses = []
        self.prev_price = None
        self.current_rsi = None

    def update(self, price: float) -> float | None:
        if not self.prev_price:
            self.prev_price = price
            return None
        change = price - self.prev_price
        if change > 0:
            self.gains.append(change)
            self.losses.append(0)
        else:
            self.gains.append(0)
            self.losses.append(abs(change))
        
        self.prev_price = price
        if len(self.gains) >= self.period:
            avg_gain = sum(self.gains[-self.period:]) / self.period
            avg_loss = sum(self.losses[-self.period:]) / self.period
            if avg_loss == 0:
                self.current_rsi = 100
            else:
                rs = avg_gain / avg_loss
                self.current_rsi = 100 - (100 / (1 + rs))
            return round(self.current_rsi, 2)

if __name__ == "__main__":
    rsi_calculator = RSICalculator("AAPL", period=14)
    prices = [150, 152, 151, 153, 155, 154, 156, 158, 157, 159, 160, 161, 162, 163, 165]
    for price in prices:
        rsi = rsi_calculator.update(price)
        print(f"Price: {price}, RSI: {rsi}")