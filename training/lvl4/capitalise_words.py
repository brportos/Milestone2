def capitalize_words(s: str) -> str:
    return " ".join(word.capitalize() for word in s.split(" "))

print(capitalize_words("42madrid exam"))