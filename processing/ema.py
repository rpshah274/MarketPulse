class EMACalculator:
    def __init__(self, symbol: str, period: int):
        self.symbol = symbol
        self.period = period
        self.multiplier = 2 / (period + 1)
        self.current_ema = None

    def update(self, price: float) -> float | None:
        # if first value, seed EMA with that price
        # otherwise: EMA = price * multiplier + previous_ema * (1 - multiplier)
        # round to 4 decimal places
        # return current_ema
        if self.current_ema is None:
            self.current_ema = price
        else:
            self.current_ema =round(price * self.multiplier + self.current_ema * (1 - self.multiplier),4)
        return self.current_ema
        
if __name__ == "__main__":
    ema = EMACalculator("AAPL", 3)
    print(ema.update(100))  
    print(ema.update(101))  
    print(ema.update(102))  
    print(ema.update(103))