import abc
import json
from src import entities

class ISetting(abc.ABC):
    @abc.abstractmethod
    def load(self) -> entities.Settings: ...

class JsonSettings(ISetting):
    def load(self) -> entities.Settings:
        with open('settings.json', 'r', encoding='utf-8') as out:
            settings = entities.Settings(**json.load(out))
            settings.account = entities.TelegramClientPrivateData(**settings.account)
            
            return settings

class TestSettings(ISetting):
    def load(self) -> entities.Settings:
        return entities.Settings(
            entity_to_parse='',
            entity_type='channel',
            user_count_limit=10,
            account=entities.TelegramClientPrivateData(
                session_path="account/session",
                api_id=0,
                api_hash="secret"
            )
        )
