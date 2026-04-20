#!/usr/bin/python3

def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===\n")

    test_value = ["25", "abc"]

    for value in test_value:
        print(f"Input data is '{value}'")
        try:
            temp = input_temperature(value)
            print(f"Temperature is now {temp}°C\n")
        except Exception as e:
            print(f"Caught input_temperature error: {e}\n")

    print("All test completed - program didn't crash")


if __name__ == "__main__":
    test_temperature()
