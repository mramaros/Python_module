#!/usr/bin/env python3

import sys
import typing

def main() -> None:
    if len(sys.argv) != 2:
        print("usage: ft_ancient_text.py <file>")
        return

    file_text = sys.argv[1]
    try:
        file = open(file_text, 'r', encoding='utf-8')
        print(f"Accessing file '{file_text}'")
        content = file.read()
        print(f"---\n\n{content}\n---")
        print(f"file '{file_text}' closed")

        print("\nTransform data:\n")
        new_content = content.replace("\n", "#\n")
        print(f"---\n\n{new_content}\n---")

        new_file = input("Enter new file name (or empty): ")

        if new_file:
            print(f"Saving data to : {new_file}")
            result = open(new_file, 'w', encoding='utf-8')
            result.write(new_content)
            print(f"Data saved in file '{new_file}'")
            result.close()
        else:
            print("Not saving data.")
        file.close()

    except Exception as e:
            print(f"Error opening file '{file_text}: {e}")


if __name__ == "__main__":
    main()
