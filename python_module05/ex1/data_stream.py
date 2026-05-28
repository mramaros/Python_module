#!/usr/bin/env python3

from abc import ABC, abstractmethod
import typing
from typing import Any, List, Dict, Union, Tuple

class DataProcessor:
    def __init__(self) -> None:
        self._storage: list[Any] = []
        self._rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass
    @abstractmethod
    def ingest(self) -> None:
        pass

    def add_to_registry(self, data) -> None:
        self._data_registry.append(data)

    def otput(self) -> Tuple[int, str]:
        item = self._storage.pop(0)
        rank = self._rank
        self._rank += 1
        return (rank, item)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)
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
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(item)
        else:
            self._storage.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            for k, v in data.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    return False
            return True
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    return False
                for k, v in item.items():
                    if not isinstance(k, str) or not isinstance(v, str):
                        return False
            return True
        else:
            return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise Exception("Imroper log data")
        elif isinstance(data, list):
            for item in data:
                self._storage.append(f"{item['log_level']}, {item['log_message']}")
        else:
            self._storage.append(f"{data['log_level']}, {data['log_message']}")

class DataStream(ABC):
    def __init__ (self) -> None:
        self._processors: list[DataProcessor] = []
        self._total_processor: dict[str, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)
        self._total_processor[type(proc).__name__] = 0

    def process_stream(self, stream: list[typing.Any]) -> None:
        for item in stream:
            check = False
            for proc in self._processors:
                if proc.validate(item):
                    proc.ingest(item)
                    name = type(proc).__name__
                    if isinstance(item, list):
                        self._total_processor[name] += len(item)
                    else:
                        self._total_processor[name] += 1
                    check = True
                    break
            if not check:
                print(f"DataStream error - Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = type(proc).__name__
            total = self._total_processor[name]
            remaining = len (proc._storage)
            print(f"{name}: total {total} items processed, remaining {remaining} on processor")


def main() -> None:
    print("=== Code Nexus - Data Stream ===")

    print("\nInitialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    stream.register_processor(NumericProcessor())

    content = [
        'Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING', 
        'log_message': 'Telnet access! Use ssh instead'},
        {'log_level': 'INFO', 'log_message': 'User wil is connected'}],
        42, ['Hi', 'five']
    ]

    print(f"Send first batch of data on stream: {content}")

    stream.process_stream(content)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    print("Send the same batch again")
    stream.process_stream(content)
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors:", end="")
    print("Numeric 3, Text 2, Log 1")

    for _ in range(3):
        stream._processors[0].otput()
    for _ in range(2):
        stream._processors[1].otput()
    for _ in range(1):
        stream._processors[2].otput()
    stream.print_processors_stats()

if __name__ == "__main__":
    main()
