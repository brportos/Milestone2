def inter(s1: str, s2: str) -> str:
    strings = ""
    for i in s1:
        if i in set(s2) and i not in strings:
            strings += i
    return strings

print(inter("banana", "band"))
