#!/usr/bin/env python3

def input_temperature(temp_str: str = "") -> int:
    temp = int(temp_str)
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    elif temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    else:
        return temp


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===\n")

    temp_strs = ["25", "abc", "100", "-50"]
    for temp_str in temp_strs:
        print(f"Input data is {temp_str!r}")
        try:
            temp = int(input_temperature(temp_str))
            print(f"Temperature is now {temp}°C\n")
        except ValueError as e:
            print(f"Caught input_temperature error: {e}\n")
    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
