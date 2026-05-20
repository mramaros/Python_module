#!/usr/bin/env/ python3

import abc

class DataProcessor:
    def __init__(self) -> None:
        self._data_registry: list[Any]

    @abstracmethode
    validate(self, data: Any) -> bool:
        return True
    @abstracmethode
    def get_type(self) -> str:
        pass

    def add_to_registry(self, data) -> None:
        self._data_registry.append(data)

    def 
