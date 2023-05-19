import typing
import random
import asyncio
import telethon

from src import entities
from src import exporters
from src import parsers

class Parser:
    def __init__(
        self,
        client: telethon.TelegramClient,
        setting: entities.Settings,
        exporter: exporters.IExporter,
        parser_iterator: parsers.IParserIterator,
        logger_writer: typing.Callable[[str], None]
    ):
        self.setting = setting
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
            self.logger_writer("Client started successfully")
            
            async for user in self.parser_iterator:
                total_users_count = self._get_users_count()
                
                if total_users_count == self.setting.user_count_limit:
                    break

                if self._get_users_count() % 5 == 0:
                    self.exporter.export(self.ready_to_export_users)

                self._add_user(user)

                if self._flip_a_coin():
                    await asyncio.sleep(random.randint(1, 5))
        
        self.exporter.export(self.ready_to_export_users)

    def _flip_a_coin(self) -> bool:
        return random.choices([True, False], [0.05, 0.95])[0]
    
    def run(self):
        self.client.loop.run_until_complete(self.main_parser_loop())
