from abc import ABC, abstractmethod

from aiohttp import ClientSession, ClientTimeout, ClientResponseError


class AbstractProvider(ABC):
    BASE_URL: str = None
    HEADERS: dict = None

    def __init__(self):
        if self.BASE_URL is None:
            raise NotImplementedError
        if self.HEADERS is None:
            self.HEADERS = {}

    async def __aenter__(self):
        self.session = ClientSession(base_url=self.BASE_URL, headers=self.HEADERS, timeout=ClientTimeout(total=5))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    @abstractmethod
    async def get_data(self) -> object:
        '''Предоставляет данные, полученные от API для дальнейшей записи в файл.'''

    @abstractmethod
    def handle_exception(self, exception: ClientResponseError):
        '''Обрабатывает исключение ClientResponseError.'''
