def whisper_lipher(text: str, shift: int) -> str:
    string = ""
    for i in text:
        if i.isupper():
            string += chr((ord(i) - ord('A') + shift)% 26 + ord('A'))
        elif i.islower():
            string += chr((ord(i) - ord('a') + shift)% 26 + ord('a'))
        else:
            string += i
    return (string)

print(whisper_lipher("xyz", 20))