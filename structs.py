import parser


class Loot(parser.CSVRow):
    ItemID: int
    Slot: str
    Quality: str
    BaseItemPower: int
    SellValue: int


class Equipment:
    weapon: int = 0
    helm: int = 0
    chest: int = 0
    legs: int = 0
    accessory: int = 0

    def get_score(self) -> int:
        return self.weapon + self.helm + self.chest + self.legs + self.accessory

    def equip_best(self, loot: list[Loot]):
        for l in loot:
            match l.Slot:
                case "Weapon":
                    self.weapon = max(self.weapon, l.BaseItemPower)
                case "Helm":
                    self.helm = max(self.helm, l.BaseItemPower)
                case "Chest":
                    self.chest = max(self.chest, l.BaseItemPower)
                case "Boots":
                    self.legs = max(self.legs, l.BaseItemPower)
                case _:
                    self.accessory = max(self.accessory, l.BaseItemPower)


class Progression(parser.CSVRow):
    Level: int
    XP_to_Next: int
    Gold_Combat: int
    Gold_NonCombat: int


class Player:
    _exp: int = 0
    level: int = 1

    _loot: list[Loot] = []
    equipment = Equipment()

    gold: int = 0

    _progression: list[Progression]

    def __init__(self):
        self._progression = parser.read_csv("data/Progression.csv", Progression)

    def get_exp(self, amount: int):
        self._exp += amount

        for p in self._progression:
            if p.Level == self.level:
                if self._exp >= p.XP_to_Next:
                    self.level += 1
                    self._exp -= p.XP_to_Next

    def get_loot(self, loot: Loot):
        self._loot.append(loot)
        self.equipment.equip_best(self._loot)


class Inputs:
    combat_chance: float


class World:
    BeatNum: int
    Stage: str
    BeatName: str
    BeatStartStep: int
    ZoneLevel: int
    BeatDC: int
