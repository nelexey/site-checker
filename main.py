import aiohttp
import asyncio
import time

TOKEN = ""
CHANNEL = ""
DELAY = 5
FILENAME = "sites.txt"

async def check_link(session, url, status):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return url, True
    except:
        if status:
            message = f"<b>Отчет за </b>{time.strftime('%d.%m %H:%M')}%0AСайт <a href=\"{url}\">{url}</a> не работает."
            await send_message(message)
        return url, False

async def send_message(message):
    async with aiohttp.ClientSession() as session:
        await session.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHANNEL}&text={message}&parse_mode=HTML")

async def main():
    async with aiohttp.ClientSession() as session:
        with open(FILENAME) as file:
            sites = {line.strip(): True for line in file}

        while True:
            tasks = [check_link(session, url, status) for url, status in sites.items()]
            results = await asyncio.gather(*tasks)
            sites.update(results)
            await asyncio.sleep(DELAY)

asyncio.run(main())
