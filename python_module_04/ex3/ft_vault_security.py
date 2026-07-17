#!/usr/bin/env python3

def secure_archive(
    filename: str, action: int = 0, content: str = ""
        ) -> tuple[bool, str]:

    try:
        if action == 0:
            with open(filename, "r") as file:
                data = file.read()
            return (True, data)
        if action == 1:
            with open(filename, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
    except OSError as e:
        return (False, str(e))
    return (False, "Invalid action")


if __name__ == "__main__":
    print("=== Cyber Archives Security ===")
    result = secure_archive("/not/existing/file")
    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    print(result)
    result = secure_archive("/etc/shadow")
    print("\nUsing 'secure_archive' to read from an inaccessible file: ")
    print(result)
    result = secure_archive("ancient_fragment.txt")
    print("\nUsing 'secure_archive' to read from a regular file: ")
    print(result)
    result = secure_archive("new_vault.txt", 1, result[1])
    print("\nUsing 'secure_archive' to write previous content to a new file: ")
    print(result)
