from datetime import datetime
from copy import deepcopy

from core.renderer import AbstractRenderer
from core.utilities import CoinData
from core.utilities.data_types import RenderedCoinData


class CoinRenderer(AbstractRenderer):
    EXCHANGES = {'Binance', 'Bybit', 'KuCoin'}

    def __init__(self, obj: list[CoinData]):
        super().__init__(obj=deepcopy(obj))

    def render(self) -> list[RenderedCoinData]:
        for coin_data in self.obj:
            exchanges = coin_data['exchanges']
            for exchange in self.EXCHANGES:
                coin_data[exchange] = True if exchange in exchanges else False

        self.obj.sort(key=lambda x: (
                   -x['total_volume'],
                   datetime.strptime(x['genesis_date'], '%Y-%m-%d')
               ))

        return self.obj