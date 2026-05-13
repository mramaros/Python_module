#!/usr/bin/env python3

import sys

def main() -> None:
    if len(sys.argv) != 2:
        print("usage: ft_ancient_text.py <file>")
    else:
        print("=== Cyber Archives Recovery & Preservation ===")
        file_text = sys.argv[1]
        try:
            file = open(file_text, 'r', encoding='utf-8')
            print(f"Accessing file: '{file_text}")
            content = file.read()
            print(f"---\n\n{content}\n---")
            print(f"File '{file_text}' closed")
            new_content = content.replace("\n", "#\n")
            
            print(f"Transform data:\n---{new_content}\n---")

            print("Enter new file name (or empty): ",end="", flush=True)
            new_file = sys.stdin.readline().strip()

            if new_file:
                result = open(new_file, 'w', encoding='utf-8')
                result.write(new_content)
                print(f"Data saved in file {new_file}")
            elif len(new_file) == 0:
                print("Not saving Data")
        except Exception as e:
            print(f"[STDERR] Error opening file 'file_text': {e}")
            print("Data not saved")

if __name__ == "__main__":
    main()
