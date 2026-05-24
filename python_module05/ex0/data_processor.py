#!/usr/bin/env/ python3

import abc

class DataProcessor:
    def __init__(self) -> None:
        self._data_registry: list[Any]

    @abstracmethode
    def validate(self, data: Any) -> bool:
        pass
    @abstracmethode
    def ingest(self) -> None:
        pass

    def add_to_registry(self, data) -> None:
        self._data_registry.append(data)

    def otput(self) -> None:
        item = self._storage.pop(0)
        rank = self._rank
        self._rank += 1
        return (rank, )


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            for item in data:
                if not isinstance(data, (int, float)):
                    return False
            return True
        else:
            return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")
        elif isinstance(data, list):
            for item in data:
                self._storage.append(str(item))
        else:
            self._storage.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        elif isinstance(data, list):
            for item in data:
                if ()
