import structs
import story
import loot
import log
import utils
import inputs
import math


def combat(
    player: structs.Player,
    world: structs.World,
    stats: structs.Statistics,
):
    # skill_check returns (success_bool, success_probability). Unpack it so we
    # don't accidentally store a tuple into stats.Success (which would embed a
    # comma in the CSV and break column alignment).
    success_bool, success_prob = utils.skill_check(
        utils.power_ratio(player, world), world.BeatDC / 20
    )
    # record the skill-check probability separately; the independent combat
    # chance metric is recorded at the start of the step so it is available on
    # non-combat turns as well (see simulate()).
    stats.SkillCheckProbability = success_prob
    stats.Success = success_bool
    # keep a local `success` variable for existing flow control below
    success = success_bool

    if success:
        chance = utils.death_chance(player, world)
        death = utils.chance(chance)
        stats.DeathChance = chance
        stats.Death = death

        if not death:
            exp = math.floor(
                utils.skill_difficulty(player, world) * inputs.BASE_XP_COMBAT
            )
            player.award_exp(exp)
            stats.XP_Earned = exp

            gold = inputs.GOLD_PER_COMBAT_STEP
            player.award_gold(gold)
            stats.Gold_Earned = gold

            drop = loot.get_drop(world)
            if drop is not None:
                player.award_loot(drop)
                stats.DropID = drop.ItemID


def non_combat(
    player: structs.Player,
    world: structs.World,
    stats: structs.Statistics,
):
    category = utils.non_combat_category(world)
    stats.OutcomeCategory = category.OutcomeCategory
    stats.SkillDifficulty = category.CategoryDC

    stat = player.get_stat(category.StatKey)
    stats.BaseStat = stat.Base
    stats.PerLevel = stat.PerLevel

    chance = utils.non_combat_chance(player, world, category.OutcomeCategory)
    success = utils.chance(chance)
    stats.StatScore = utils.stat_score(player, category.StatKey)
    stats.SuccessChance_NonCombat = chance
    stats.Success = success

    exp = math.floor(utils.skill_difficulty(player, world) * inputs.BASE_XP_NON_COMBAT)
    player.award_exp(exp)
    stats.XP_Earned = exp

    if success:
        # maybe use nc_rules.csv
        gold = inputs.GOLD_PER_NON_COMBAT_STEP
        player.award_gold(gold)
        stats.Gold_Earned = gold


def simulate(turns: int):
    player = structs.Player()
    world = story.create_world()

    for turn in range(turns):
        stats = structs.Statistics()

        # compute and record the independent combat-chance metric every step
        # so the CSV/plots show the combat difficulty even on non-combat steps
        # Also compute the underlying ability and difficulty so we can export
        # them for debugging/plotting.
        pr = utils.power_ratio(player, world)
        stats.Power_Ratio = pr
        level_frac = player.level / max(1, player.max_level())
        stats.Ability = pr * level_frac
        stats.Difficulty = world.ZoneLevel / (story.max_zone_level() / 2)
        stats.SuccessChanceCombat = utils.combat_chance(player, world)

        # decide action
        if utils.chance(inputs.COMBAT_CHANCE):
            combat(player, world, stats)
        else:
            non_combat(player, world, stats)

        # change stage
        world = story.progress_story(turn, world)

        # record results
        log.record_turn(turn, player, world, stats)
