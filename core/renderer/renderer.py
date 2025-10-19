from abc import abstractmethod, ABC
from typing import Any


class AbstractRenderer(ABC):

    def __init__(self, obj: Any):
        self.obj = obj

    @abstractmethod
    def render(self) -> Any:
        '''Преобразует данные к формату, готовому к сериализации.'''
