import sys
import os
import typing

def main() -> None:
    if len(sys.argv[1:])
        print("usage: ft_ancient_text.py <file>")

    else:
        file_text = sys.argv[1]
        try:
            print(f"Accessing file '{file_text}'")

            with open(file_text, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"---\n\n{content}\n---")


