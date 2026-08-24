def whisper_lipher(text: str, shift: int) -> str:
    string = ""
    for i in text:
        if i.isalpha():
            string += chr(ord(i) + shift)
        else:
            continue
    return (string)
print(whisper_lipher("Hello, World!", 3))