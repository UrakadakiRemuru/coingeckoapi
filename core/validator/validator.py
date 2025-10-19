from abc import ABC, abstractmethod
from typing import Any


class AbstractValidator(ABC):
    def __init__(self, obj: Any, many: bool = False):
        self.obj = obj
        self.many = many

    @abstractmethod
    def validate(self) -> Any:
        '''Валидирует данные.'''