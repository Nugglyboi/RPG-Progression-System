import sys
import pathlib
import math

# ensure repo root is on sys.path so we can import project modules when running
# this script from the tools/ folder or from the project root
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils import logistic
import params

# simple function to compute logistic with center 1

def power_ratio_chance(ratio, slope=None):
    slope = slope if slope is not None else getattr(params, 'COMBAT_SLOPE', 0.55)
    # logistic(x, L=1.0, k=..., x0=1.0)
    L = 1.0
    x0 = 1.0
    k = slope
    return L / (1 + math.exp(-k * (ratio - x0)))


if __name__ == '__main__':
    for r in [0.5, 1.0, 2.0]:
        print(f"ratio={r}: chance={power_ratio_chance(r):.4f}")
