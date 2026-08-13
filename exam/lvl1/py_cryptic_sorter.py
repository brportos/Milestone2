def count_vowels(s: str) -> int:
    count = 0
    for i in s.lower():
        if i in "eyuioa":
            count += 1
    return count

def cryptic_sorter(strings: list[str]) -> list[str]:

    def get_sort_key(s):
        return (len(s), s.lower(), count_vowels(s))

    for i in range(len(strings)):
        item = strings[i]
        key = get_sort_key(item)
        j = i - 1

        while j >= 0 and get_sort_key(strings[j]) > key:
            strings[j + 1] = strings[j]
            j -= 1

        strings[j + 1] = item
    return strings



print(cryptic_sorter(["aaa","bbb","AAA","BBB"]))