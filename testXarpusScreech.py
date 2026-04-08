import sys
import os

# Add the app directory to the Python path FIRST
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Pre-load the correct modules and create aliases in sys.modules
import NPC
import Weapon
import Stats
import Player

sys.modules['Monsters.NPC'] = sys.modules['NPC']
sys.modules['Weapons.Weapon'] = sys.modules['Weapon']
sys.modules['Weapons.Stats'] = sys.modules['Stats']
sys.modules['Weapons.NPC'] = sys.modules['NPC']
sys.modules['Loadouts.Stats'] = sys.modules['Stats']
sys.modules['Loadouts.Weapon'] = sys.modules['Weapon']
sys.modules['Loadouts.Player'] = sys.modules['Player']

from Monsters.Xarpus import Xarpus
from Player import Player
from Weapons.CrystalHalberd import CrystalHalberd
from Weapons.Scythe import Scythe
from Loadouts.OathTorvaRancour import player as oath_torva_rancour

chally = CrystalHalberd()
scythe = Scythe()

num_runs = 1000
default_percentiles = [50, 40, 30, 20, 10, 5]
starting_hp = 600


def run_simulation(team_size, weapon, use_spec):
    total_damages = []
    print(f"Running {num_runs} iterations of {team_size} players using {weapon.name}...")
    print("(0% progress) ", end="", flush=True)

    base_hp = Xarpus(team_size).stats.hp_level

    for run in range(num_runs):
        if (run + 1) % 100 == 0:
            print(f"\r({int((run + 1) / num_runs * 100)}% progress)", end="", flush=True)

        players = [
            Player(stats=oath_torva_rancour.stats.get_stats())
            for _ in range(team_size)
        ]

        xarpus = Xarpus(team_size)
        xarpus.stats.def_level = 0
        xarpus.current_hp = starting_hp

        total_run_damage = 0
        for player in players:
            player.equip_weapon(weapon)
            hit = player.do_attack(xarpus, special_attack=use_spec)
            total_run_damage += hit

        total_damages.append(total_run_damage)

    print("\r(100% progress)")
    print()
    return total_damages, base_hp


def print_stats(title, total_damages, base_hp, thresholds, percentiles):
    total_damages.sort()
    start_percent = (starting_hp / base_hp) * 100

    print(f"Boss starting HP: {base_hp} (100%) → {start_percent:.1f}% = {starting_hp} HP")
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)
    print(f"Total Runs: {len(total_damages)}")
    print(f"Min Damage: {min(total_damages)}")
    print(f"Max Damage: {max(total_damages)}")
    print(f"Avg Damage: {sum(total_damages) / len(total_damages):.2f}")
    print(f"Starting HP: {starting_hp}")
    print()

    print("Damage thresholds hit at least X% of the time:")
    print("-" * 80)
    for percentile in percentiles:
        index = int(len(total_damages) * (100 - percentile) / 100)
        threshold = total_damages[index]
        remaining_hp = starting_hp - threshold
        print(f"{percentile:>2}% of the time: {threshold:>3} damage or higher | Remaining HP: {remaining_hp:>4}")

    print("=" * 80)
    print()

    print("Hit count for specific damage thresholds:")
    print("-" * 80)
    for threshold in thresholds:
        count = sum(1 for d in total_damages if d >= threshold)
        percentage = (count / len(total_damages)) * 100
        print(f"{threshold}+ damage: {count:>4} times out of {len(total_damages)} ({percentage:>5.1f}%)")

    print("=" * 80)
    print()
    print()


for team_size in [5, 4, 3]:
    print(f"\n\n######## TEAM SIZE: {team_size} ########\n")

    chally_thresholds = [500, 450, 400, 350, 300, 250, 200, 150, 100]
    scythe_thresholds = [350, 300, 250, 200, 150, 100]
    percentiles = default_percentiles
    if team_size == 3:
        chally_thresholds.append(175)
        chally_thresholds.append(275)
        chally_thresholds.append(325)
        scythe_thresholds.append(175)
        scythe_thresholds.append(275)
        scythe_thresholds.append(325)
        chally_thresholds = sorted(set(chally_thresholds), reverse=True)
        scythe_thresholds = sorted(set(scythe_thresholds), reverse=True)
        percentiles = list(range(50, 0, -5))

    chally_damages, chally_base_hp = run_simulation(team_size, chally, use_spec=True)
    print_stats(
        title=f"CRYSTAL HALBERD SPEC DAMAGE STATISTICS ({num_runs} runs, {team_size}-man)",
        total_damages=chally_damages,
        base_hp=chally_base_hp,
        thresholds=chally_thresholds,
        percentiles=percentiles
    )

    scythe_damages, scythe_base_hp = run_simulation(team_size, scythe, use_spec=False)
    print_stats(
        title=f"SCYTHE HIT DAMAGE STATISTICS ({num_runs} runs, {team_size}-man)",
        total_damages=scythe_damages,
        base_hp=scythe_base_hp,
        thresholds=scythe_thresholds,
        percentiles=percentiles
    )
