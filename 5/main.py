import asyncio
import sys
import platform
import aiohttp
from datetime import date, timedelta
from pprint import pprint
from loguru import logger


def main():
    async def request(url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        r = await response.json()
                        return r
                    logger.error(f"Error status {response.status} for {url}")
            except aiohttp.ClientConnectorError as e:
                logger.error(f"Connection error {url}: {e}")
            return None

    async def get_exchange(date):
        res = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}')
        return res

    def exchange_on_date():
        res = {}
        lst_exc = {'EUR': 0, 'USD': 0}
        cur_eur = {'sale': 0, 'purchase': 0}
        cur_usd = {'sale': 0, 'purchase': 0}
        for val in r['exchangeRate']:
            if val['currency'] == 'EUR':
                cur_eur['sale'] = val['saleRate']
                cur_eur['purchase'] = val['purchaseRate']
            if val['currency'] == 'USD':
                cur_usd['sale'] = val['saleRate']
                cur_usd['purchase'] = val['purchaseRate']
        lst_exc['EUR'] = cur_eur
        lst_exc['USD'] = cur_usd
        res[r['date']] = lst_exc
        return res

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for date in dates:
        r = asyncio.run(get_exchange(date))
        exc = exchange_on_date()
        pprint(exc)


if __name__ == "__main__":

    try:
        NUM_DAYS = int(sys.argv[1])
        print(f'Start downloading of exchange for {NUM_DAYS} days')
        dates = []
        for i in range(1, NUM_DAYS + 1):
            dates.append((date.today() - timedelta(i)).strftime('%d.%m.%Y'))
    except IndexError:
        print(f'Enter command in format "py main.py x"')
    else:
        main()
