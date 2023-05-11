import typing
import dataclasses

Phone: typing.TypeAlias = str
Username: typing.TypeAlias = str

@dataclasses.dataclass
class TelegramClientPrivateData:
    session_path: str
    api_id: int
    api_hash: str

@dataclasses.dataclass
class Settings:
    entity_to_parse: Username
    entity_type: typing.Literal['chat', 'channel']
    user_count_limit: int
    account: TelegramClientPrivateData

@dataclasses.dataclass
class User:
    _id: int
    username: Username | None
    phone: Phone | None
    first_name: str
    last_name: str | None
