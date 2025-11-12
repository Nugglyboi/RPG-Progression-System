import structs
import csvparser
import utils
import random

_loot_table = csvparser.read_csv("data/LootTable.csv", structs.Loot)

QualityWeights = {
    "T1": {
        "Common": 0,
        "Rare": 0,
        "Epic": 0,
        "Legendary": 0.0,
    },
    "T2": {
        "Common": 0.55,
        "Rare": 0.3,
        "Epic": 0.12,
        "Legendary": 0.03,
    },
    "T3": {
        "Common": 0.4,
        "Rare": 0.35,
        "Epic": 0.2,
        "Legendary": 0.05,
    },
    "T4": {
        "Common": 0.25,
        "Rare": 0.4,
        "Epic": 0.27,
        "Legendary": 0.08,
    },
}

PieceWeights = {
    "Weapon": 0.15,
    "Chest": 0.25,
    "Helm": 0.2,
    "Boots": 0.2,
    "Accessory": 0.2,
}


def weighted_choice(weight_dict: dict[str, float]) -> str:
    r = random.random() * sum(weight_dict.values())

    for key, weight in weight_dict.items():
        r -= weight
        if r <= 0:
            return key

    return list(weight_dict.keys())[-1]  # Fallback


def get_drop(world: structs.World) -> structs.Loot | None:
    if utils.chance(.50):
        return None  # no drop

    slot = weighted_choice(PieceWeights)
    quality = weighted_choice(QualityWeights[f"T{world.ZoneTier}"])

    possible_drops = [x for x in _loot_table if x.Slot == slot and x.Quality == quality]
    if not possible_drops:
        return None

    return random.choice(possible_drops)
