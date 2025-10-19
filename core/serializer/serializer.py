from abc import ABC, abstractmethod
import json
from typing import Any



class AbstractSerializer(ABC):

    def __init__(self, obj: Any):
        if obj is None:
            raise TypeError('obj cannot be None')

        self.obj = obj

    @abstractmethod
    def serialize(self) -> object:
        '''Сериализует данные.'''
