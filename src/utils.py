import typing
import asyncio
import random
import telethon

from src.entities import Settings
from src.parsers import (
    IParserIterator,
    ChatParserIterator,
    ChannelCommentsParserIterator
)

T = typing.TypeVar('T')

def sync_to_async_bridge(function: typing.Awaitable[T]) -> T:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(function)

def flip_a_coin(chansey: float=.5) -> bool:
    assert 0 <= chansey <= 1
    return random.choices([True, False], [chansey, 1-chansey])[0]

async def is_channel_link(client: telethon.TelegramClient, link: str) -> bool:
    async with client:
        entity = await client.get_entity(link)

    return get_entity_type(entity) == 'channel'

def get_entity_type(
        entity: telethon.types.PeerChat | telethon.types.PeerUser | telethon.types.PeerChannel
    ) -> typing.Literal['user', 'channel', 'chat']:

    if entity.__class__.__name__ == 'User':
        return 'user'
    
    return 'chat' if getattr(entity, 'megagroup', False) else 'channel'

def build_client_from_settings(settings: Settings) -> telethon.TelegramClient:
    return telethon.TelegramClient(
        settings.account.session_path,
        settings.account.api_id,
        settings.account.api_hash
    )

async def get_parser_iterator_due_to_link(client: telethon.TelegramClient, link: str) -> IParserIterator:
    return (ChannelCommentsParserIterator if await is_channel_link(client, link) else ChatParserIterator)(client, link)