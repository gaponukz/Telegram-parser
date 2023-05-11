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

class CsvExporter(IExporter):
    def export(self, users: list[entities.User]) -> None:
        with open('parser_results.csv', 'w', encoding='utf-8') as out:
            out.write('_id,username,phone,first_name,last_name\n')
            
            for user in users:
                username = user.username if user.username is not None else ''
                phone = user.phone if user.phone is not None else ''
                last_name = user.last_name if user.last_name is not None else ''
                
                row = f'{user._id},{username},{phone},{user.first_name},{last_name}\n'
                out.write(row)
