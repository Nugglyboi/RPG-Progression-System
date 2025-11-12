import csv
from typing import Type, Any, get_type_hints, TypeVar

_T = TypeVar("_T", bound="CSVRow")


class CSVRow:
    def __init__(self, **kwargs: dict[Any, Any]):
        self.__dict__ = kwargs


def read_csv(file_path: str, cls: Type[_T]) -> list[_T]:
    hints = get_type_hints(cls)

    def cast(value: str, typ: type):
        if typ == int:
            return int(value)
        elif typ == float:
            return float(value)
        elif typ == bool:
            return value.lower() in ("true", "1", "yes")
        return value

    instances: list[_T] = []

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kwargs = {k: cast(v, hints.get(k, str)) for k, v in row.items()}
            instances.append(cls(**kwargs))  # type: ignore

    return instances
import csv
from typing import Type, Any, get_type_hints, TypeVar

_T = TypeVar("_T", bound="CSVRow")


class CSVRow:
    def __init__(self, **kwargs: dict[Any, Any]):
        self.__dict__ = kwargs


def read_csv(file_path: str, cls: Type[_T]) -> list[_T]:
    hints = get_type_hints(cls)

    def cast(value: str, typ: type):
        if typ == int:
            return int(value)
        elif typ == float:
            return float(value)
        elif typ == bool:
            return value.lower() in ("true", "1", "yes")
        return value

    instances: list[_T] = []

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            kwargs = {k: cast(v, hints.get(k, str)) for k, v in row.items()}
            instances.append(cls(**kwargs))  # type: ignore

    return instances
