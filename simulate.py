import structs
import story
import loot
import log
import utils


def combat(player: structs.Player, world: structs.World):
    if utils.chance(50):  # TODO generate chance
        player.get_exp(10)
        player.get_loot(loot.get_drop())


def non_combat(player: structs.Player):
    # decide success
    # award exp
    pass


def simulate(turns: int, inputs: structs.Inputs):
    player = structs.Player()
    world = story.create_world()

    for turn in range(turns):
        # decide action
        if utils.chance(inputs.combat_chance):
            combat(player, world)
        else:
            non_combat(player)

        # change stage
        story.progress_story(turn, world)

        # record results
        log.record_turn(turn, player)
