import simulate
import inputs

if __name__ == "__main__":
    simulate.simulate(inputs.TURNS)
    print("Simulation complete.")
    exec(open("curve.py").read())