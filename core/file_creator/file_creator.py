import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent
class FileCreator(ABC):
    FILE_DIR = BASE_DIR / "media"

    def __init__(self, obj: Any):
        self.obj = obj
        os.makedirs(self.FILE_DIR, exist_ok=True)

    @abstractmethod
    def create_file(self):
        '''Создает файл и записывает его в FILE_DIR.'''