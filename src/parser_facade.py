import typing
import random
import asyncio
import telethon

from src import entities
from src import exporters
from src import parsers
from src import utils

class Parser:
    def __init__(
        self,
        client: telethon.TelegramClient,
        exporter: exporters.IExporter,
        parser_iterator: parsers.IParserIterator,
        logger_writer: typing.Callable[[str], None]
    ):
        self.exporter = exporter
        self.parser_iterator = parser_iterator
        self.logger_writer = logger_writer

        self.unique_parsed: set[str] = set()
        self.ready_to_export_users: list[entities.User] = []

        self.client = client

    def _add_user(self, user: entities.User):
        if not str(user) in self.unique_parsed:
            self.unique_parsed.add(str(user))
            self.ready_to_export_users.append(user)
    
    def _get_users_count(self) -> int:
        return len(self.unique_parsed)
    
    async def main_parser_loop(self):
        async with self.client:
            self.logger_writer("Парсер розпочав роботу")
            
            async for user in self.parser_iterator:                
                users_count = self._get_users_count()

                if utils.flip_a_coin(0.05):
                    self.logger_writer(f"Більше ніж {users_count} користувачів зібрано")
                    self.exporter.export(self.ready_to_export_users)

                self._add_user(user)

                if utils.flip_a_coin(0.05):
                    await asyncio.sleep(random.randint(1, 5))
        
        self.logger_writer("Парсер закінчив роботу")
        self.exporter.export(self.ready_to_export_users)
        self.logger_writer("Результат збережено")
