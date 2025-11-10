import structs
import story
import loot
import log
import utils


def combat(
    player: structs.Player,
    world: structs.World,
    stats: structs.Statistics,
):
    success = utils.chance(50)  # TODO generate chance
    stats.Success = success

    if success:
        death = utils.chance(1)  # TODO generate chance
        stats.Death = death

        if not death:
            exp = 10  # TODO calculate exp
            player.award_exp(exp)
            stats.XP_Earned = exp

            gold = 1  # TODO calculate gold
            player.award_gold(gold)
            stats.Gold_Earned = gold

            drop = loot.get_drop()
            if drop is not None:
                player.award_loot(drop)
                stats.DropID = drop.ItemID


def non_combat(
    player: structs.Player,
    world: structs.World,
    stats: structs.Statistics,
):
    # decide success
    # award exp
    pass


def simulate(turns: int, inputs: structs.Inputs):
    player = structs.Player()
    world = story.create_world()

    for turn in range(turns):
        stats = structs.Statistics()

        # decide action
        if utils.chance(inputs.combat_chance):
            combat(player, world, stats)
        else:
            non_combat(player, world, stats)

        # change stage
        story.progress_story(turn, world)

        # record results
        log.record_turn(turn, player, world, stats)
