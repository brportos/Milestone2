#!/usr/bin/env python3

def input_temperature(temp_str: str = "") -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===\n")

    temp_str = "25"
    print(f"Input data is '{temp_str}'")
    try:
        temp = int(input_temperature(temp_str))
        print(f"Temperature is now {temp}°C")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")

    temp_str = "abc"
    print(f"\nInput data is '{temp_str}'")
    try:
        temp = int(input_temperature(temp_str))
        print(f"Temperature is now {temp}°C")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}")

    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
