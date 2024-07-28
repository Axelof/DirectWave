from cache import client


async def sp_ping() -> bool:
    return await client.ping()
