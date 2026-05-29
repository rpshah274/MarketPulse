class VWAPCalculator:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.cumulative_pv = 0.0
        self.cumulative_volume = 0
        self.current_vwap = 0.0

    def update(self, price: float, size: int) -> float:
        # 1. add price*size to cumulative_pv
        # 2. add size to cumulative_volume
        # 3. calculate new vwap
        # 4. store in self.current_vwap
        # 5. return it
        self.cumulative_pv += price * size
        self.cumulative_volume += size
        self.current_vwap = round(self.cumulative_pv / self.cumulative_volume,4)
        return self.current_vwap

    def reset(self):
        # reset all state to zero called at market open each day
        self.cumulative_pv = 0.0
        self.cumulative_volume = 0
        self.current_vwap = 0.0
        
if __name__ == "__main__":
    vwap_calculator = VWAPCalculator("AAPL")
    print(vwap_calculator.update(150.0, 100))  # First trade
    print(vwap_calculator.update(151.0, 200))  # Second trade
    print(vwap_calculator.update(149.5, 50))   # Third trade
    vwap_calculator.reset()  # Reset at market open