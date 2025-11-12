import simulate
import inputs

if __name__ == "__main__":
    simulate.simulate(inputs.TURNS)
    for i in range(inputs.TURNS):
        if i == inputs.TURNS - 1:
            print("Simulation complete.")
            exec(open("curve.py").read())