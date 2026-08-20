def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    if not (2 <= from_base <= 36 or 2 <= to_base <= 36):
        return "ERROR"
    result = ""
    try:
        decimal = int(number, from_base)
    except ValueError:
        return "ERROR"
    if decimal == 0:
        return "0"
    
    base = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while decimal > 0:
        result = base[decimal % to_base] + result
        decimal //= to_base
    return result

print(number_base_converter("G", 34, 10))