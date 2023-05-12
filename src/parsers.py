import abc
import typing
import telethon

from src import entities

class IParserIterator(abc.ABC, typing.AsyncIterator[entities.User]):
    @abc.abstractmethod
    def __init__(self, client: telethon.TelegramClient, chat: entities.Username): ...

    def _log_error(self, error: Exception, scope: str):
        if error.__traceback__:
            print(f"{error.__class__.__name__}: {error} on line {error.__traceback__.tb_lineno} ({scope})")

class ChatParserIterator(IParserIterator):
    def __init__(self, client: telethon.TelegramClient, chat: entities.Username):
        self.client = client
        self.chat = chat

        self._current_message_id: int | None = None
    
    async def _get_message_by_id(self, message_id: int) -> telethon.types.Message | None:
        return await self.client.get_messages(self.chat, ids=message_id)
    
    async def __anext__(self) -> entities.User:
        if self._current_message_id is None:
            messages = await self.client.get_messages(self.chat, limit=1)
            self._current_message_id = int(messages[0].id)

        if self._current_message_id <= 0:
            raise StopAsyncIteration
        
        while True:
            try:
                message = await self._get_message_by_id(self._current_message_id)
            
                self._current_message_id -= 1
                
                if self._current_message_id <= 0:
                    raise StopAsyncIteration
            
                message_owner: telethon.types.User = await self.client.get_entity(message.from_id)

            except Exception as error:
                self._log_error(error, "while True, get message owner")
                continue

            return entities.User(
                _id=message_owner.id,
                username=message_owner.username,
                phone=message_owner.phone,
                first_name=message_owner.first_name,
                last_name=message_owner.last_name
            )
    
    def __aiter__(self):
        return self

class ChannelCommentsParserIterator(IParserIterator):
    def __init__(self, client: telethon.TelegramClient, chat: entities.Username):
        self.client = client
        self.chat = chat

        self._current_post_id: int | None = None
        self._comments: list[entities.User] = []

    async def _get_post_by_id(self, post_id: int) -> telethon.types.Message | None:
        return await self.client.get_messages(self.chat, ids=post_id)

    async def _iter_comments(self, start_id: int):
        async for message in self.client.iter_messages(self.chat, reply_to=start_id):
            try:
                message_owner: telethon.types.User = await self.client.get_entity(message.from_id)

                self._comments.append(
                    entities.User(
                        _id=message_owner.id,
                        username=message_owner.username,
                        phone=message_owner.phone,
                        first_name=message_owner.first_name,
                        last_name=message_owner.last_name
                    )
                )
            
            except Exception as error:
                self._log_error(error, "_iter_comments")

    async def __anext__(self) -> entities.User:
        if self._current_post_id is None:
            messages = await self.client.get_messages(self.chat, limit=1)
            self._current_post_id = int(messages[0].id)
        
        if self._comments:
            return self._comments.pop()

        if self._current_post_id <= 0:
            raise StopAsyncIteration
        
        while True:
            try:
                self._current_post_id -= 1
                post = await self._get_post_by_id(self._current_post_id)
                
                if post is None:
                    continue
                
                await self._iter_comments(post.id)

                if not self._comments:
                    continue

                break

            except Exception as error:
                self._current_post_id -= 1
                self._log_error(error, "__anext__, while loop")

        self._current_post_id -= 1
        return self._comments.pop()

    def __aiter__(self):
        return self
