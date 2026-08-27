def alternate_case(s: str) -> str:
    string = ""
    for i, char in enumerate(s):
        if char.isalpha():
            if i % 2 == 0:
                string += char.upper()
            else:
                string += char.lower()
        else:
            string += char

    return string

print(alternate_case("a!b?c python3"))