#!/usr/bin/env/ python3

from abc import ABC, abstractmethod
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

    def otput(self) -> None:
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

def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    try:
        print("Test invalid ingestion of string 'foo' without prior validation:")
        numeric.ingest('foo')
    except Exception as e:
        print(f"Cot Exception: {e}")
    numeric.ingest([1, 2, 3, 4, 5])
    print("Processing data: [1, 2, 3, 4, 5]")
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.otput()
        print(f"Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    text.ingest(['Hello', 'Nexus', 'World'])
    print(f"Processing data: ['Hello', 'Nexus', 'World']")
    print("Extracting 1 value...")
    rank, value = text.otput()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    
    logs = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]

    log.ingest(logs)
    print("Processing data: [{'log_level': 'NOTICE', 'log_message':", end="")
    print(" 'Connection to server'}, {'log_level': 'ERROR\n\t',", end=" ")
    print("'log_message': 'Unauthorized access!!'}]")
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.otput()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
