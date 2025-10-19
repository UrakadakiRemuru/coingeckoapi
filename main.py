import asyncio

from core.provider.coin_gecko_provider import CoinGeckoProvider
from core.file_creator.json_creator import JSONCreator

if __name__ == '__main__':
    async def main():
        async with CoinGeckoProvider() as coin_provider:
            data = await coin_provider.get_data()
        JSONCreator(data).create_file()

    asyncio.run(main())