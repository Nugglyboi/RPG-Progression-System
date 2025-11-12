import csvparser as parser
import structs
import random
import math
import params
import inputs
import story

_nc_categories = parser.read_csv("data/NC_Categories.csv", structs.NCCategory)
# _nc_rules ?
_non_combat = parser.read_csv("data/NonCombat.csv", structs.NonCombat)


def chance(percent: float) -> bool:
    return random.random() <= clamp(percent, floor=0, ceil=1)


def logistic(x: float, *args, L: float = 1.0, k: float = 1.0, x0: float = 0.0) -> float:
    """Logistic function.

    Accepts either keyword-style calls (recommended) such as
        logistic(x, L=1.0, k=1.0, x0=0.0)
    or a legacy positional form used in this codebase:
        logistic(x, x0, k)

    Positional mapping (if provided):
        args[0] -> x0
        args[1] -> k
        args[2] -> L
    """
    # Map legacy positional args to their respective parameters
    if len(args) >= 1:
        x0 = args[0]
    if len(args) >= 2:
        k = args[1]
    if len(args) >= 3:
        L = args[2]

    return L / (1 + math.exp(-k * (x - x0)))


def skill_check(
    ratio: float,
    DC: float,
    steepness: float = 1.0,
) -> tuple[bool, float]:
    """
    Determine success probability based on ratio vs. DC using a logistic curve. When ratio == DC, then there is a 50% chance of success.

    Parameters:
        ratio     : player's effective power ratio or stat score
        DC        : difficulty (d20 roll)
        steepness : how quickly probability ramps up around equality

    Returns:
        (success, chance)
    """

    x = ratio - DC
    chance = logistic(x, L=1.0, k=steepness, x0=0.0)
    success = random.random() < chance
    return success, chance


def clamp(x: float, *, floor: float, ceil: float):
    return max(floor, min(ceil, x))


def power_ratio(player: structs.Player, world: structs.World) -> float:
    # Use a direct, linear comparison of player gear score to zone demand so
    # the ratio is intuitive: if player's gear > zone demand the ratio > 1.
    # The demand scales with zone level times the number of gear slots.
    demand = max(1, world.ZoneLevel * inputs.GEAR_SLOTS)
    return player.equipment.get_score() / demand
    
def stat_score(player: structs.Player, stat_key: str) -> float:
    stat = player.get_stat(stat_key)

    return (
        stat.Base
        + (player.level * stat.PerLevel)
        + (player.equipment.get_score() / max(1, inputs.GEAR_STAT_SCALING))
    )


def combat_chance(player: structs.Player, world: structs.World) -> float:
    """
    Compute combat success chance based on the player's power ratio.

    The result is centered so that a power ratio of 1.0 => ~50% chance. Values
    below 1.0 give <50% and above 1.0 give >50%. The logistic steepness is
    controlled by the COMBAT_SLOPE parameter (or params.COMBAT_SLOPE) and the
    returned chance is clamped to the configured FLOOR_SUCCESS/CEIL_SUCCESS.

    We intentionally use the raw power ratio as the curve input so the mapping
    is intuitive (ratio > 1 means player power > zone demand -> >50% chance).
    """

    ratio = power_ratio(player, world)
    # Use params-defined slope/limits when available; fall back to inputs otherwise
    slope = getattr(params, "COMBAT_SLOPE", inputs.COMBAT_SLOPE)
    floor = getattr(params, "FLOOR_SUCCESS", 0.0)
    ceil = getattr(params, "CEIL_SUCCESS", 1.0)

    # Logistic centered at x0=1.0 (so ratio==1 -> 50%), L=1.0
    raw = logistic(ratio, L=1.0, k=slope, x0=1.0)
    return clamp(raw, floor=floor, ceil=ceil)


def non_combat_chance(
    player: structs.Player, world: structs.World, category_key: str
) -> float:
    category = _nc_categories[0]
    for cat in _nc_categories:
        if cat.OutcomeCategory == category_key:
            category = cat

    tn = category.CategoryDC + world.BeatDC
    uni = clamp(
        (21 - (tn - stat_score(player, category.StatKey))) / 20,
        floor=0,
        ceil=1,
    )
    success_chance = clamp(
        1 / (1 + math.exp(-params.ATTEMPT_SLOPE * (tn - uni))),
        floor=params.FLOOR_SUCCESS,
        ceil=params.CEIL_SUCCESS,
    )

    return success_chance


def death_chance(player: structs.Player, world: structs.World) -> float:
    return (1 - combat_chance(player, world)) * inputs.DEATH_SEVERITY


def non_combat_category(world: structs.World) -> structs.NCCategory:
    rand = random.random()

    scenario = _non_combat[0]
    for s in _non_combat:
        thresh = 0
        if world.ZoneTier == 1:
            thresh = s.T1Threshold
        elif world.ZoneTier == 2:
            thresh = s.T2Threshold
        elif world.ZoneTier == 3:
            thresh = s.T3Threshold
        elif world.ZoneTier == 4:
            thresh = s.T4Threshold
        if rand <= thresh:
            scenario = s
            break

    category = _nc_categories[0]
    for cat in _nc_categories:
        if cat.OutcomeCategory == scenario.Category:
            category = cat

    return category


def skill_difficulty(player: structs.Player, world: structs.World) -> float:
    skill_noise = math.sqrt(-2 * math.log(random.random())) * math.cos(
        2 * math.pi * random.random()
    )
    skill_difficulty = inputs.SKILL_DIFF_TIER_MULT + world.ZoneTier * skill_noise
    return skill_difficulty
