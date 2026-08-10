def cryptic_sorter(strings: list[str]) -> list[str]:
    n = len(strings)
    for i in range(n -1):
        for j in range(n -i -1):
            if len(strings[j]) > len(strings[j + 1]):
                strings[j], strings[j + 1] = strings[j + 1], strings[j]
    return strings

print(cryptic_sorter(["aaa","bbb","AAA","BBB"]))
