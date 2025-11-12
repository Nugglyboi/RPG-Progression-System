import csv
from collections import defaultdict

INPUT = "data/output.csv"

def parse_bool(v: str) -> bool:
    if v is None:
        return False
    v = v.strip()
    if v == "":
        return False
    return v.lower() in ("true", "1", "t", "yes")


def safe_float(v: str, default=0.0):
    try:
        return float(v)
    except Exception:
        return default


def analyze():
    with open(INPUT, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        combat_groups = defaultdict(lambda: [0,0])  # chance_str -> [count, successes]
        nc_groups = defaultdict(lambda: [0,0])
        combat_total_count = 0
        combat_total_success = 0
        nc_total_count = 0
        nc_total_success = 0

        for row in reader:
            # header uses 'Success?' for the boolean
            success = parse_bool(row.get('Success?') or row.get('Success') or '')
            sc_combat = safe_float(row.get('SuccessChanceCombat', '') or 0.0)
            sc_nc = safe_float(row.get('SuccessChance_NonCombat', '') or 0.0)

            # treat as combat if SuccessChanceCombat > 0 (or non-zero string)
            if sc_combat > 0.0:
                key = f"{sc_combat:.4f}"
                combat_groups[key][0] += 1
                combat_groups[key][1] += 1 if success else 0
                combat_total_count += 1
                combat_total_success += 1 if success else 0
            # otherwise if non-combat chance present
            elif sc_nc > 0.0:
                key = f"{sc_nc:.4f}"
                nc_groups[key][0] += 1
                nc_groups[key][1] += 1 if success else 0
                nc_total_count += 1
                nc_total_success += 1 if success else 0
            else:
                # neither chance present (likely rows where both chances are 0.00) - ignore
                continue

    def print_summary(title, groups, total_count, total_success):
        print(f"\n== {title} ==")
        if total_count == 0:
            print("No rows")
            return
        print(f"Rows: {total_count}, successes: {total_success}, observed rate: {total_success/total_count:.4f}")
        # convert groups to list of (chance, count, successes, observed, diff)
        rows = []
        for chance_str, (cnt, succ) in groups.items():
            chance = float(chance_str)
            obs = succ / cnt if cnt else 0.0
            rows.append((chance, cnt, succ, obs, obs - chance))
        # sort by count desc
        rows.sort(key=lambda x: x[1], reverse=True)

        print('\nTop chance groups (chance, count, successes, observed, obs-expected):')
        print(f"{'chance':>8} {'count':>8} {'succ':>8} {'observed':>10} {'diff':>10}")
        for chance, cnt, succ, obs, diff in rows[:20]:
            print(f"{chance:8.4f} {cnt:8d} {succ:8d} {obs:10.4f} {diff:10.4f}")

    print_summary('Combat', combat_groups, combat_total_count, combat_total_success)
    print_summary('Non-combat', nc_groups, nc_total_count, nc_total_success)

if __name__ == '__main__':
    analyze()
