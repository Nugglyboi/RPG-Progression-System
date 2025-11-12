import random
import utils
import structs
import story

random.seed(12345)

player = structs.Player()
world = story.create_world()

chance = utils.combat_chance(player, world)
print(f"Computed combat chance: {chance:.6f}")

trials = 100000
successes = 0
for _ in range(trials):
    if utils.chance(chance):
        successes += 1

print(f"Trials: {trials}, Successes: {successes}, Observed rate: {successes/trials:.6f}")
