from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    try:
        return sorted(
            artifacts,
            key=lambda artifact: artifact["power"],
            reverse=True
            )
    except Exception as e:
        print(f"Error: {e}")
        return []


def power_filter(
    mages: list[dict[str, Any]],
    min_power: int
) -> list[dict[str, Any]]:
    try:
        return list(filter(lambda mage: mage["power"] >= min_power, mages))
    except Exception as e:
        print(f"Error: {e}")
        return []


def spell_transformer(spells: list[str]) -> list[str]:
    try:
        return list(map(lambda spell: f"* {spell} *", spells))
    except Exception as e:
        print(f"Erro: {e}")
        return []


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        most = max(mages, key=lambda mage: mage["power"])
        least = min(mages, key=lambda mage: mage["power"])
        power = map(lambda mage: mage["power"], mages)
        average = round(sum(power) / len(mages), 2)
        return {
            "most": most,
            "least": least,
            "avarage": average
        }
    except Exception as e:
        print(f"Error: {e}")
        return {}


if __name__ == "__main__":
    artifacts = [
            {"name": "Crystal Orb", "power": 85, "type": "focus"},
            {"name": "Fire Staff", "power": 92, "type": "fire"}
            ]
    print("\nTesting artifact sorter...")
    sorted_artifact = artifact_sorter(artifacts)
    print(
        f"{sorted_artifact[0]['name']}"
        f"({sorted_artifact[0]['power']} power)"
        f"comes before  ({sorted_artifact[1]['power']} power)"
    )

    spell = spell_transformer(["fireball", "heal", "shield"])
    print("\nTesting spell transformer...")
    print(*spell)
