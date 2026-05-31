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

@dataclass
class Bar:
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    vwap: float
    timestamp: str

    @classmethod
    def from_raw(cls, raw: dict) -> "Bar":
        return cls(
            symbol=raw.get('S'),
            open=raw.get('o'),
            high=raw.get('h'),
            low=raw.get('l'),
            close=raw.get('c'),
            volume=raw.get('v'),
            vwap=raw.get('vw'),
            timestamp=raw.get('t')
        )