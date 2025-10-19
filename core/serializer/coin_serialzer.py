import json

from core.serializer import AbstractSerializer
from core.utilities.data_types import RenderedCoinData


class CoinSerializer(AbstractSerializer):
    def __init__(self, obj: list[RenderedCoinData]):
        super().__init__(obj)

    def serialize(self) -> str:
        return json.dumps(self.obj)
