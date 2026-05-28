from dataclasses import dataclass

@dataclass
class Trade:
    symbol: str
    price: float
    size: int
    exchange: str
    timestamp: str

    @classmethod
    def from_raw(cls, raw: dict) -> "Trade":
        # map raw Alpaca keys to Trade fields
        return cls(
            symbol=raw.get('S'),
            price=raw.get('p'),
            size=raw.get('s'),
            exchange=raw.get('x'),
            timestamp=raw.get('t')
        )