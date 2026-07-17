#!/usr/bin/env python3

import sys
import typing


def open_file(filename: str,  mode: str) -> typing.IO[str] | None:
    file: typing.IO[str] | None = None
    try:
        file = open(filename, mode)
    except OSError as e:
        print(
            f"[STDERR] Error opening file {filename!r}: {e}", file=sys.stderr
            )
    return file


def read_content(filename: str) -> str:
    file: typing.IO[str] | None = open_file(filename, "r")
    if file is None:
        return ""
    content: str = file.read()
    print(f"---\n\n{content}\n\n---")
    file.close()
    print(f"File {filename!r} closed.")
    return content


def transform_content(content: str) -> str:
    lines: list[str] = content.splitlines()
    new_lines: list[str] = []
    for line in lines:
        new_lines.append(line + "#")
    return "\n".join(new_lines) + "\n"


def save_content(transformed: str) -> None:
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_filename: str = sys.stdin.readline().rstrip("\n")
    if new_filename == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{new_filename}'")
    file: typing.IO[str] | None = open_file(new_filename, "w")
    if file is None:
        print("Data not saved.")
        return
    file.write(transformed)
    file.close()
    print(f"Data saved in file {new_filename!r}.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        if sys.argv[0][:2] == "./":
            print(f"Usage: {sys.argv[0][2:]} <file>\n")
        else:
            print(f"Usage: {sys.argv[0]} <file>\n")
        sys.exit(1)
    print("=== Cyber Archives Recovery & Preservation ===")
    filename: str = sys.argv[1]
    print(f"Accessing file {filename!r}")

    content: str = read_content(filename)
    if content == "":
        sys.exit(1)
    transformed: str = transform_content(content)
    print("\nTransform data:")
    print(f"---\n\n{transformed}\n---")
    save_content(transformed)
