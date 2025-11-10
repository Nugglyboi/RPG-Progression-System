import simulate
import structs

if __name__ == "__main__":
    inputs = structs.Inputs()
    inputs.combat_chance = 100

    simulate.simulate(50, inputs)
