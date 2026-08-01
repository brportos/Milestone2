from functools import wraps
import time
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Spell completed in {end - start:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Any:
        @wraps(func)
        def wrapper(power: int, *args: Any, **kwargs: Any) -> Any:
            if power >= min_power:
                return func(power, *args, **kwargs)
            else:
                return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            "Spell failed, retrying..."
                            f"(attempt {attempt}/{max_attempts})"
                            )
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name)

    def cast_spell(self, spell_name: str, power: int) -> Any:
        @power_validator(min_power=10)
        def cast(power: int, spell_name: str) -> str:
            return f"Successfully cast {spell_name} with {power} power"
        return cast(power, spell_name)


if __name__ == "__main__":
    @spell_timer
    def fireball() -> str:
        time.sleep(0.101)
        return f"Result: {fireball.__name__.capitalize()} cast!\n"
    print("Testing spell timer...")
    print(fireball())

    print("Testing retrying spell...")

    @retry_spell(max_attempts=3)
    def unstable_spell() -> None:
        raise ValueError("Error")
    print(unstable_spell())
    print("Waaaaaaagh spelled!")

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Gandalf"))
    print(MageGuild.validate_mage_name("G1"))
    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))
