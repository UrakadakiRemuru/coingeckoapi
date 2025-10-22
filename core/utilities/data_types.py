from datetime import date
from typing import TypedDict


class CoinData(TypedDict):
    name: str
    total_volume: int
    networks: list[str]
    exchanges: list[str]
    genesis_date: str

class RenderedCoinData(TypedDict):
    name: str
    total_volume: int
    binance: bool
    bybit: bool
    kucoin: bool
    networks: list[str]
    exchanges: list[str]
    genesis_date: str