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


async def get_film(films, session):
    list_films = []
    for film in films:
        response = await session.get(
            f'{film}',
        )
        json_data = await response.json()
        list_films.append(json_data['title'])
    return {'films': ','.join(list_films)}


async def get_species(species, session):
    list_species = []
    for specie in species:
        response = await session.get(
            f'{specie}',
        )
        json_data = await response.json()
        list_species.append(json_data['name'])
    return {'species': ','.join(list_species)}


async def get_starships(starships, session):
    list_starships = []
    for starship in starships:
        response = await session.get(
            f'{starship}',
        )
        json_data = await response.json()
        list_starships.append(json_data['name'])
    return {'starships': ','.join(list_starships)}


async def get_vehicles(vehicles, session):
    list_vehicles = []
    for vehicle in vehicles:
        response = await session.get(
            f'{vehicle}',
        )
        json_data = await response.json()
        list_vehicles.append(json_data['name'])
    return {'starships': ','.join(list_vehicles)}


async def insert_people(people_list, session_http):
    async with SessionDB() as session:
        orm_model_list = []
        for people_dict in people_list:
            people_dict['films'] = await get_film(people_dict['films'], session_http)
            people_dict['species'] = await get_species(people_dict['species'], session_http)
            people_dict['starships'] = await get_starships(people_dict['starships'], session_http)
            people_dict['vehicles'] = await get_vehicles(people_dict['vehicles'], session_http)

            orm_model_list.append(Сharacter(json=people_dict))

        session.add_all(orm_model_list)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:
        coros = (get_people(i, session) for i in range(1, 100_001))
        for coros_chunk in more_itertools.chunked(coros, 5):
            people_list = await asyncio.gather(*coros_chunk)
            await insert_people(people_list, session)
            print(people_list)


asyncio.run(main())
