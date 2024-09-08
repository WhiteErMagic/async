import asyncio

import aiohttp
import more_itertools
import requests
import os
from models import SessionDB, init_orm, Сharacter

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'flask_db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')


async def get_people(people_id, session):
    response = await session.get(
        f'https://swapi.py4e.com/api/people/{people_id}/',
    )
    json_data = await response.json()
    return json_data


async def insert_people(people_list):
    async with SessionDB() as session:
        orm_model_list = [
            Сharacter(json=people_dict)
            for people_dict in people_list
        ]
        session.add_all(orm_model_list)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:
        coros = (get_people(i, session) for i in range(1, 100_001))
        for coros_chunk in more_itertools.chunked(coros, 5):
            people_list = await asyncio.gather(*coros_chunk)
            await insert_people(people_list)
            print(people_list)


asyncio.run(main())
