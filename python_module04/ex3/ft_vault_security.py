#!/usr/bin/env python3

def secure_archive(source: str, dest: str) -> tuple[bool, str]:
    try:
        with open(source, 'r', encoding='utf-8') as file:
            content = file.read()

        if source == dest:
            return (True, "Content successfully written to file")

        with open(dest, 'w', encoding='utf-8') as file_dest:
            file_dest.write(content)
            print(f"{content}")

        return (True, content)

    except Exception as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(f"{secure_archive("/not/existing/file", "result_test.txt")}\n")

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(f"{secure_archive("/etc/shadow", "dest_test.txt")}\n")

    print("Using 'secure_archive' to read from a regular file:")
    print(f"{secure_archive("source.txt", "dest.txt")}\n")

    print("Using 'secure_archive' to write previous content to a new file:")
    print(f"{secure_archive("source.txt", "source.txt")}")


if __name__ == "__main__":
    main()
