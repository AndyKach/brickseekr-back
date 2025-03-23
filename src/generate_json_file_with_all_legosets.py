import asyncio
import json
from infrastructure.config.repositories_config import legosets_repository

async def generate():
    legosets = await legosets_repository.get_all()
    result = []
    for legoset in legosets:
        result.append({'legoset_id': legoset.id, 'name': legoset.name})

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)



asyncio.run(generate())
