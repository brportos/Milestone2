def atoi(s: str) -> int:
    string = s.strip()
    sign = 1
    i = 0
    result = 0

    if i < len(string) and string[i] in "-+":
        sign = -1 if string[i] == "-" else 1
        i += 1

    while i < len(string) and string[i].isdigit():
        result = result * 10 + int(string[i])
        i += 1

    return sign * result

print(atoi("  +122"))


