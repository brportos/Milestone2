def count_vowel(s: str) -> int:
    count = 0
    for i in s:
        if i.lower() in "eyuioa":
            count += 1
    return count

def get_sorted(s: str):
    return (len(s), s.lower(), count_vowel(s))

def cryptic_sorter(strings: list[str]) -> list[str]:
    for i in range(len(strings)):
        for j in range(len(strings)-1 -i):
            if get_sorted(strings[j]) > get_sorted(strings[j + 1]):
                strings[j], strings[j + 1] = strings[j + 1], strings[j]
            
    return strings

print(cryptic_sorter(["aaa", "AAA","boo","cat"]))