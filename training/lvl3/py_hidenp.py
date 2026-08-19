def hidenp(small: str, big: str) -> bool:
    c = 0
    for i in big:
        if c < len(small) and i == small[c]:
            c += 1
    return c == len(small)

print(hidenp("sing","subsequence testing"))