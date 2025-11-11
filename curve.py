import matplotlib.pyplot as plt
import csv
from pathlib import Path


def load_curve_data():
    """Load success chance curves from Curve.csv"""
    curve_file = Path("data") / "Curve.csv"
    
    deltas = []
    nc_chances = []
    combat_chances = []
    
    with open(curve_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip all keys and values to handle spacing issues
            row = {k.strip(): v.strip() for k, v in row.items()}
            
            delta = float(row['Delta'])
            nc_chance = float(row['NC_Chance'])
            combat_chance = float(row['Combat_Chance'])
            
            deltas.append(delta)
            nc_chances.append(nc_chance)
            combat_chances.append(combat_chance)
    
    return deltas, nc_chances, combat_chances


def load_progression_data():
    """Load XP progression from Progression.csv"""
    progression_file = Path("data") / "Progression.csv"
    
    levels = []
    xp_to_next = []
    cumulative_xp = [0]
    gold_combat = []
    gold_noncombat = []
    
    with open(progression_file, 'r') as f:
        reader = csv.DictReader(f)
        total_xp = 0
        for row in reader:
            level = int(row['Level'])
            xp = int(row['XP_to_Next'])
            gold_c = int(row['Gold_Combat'])
            gold_nc = int(row['Gold_NonCombat'])
            
            levels.append(level)
            xp_to_next.append(xp)
            total_xp += xp
            cumulative_xp.append(total_xp)
            gold_combat.append(gold_c)
            gold_noncombat.append(gold_nc)
    
    return levels, xp_to_next, cumulative_xp, gold_combat, gold_noncombat


def plot_success_curves():
    """Plot combat and non-combat success chance curves"""
    deltas, nc_chances, combat_chances = load_curve_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Combined success curves
    ax1.plot(deltas, combat_chances, 'r-', linewidth=2, label='Combat Success', marker='o', markersize=3)
    ax1.plot(deltas, nc_chances, 'b-', linewidth=2, label='Non-Combat Success', marker='s', markersize=3)
    ax1.axhline(y=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='50% Success')
    ax1.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Even Power')
    ax1.axhline(y=0.05, color='orange', linestyle=':', linewidth=1, alpha=0.5, label='Floor (5%)')
    ax1.axhline(y=0.95, color='green', linestyle=':', linewidth=1, alpha=0.5, label='Cap (95%)')
    
    ax1.set_xlabel('Power Delta (Player - Zone)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Success Chance', fontsize=11, fontweight='bold')
    ax1.set_title('Success Chance vs Power Delta', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='best', fontsize=9)
    ax1.set_ylim(-0.05, 1.05)
    
    # Add annotations
    ax1.annotate('Player Weaker', xy=(-5, 0.1), fontsize=9, ha='center', style='italic', color='red')
    ax1.annotate('Player Stronger', xy=(5, 0.9), fontsize=9, ha='center', style='italic', color='green')
    
    # Plot 2: Difference between combat and non-combat
    difference = [nc - c for nc, c in zip(nc_chances, combat_chances)]
    ax2.plot(deltas, difference, 'purple', linewidth=2, marker='d', markersize=3)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    ax2.set_xlabel('Power Delta (Player - Zone)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('NC Success - Combat Success', fontsize=11, fontweight='bold')
    ax2.set_title('Non-Combat Advantage Over Combat', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.fill_between(deltas, 0, difference, where=[d > 0 for d in difference], 
                     alpha=0.3, color='green', label='NC Easier')
    ax2.fill_between(deltas, 0, difference, where=[d < 0 for d in difference], 
                     alpha=0.3, color='red', label='Combat Easier')
    ax2.legend(loc='best', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('success_curves.png', dpi=300, bbox_inches='tight')
    print("[OK] Saved: success_curves.png")
    plt.show()


def plot_xp_progression():
    """Plot XP progression curves"""
    levels, xp_to_next, cumulative_xp, gold_combat, gold_noncombat = load_progression_data()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: XP Required per Level
    ax1.bar(levels, xp_to_next, color='steelblue', edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('Level', fontsize=11, fontweight='bold')
    ax1.set_ylabel('XP Required to Next Level', fontsize=11, fontweight='bold')
    ax1.set_title('XP Required Per Level', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Plot 2: Cumulative XP
    ax2.plot(levels, cumulative_xp[1:], 'o-', color='darkgreen', linewidth=2, markersize=5)
    ax2.fill_between(levels, 0, cumulative_xp[1:], alpha=0.3, color='green')
    ax2.set_xlabel('Level', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Cumulative XP', fontsize=11, fontweight='bold')
    ax2.set_title('Total XP to Reach Level', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # Add annotation for total XP at max level
    max_xp = cumulative_xp[-1]
    ax2.annotate(f'Max XP: {max_xp:,}', 
                xy=(levels[-1], max_xp), 
                xytext=(levels[-1]-3, max_xp*0.8),
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', lw=1.5))
    
    # Plot 3: XP Growth Rate
    xp_growth = [xp_to_next[i] - xp_to_next[i-1] if i > 0 else 0 for i in range(len(xp_to_next))]
    ax3.plot(levels, xp_growth, 's-', color='darkorange', linewidth=2, markersize=5)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.set_xlabel('Level', fontsize=11, fontweight='bold')
    ax3.set_ylabel('XP Increase from Previous Level', fontsize=11, fontweight='bold')
    ax3.set_title('XP Growth Rate (Difficulty Scaling)', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3, linestyle='--')
    
    # Plot 4: Gold Rewards
    x_positions = range(1, len(levels) + 1)
    width = 0.35
    ax4.bar([x - width/2 for x in x_positions], gold_combat, width, 
            label='Combat Gold', color='crimson', alpha=0.7, edgecolor='darkred')
    ax4.bar([x + width/2 for x in x_positions], gold_noncombat, width, 
            label='Non-Combat Gold', color='royalblue', alpha=0.7, edgecolor='darkblue')
    ax4.set_xlabel('Level', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Gold Reward', fontsize=11, fontweight='bold')
    ax4.set_title('Gold Rewards by Encounter Type', fontsize=13, fontweight='bold')
    ax4.set_xticks(x_positions)
    ax4.set_xticklabels(levels)
    ax4.legend(loc='best', fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    plt.tight_layout()
    plt.savefig('xp_progression.png', dpi=300, bbox_inches='tight')
    print("[OK] Saved: xp_progression.png")
    plt.show()


def plot_all():
    """Generate all progression curve visualizations"""
    print("\n" + "="*50)
    print("  RPG PROGRESSION SYSTEM - CURVE VISUALIZATION")
    print("="*50 + "\n")
    
    print("Generating success curve graphs...")
    plot_success_curves()
    
    print("\nGenerating XP progression graphs...")
    plot_xp_progression()
    
    print("\n" + "="*50)
    print("  All visualizations complete!")
    print("="*50 + "\n")


if __name__ == "__main__":
    plot_all()

