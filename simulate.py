import structs
import story
import loot
import log
import utils
import inputs


def combat(
    player: structs.Player,
    world: structs.World,
    stats: structs.Statistics,
):
    chance = utils.combat_chance(player, world)
    success = utils.chance(chance)
    stats.SuccessChanceCombat = chance
    stats.Success = success

    if success:
        chance = utils.death_chance(player, world)
        death = utils.chance(chance)
        stats.DeathChance = chance
        stats.Death = death

        if not death:
            exp = 10  # TODO calculate exp
            player.award_exp(exp)
            stats.XP_Earned = exp

            gold = 1  # TODO calculate gold
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
    category = utils.non_combat_category()
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

    # TODO calculate exp
    # TODO calculate gold
    if success:
        # nc_rules.csv
        exp = 10
        gold = 1
    else:
        exp = 10
        gold = 0

    player.award_exp(exp)
    stats.XP_Earned = exp

    player.award_gold(gold)
    stats.Gold_Earned = gold


def simulate(turns: int):
    player = structs.Player()
    world = story.create_world()

    for turn in range(turns):
        stats = structs.Statistics()

        # decide action
        if utils.chance(inputs.COMBAT_CHANCE):
            combat(player, world, stats)
        else:
            non_combat(player, world, stats)

        # change stage
        world = story.progress_story(turn, world)

        # record results
        log.record_turn(turn, player, world, stats)
