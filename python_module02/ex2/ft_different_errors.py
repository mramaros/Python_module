#!/usr/bin/python3

def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        _ = 10 / 0
    elif operation_number == 2:
        open("non/existent/file")
    elif operation_number == 3:
        _ = "hello" + 5
    else:
        print("Operation completed successfully")


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")

    for i in range(5):
        try:
            garden_operations(i)
        except ValueError as e:
            print(f"Caught ValueError: {e}")
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
        except FileNotFoundError as e:
            print(f"Caught FileNotFoundError: {e}")
        except (TypeError, Exception) as e:
            print(f"Caught error: {e}")

    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
