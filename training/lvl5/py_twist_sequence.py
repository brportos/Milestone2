def twist_sequence(arr: list[int], k: int) -> list[int]:
    if not arr:
        return arr
    k = k % len(arr)
    return arr[-k:] + arr[:-k] if k != 0 else arr
