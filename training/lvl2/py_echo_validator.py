def echo_validator(text: str) -> bool:
    cleaned = ""
    for c in text:
        if c.isalpha():
            cleaned += c.lower()
    if not cleaned:
        return False
    return cleaned == cleaned[::-1]



print(echo_validator(""))

