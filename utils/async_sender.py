import aiohttp
import orjson
import asyncio
from retrying_async import retry
from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv
from utils.log_func import *

load_dotenv(".env")
playmatrix=getenv('playmatrix_endpoint')

logg=logging_func("sending-data",getenv("sender_logs"))[1] #get only logger object

@dataclass
class AsyncSender:

    @retry(attempts=10, delay=0.2)
    async def send_single_resolved_fixture(self,session: aiohttp.ClientSession, fixture: dict):
        form_data = aiohttp.FormData()
        form_data.add_field("data", orjson.dumps(fixture))
        """
        logging resolved games for quick check of first 3 resolved games validity 
        """
        logg.info(f"RESOLVING, gameid: {fixture['fixtureId']}, gamesLength: {len(fixture['games'])}, resolved_games: {fixture['games'][0:3]}")
        #with open('data/resolved_' + str(fixture['fixtureId']) + '.json', 'w') as outfile:
        #    json.dump(fixture, outfile)
        # async with session.post(f"{playmatrix}results/full?sourceId={fixture['source']}",
        #                         data=form_data, verify_ssl=False) as response:
        #     if response.status != 200:
        #         logg.error(f"Error sending markets of {fixture['fixtureId']} to COU. Response: {response}")
        #         return False

    @retry(attempts=10, delay=0.2)
    async def send_single_live_fixture(self,session: aiohttp.ClientSession, fixture: dict):
        form_data = aiohttp.FormData()
        form_data.add_field("data", orjson.dumps(fixture))
        #logg.info(f"MARKETS, gameid: {fixture['fixtureId']}, gamesLength: {len(fixture['games'])}, compstring: {fixture['competitionString']}")
        # with open('data/markets_' + str(fixture['fixtureId']) + '.json', 'w') as outfile:
        #    json.dump(fixture, outfile)
        # async with session.post(f"{playmatrix}live/full?sourceId={fixture['source']}",
        #                         data=form_data, verify_ssl=False) as response:
        #     if response.status != 200:
        #         logg.error(f"Error sending markets of {fixture['fixtureId']} to COU. Response: {response}")
        #         return False

    async def send_all_markets(self, fixtures: list):
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.send_single_live_fixture(session=session, fixture=fixture),name=None) for fixture in fixtures]
            return await asyncio.gather(*tasks)

    async def send_all_resolved_live(self, fixtures: list):
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.send_single_resolved_fixture(session=session, fixture=fixture),name=None) for fixture in fixtures]
            return await asyncio.gather(*tasks)
