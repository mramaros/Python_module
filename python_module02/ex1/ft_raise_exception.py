#!/usr/bin/python3

def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)

    if temp < 0:
        raise Exception(f"{temp}°C is too cold for plants (min 0°C)")
    if (temp > 40):
        raise Exception(f"{temp}°C too hot for plants (max 40°C)")
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===\n")

    test_value = ["25", "abc", "100", "-25"]
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
