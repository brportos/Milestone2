def bracket_validator(s: str) -> bool:
    brackets = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    stack = []
    for i in s:
        if i in brackets:
            if stack and stack[-1] == brackets[i]:
                stack.pop()
            else:
                return False
        elif i in brackets.values():
            stack.append(i)
    return True if not stack else False


print(bracket_validator("hello(wo[rld])"))