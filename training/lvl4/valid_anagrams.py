def valid_anagram(s: str, t: str) -> bool:
    c = 0
    if len(s) != len(t):
        return False
    for i in s:
        for j in s:
            if c < len(t) and j in t[c]:
                c += 1
  
    return (c == len(t))

print(valid_anagram("abc", "cab"))

# def valid_anagram(s: str, t: str) -> bool:
#     return sorted(s) == sorted(t)