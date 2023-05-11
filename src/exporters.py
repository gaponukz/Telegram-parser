import abc
import json
import dataclasses

from src import entities

class IExporter(abc.ABC):
    @abc.abstractmethod
    def export(self, users: list[entities.User]) -> None: ...

class ExcelExporter(IExporter):
    def export(self, users: list[entities.User]) -> None:
        raise NotImplementedError

class JsonExporter(IExporter):
    def export(self, users: list[entities.User]) -> None:
        json_data = [dataclasses.asdict(user) for user in users]

        with open("parser_results.json", "w", encoding='utf-8') as out:
            json.dump(json_data, out, indent=4)
