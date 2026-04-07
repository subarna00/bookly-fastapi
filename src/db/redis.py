import aioredis
from src.config import Config


token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
)

async def add_token_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=Config.REFRESH_TOKEN_EXPIRY)

async def is_token_blocklisted(jti: str) -> bool:
    exists = await token_blocklist.exists(jti)
    return exists == 1