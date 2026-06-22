#!/usr/bin/env python3

import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: ft_ancient_text.py <file>")
        return

    file_text = sys.argv[1]
    try:
        io: typing.IO = open(file_text, 'r', encoding='utf-8')
        print(f"Accessing file '{file_text}'")
        content = io.read()
        print(f"---\n\n{content}\n---")
        print(f"file '{file_text}' closed")
        io.close()

        print("\nTransform data:\n")
        new_content = content.replace("\n", "#\n")
        print(f"---\n\n{new_content}\n---")

        new_file = input("Enter new file name (or empty): ")

        if new_file:
            print(f"Saving data to : {new_file}")
            io:typing.IO = open(new_file, 'w', encoding='utf-8')
            io.write(new_content)
            print(f"Data saved in file '{new_file}'")
            io.close()
        else:
            print("Not saving data.")

    except Exception as e:
        print(f"Error opening file '{file_text}: {e}")


if __name__ == "__main__":
    main()
