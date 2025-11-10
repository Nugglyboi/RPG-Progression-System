import structs
import parser

_loot_table = parser.read_csv("data/LootTable.csv", structs.Loot)


def get_drop() -> structs.Loot:
    return _loot_table[0]
