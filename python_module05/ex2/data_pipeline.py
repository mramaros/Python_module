#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: List[str] = []
        self._rank: int = 0
        self._data_registry: List[Any] = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def add_to_registry(self, data: Any) -> None:
        self._data_registry.append(data)

    def output(self) -> tuple[int, str]:
        item = self._storage.pop(0)
        rank = self._rank
        self._rank += 1
        return rank, item


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)
        else:
            return False

    def ingest(
        self, data: int | float | List[int | float]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
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

    def ingest(self, data: str | List[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
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

    def ingest(
        self, data: Dict[str, str] | List[Dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(
                    f"{item['log_level']}, {item['log_message']}"
                )
        else:
            self._storage.append(
                f"{data['log_level']}, {data['log_message']}"
            )


class ExportPlugin(Protocol):
    def process_output(
        self, data: List[tuple[int, str]]
    ) -> None:
        ...


class JSONexport_plugin:
    def process_output(self, data: List[tuple[int, str]]) -> None:
        if not data:
            return
        item: Dict[str, str] = {}
        for rank, value in data:
            item[f"item_{rank}"] = value
        json_parts: List[str] = []
        for k, v in item.items():
            json_parts.append(f'"{k}": "{v}"')
        print("{" + ", ".join(json_parts) + "}")


class CSVexport_plugin:
    def process_output(self, data: List[tuple[int, str]]) -> None:
        if not data:
            return
        csv_lines = ["rank,value"]
        for rank, value in data:
            csv_lines.append(f"{rank},{value}")
        print("CSV Output:")
        print(",".join(csv_lines))


class DataStream(ABC):
    def __init__(self) -> None:
        self._processors: List[DataProcessor] = []
        self._total_processor: Dict[str, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)
        self._total_processor[type(proc).__name__] = 0

    def process_stream(self, stream: List[Any]) -> None:
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
                print(
                    "DataStream error - "
                    f"Can't process element in stream: {item}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = type(proc).__name__
            total = self._total_processor[name]
            remaining = len(proc._storage)
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            data: List[tuple[int, str]] = []
            available = min(nb, len(proc._storage))
            for _ in range(available):
                data.append(proc.output())
            if data:
                plugin.process_output(data)


def main() -> None:
    print("=== Code Nexus - Data Stream ===")

    print("\nInitialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors\n")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    batch: List[Any] = []
    batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]

    print(f"Send first batch of data on stream: {batch}")

    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVexport_plugin())
    print("")
    stream.print_processors_stats()

    batch1 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificateexpires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {batch1}\n")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONexport_plugin())
    print("")
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
