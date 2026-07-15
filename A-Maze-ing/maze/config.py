#!/usr/bin/env python3
from typing import Any

REQUIRED_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]


def convert_value(config: dict[str, Any]) -> dict[str, Any]:
    try:
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])

        entry = config["ENTRY"].split(',')
        if len(entry) != 2:
            raise ValueError("value not in format (x, y)")
        config["ENTRY"] = (int(entry[0]), int(entry[1]))

        exited = config["EXIT"].split(',')
        if len(exited) != 2:
            raise ValueError("value not in format (x, y)")
        config["EXIT"] = (int(exited[0]), int(exited[1]))

        config["PERFECT"] = config["PERFECT"].upper()
        if config["PERFECT"] == "TRUE":
            config["PERFECT"] = True
        elif config["PERFECT"] == "FALSE":
            config["PERFECT"] = False
        else:
            raise ValueError("PERFECT have to be True or False")

        if "SEED" in config:
            config["SEED"] = int(config["SEED"])
        else:
            config["SEED"] = 42

    except ValueError as e:
        raise ValueError(f"Value invalide in config: {e}")
    return config


def validate_value(config: dict[str, Any]) -> None:
    if config["WIDTH"] < 1:
        raise ValueError("Error, WIDTH have to be greater than 1")
    if config["HEIGHT"] < 1:
        raise ValueError("Error, HEIGHT have to be greater than 1")

    x = config["ENTRY"][0]
    y = config["ENTRY"][1]
    if x < 0 or x > config["WIDTH"] - 1:
        raise ValueError("ENTRY out of bounds")
    if y < 0 or y > config["HEIGHT"] - 1:
        raise ValueError("ENTRY out of bounds")

    x_exit = config["EXIT"][0]
    y_exit = config["EXIT"][1]
    if x_exit < 0 or x_exit > config["WIDTH"] - 1:
        raise ValueError("EXIT out of bounds")
    if y_exit < 0 or y_exit > config["HEIGHT"] - 1:
        raise ValueError("EXIT out of bounds")

    if config["EXIT"] == config["ENTRY"]:
        raise ValueError("ENTRY and EXIT must be different")


def parse_config(filepath: str) -> dict[str, Any]:
    config = {}
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                parts = line.split('=', 1)
                if len(parts) != 2:
                    print(f"invalide line: {line}")
                    continue
                config[parts[0].strip()] = parts[1].strip()

        for cle in REQUIRED_KEYS:
            if cle not in config:
                raise ValueError(f"Error: Missing key {cle}")

        config = convert_value(config)
        validate_value(config)

    except FileNotFoundError:
        print(f"Error : file '{filepath}' not found")

    except Exception as e:
        print(f"Error: {e}")

    return config
