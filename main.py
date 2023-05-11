import telethon

from src.parser_facade import Parser
from src.parsers import ChatParserIterator
from src.parsers import ChannelCommentsParserIterator
from src.settings import JsonSettings
from src.exporters import JsonExporter

settings = JsonSettings().load()

client = telethon.TelegramClient(
    settings.account.session_path,
    settings.account.api_id,
    settings.account.api_hash
)

if settings.entity_type == 'chat':
    parser_iterator = ChatParserIterator(client, settings.entity_to_parse)

elif settings.entity_type == 'channel':
    parser_iterator = ChannelCommentsParserIterator(client, settings.entity_to_parse)

parser = Parser(client, settings, JsonExporter(), parser_iterator)

if __name__ == '__main__':
    parser.run()
