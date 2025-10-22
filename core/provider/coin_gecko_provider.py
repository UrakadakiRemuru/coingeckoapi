import asyncio
import os
from asyncio import as_completed
from typing import Type

from aiohttp import ClientResponseError, ClientConnectionError, ServerTimeoutError
from dotenv import load_dotenv

from core.provider import AbstractProvider
from core.renderer import CoinRenderer
from core.serializer import CoinSerializer
from core.utilities import CoinData, RequestLimit, retry, ValidationError
from core.validator import CoinValidator

load_dotenv()


class CoinGeckoException(Exception):
    pass


class CoinGeckoProvider(AbstractProvider):
    BASE_URL = 'https://api.coingecko.com/api/v3/'
    HEADERS = {'x-cg-demo-api-key': os.getenv('API_KEY')}
    EXCEPTIONS_MAP = {
        403: CoinGeckoException('Запрос не может быть пропущен, нас заблокировали!'),
        429: RequestLimit('Мы делаем слишком много запросов, необходимо подождать минутку!'),
        500: CoinGeckoException('Представитель данных лишился сервера, нет возможности получить данные.'),
        503: CoinGeckoException('Представитель данных лишился сервера, нет возможности получить данные.'),
        1020: CoinGeckoException('Какие-то проблемы с брандмауэром.'),
        10005: CoinGeckoException('Отсюда мы ничего не получим, надо улучшать подписку до PRO.'),
        10002: CoinGeckoException('Забыли указать API ключ  в запросе, исправьтесь!'),
        10010: CoinGeckoException('Уровень подписки был изменен на PRO! Теперь нужен URL: pro-api.coingecko.com'),
        10011: CoinGeckoException('Базовый уровень подписки! Используйте URL: api.coingecko.com'),
    }

    _serializer = CoinSerializer
    _validator = CoinValidator
    _renderer = CoinRenderer

    @property
    def serializer(self) -> Type[CoinSerializer]:
        return self._serializer

    @property
    def validator(self) -> Type[CoinValidator]:
        return self._validator

    @property
    def renderer(self) -> Type[CoinRenderer]:
        return self._renderer

    async def get_data(self):
        coin_ids = await self._get_top_coin_ids_by_volume()
        coins_data = [self._get_coin_data_by_id(coin_id) for coin_id in coin_ids]
        result: list[CoinData] = []
        counter = 0
        for coin_data in as_completed(coins_data):
            counter += 1
            try:
                data = await coin_data
                print(f'Обрабатываем {counter} / {len(coins_data)}')
                result.append(self.validator(data).validate())
            except ValidationError as e:
                print(f'Данные о {data.get('name', 'монете')} испорчены: {str(e)}. Пропускаем...')
            print(f'Данные о {data.get('name')} успешно обработаны!')
        rendered = self.renderer(result).render()
        # return self.serializer(rendered).serialize()
        return rendered

    def handle_exception(self, exception: ClientResponseError):
        if exception.status in self.EXCEPTIONS_MAP:
            raise self.EXCEPTIONS_MAP[exception.status]
        raise exception

    @retry(attempts=3, attempt_time=60, exceptions=(RequestLimit, ClientConnectionError, ServerTimeoutError))
    async def _get_top_coin_ids_by_volume(self, amount: int = 100) -> list[str]:
        async with self.session.get('coins/markets',
                                    params=dict(vs_currency='usd', order='volume_desc', per_page=amount)) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                self.handle_exception(e)
            return [coin['id'] for coin in await response.json()]

    @retry(attempts=3, attempt_time=60, exceptions=(RequestLimit, ClientConnectionError, ServerTimeoutError))
    async def _get_coin_data_by_id(self, coin_id: str) -> CoinData:
        async with self.session.get(f'coins/{coin_id}', params=dict(
                localization='false',
                community_data='false',
                developer_data='false')
                                    ) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                self.handle_exception(e)
            res = await response.json()
            return {
                'name': res['id'],
                'networks': self._parse_platform(res['platforms']),
                'exchanges': self._parse_tickers(res['tickers']),
                'genesis_date': self._parse_genesis_date(res['genesis_date']),
                'total_volume': self._parse_total_volume(res['market_data']),
            }

    @staticmethod
    def _parse_platform(platforms: dict[str, str]) -> list[str]:
        result = []
        for platform in platforms.keys():
            result.append(platform) if platform else None
        return result

    @staticmethod
    def _parse_tickers(tickers: list[dict[str, str | dict[str, str]]]) -> list[str]:
        result = set()
        for ticker in tickers:
            if ticker.get('market') and ticker['market'].get('name'):
                result.add(ticker['market']['name'])

        return list(result)

    @staticmethod
    def _parse_genesis_date(genesis_date: str | None) -> str | None:
        return genesis_date if genesis_date else None

    @staticmethod
    def _parse_total_volume(market_data: dict[str, dict[str, int]] | None) -> int | None:
        if market_data is None:
            return None
        if market_data.get('total_volume') and market_data['total_volume'].get('usd'):
            return market_data['total_volume']['usd']
        return None


if __name__ == '__main__':
    async def main():
        async with CoinGeckoProvider() as coin_provider:
            # print(await coin_provider._get_top_coin_ids_by_volume())
            # ['tether', 'bitcoin', 'ethereum', 'usd-coin', 'solana', 'first-digital-usd', 'ripple', 'binance-bridged-usdt-bnb-smart-chain', 'binancecoin', 'dogecoin', 'wbnb', 'cardano', 'wrapped-solana', 'aster-2', 'standx-dusd', 'chainlink', 'sui', 'tron', 'l2-standard-bridged-weth-base', 'litecoin', 'zerobase', 'ethena', 'zcash', 'binance-bridged-usdc-bnb-smart-chain', 'avalanche-2', 'bnb48-club-token', 'coinbase-wrapped-btc', 'ark-of-panda', 'wrapped-bitcoin', 'ethena-usde', 'tether-gold', 'hyperliquid', 'arbitrum-bridged-weth-arbitrum-one', 'quq', 'pepe', 'pax-gold', 'bittensor', 'aave', 'aptos', 'plasma', 'usdt0', 'bitcoin-cash', 'usd1-wlfi', 'official-trump', 'chainopera-ai', 'uniswap', 'weth', 'recall', 'hedera-hashgraph', 'mantle', 'pancakeswap-token', 'wrapped-avax', 'dash', 'stellar', 'zora', 'yield-basis', 'polkadot', 'ugold-inc', 'wrapped-hype', 'monero', 'shiba-inu', 'pump-fun', 'pudgy-penguins', 'dogwifcoin', 'bonk', 'arbitrum', 'near', 'thorchain', 'havven', 'kgen', 'curve-dao-token', 'walrus-2', 'binance-bitcoin', 'the-open-network', 'dai', 'sei-network', 'worldcoin-wld', 'world-liberty-financial', 'ondo-finance', 'paypal-usd', 'towns', 'optimism', 'xpin-network', 'basic-attention-token', 'morpho', 'whitebit', 'boundless', 'lab', 'ethena-staked-usde', 'polygon-pos-bridged-dai-polygon-pos', 'arbitrum-bridged-wbtc-arbitrum-one', 'fetch-ai', 'soon-2', 'ripple-usd', 'fartcoin', 'overtake', 'okb', 'unit-bitcoin', 'lido-dao', 'useless-3']
            await coin_provider.get_data()


    asyncio.run(main())
