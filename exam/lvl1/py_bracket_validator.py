def bracket_validator(s: str) -> bool:
    stack = []
    brackets = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    for c in s:
        if c in brackets:
            if stack and stack[-1] == brackets[c]:
                stack.pop()
            else:
                return False
        elif c in brackets.values():
            stack.append(c)
    return True if not stack else False

print(bracket_validator("hello(Word)"))
