"""
XarpScythingSims.py

Scythe-only team simulator for Xarpus.

What it does:
- Uses a 3-player team where all players use Scythe.
- Runs both loadouts:
    - OathTorvaRancour
    - TorvaRancour
- For each defense level 0..69:
    - Simulates 1000 runs
    - Each run goes to 23 attacks per player
    - From the same run, records cumulative team damage at attack checkpoints:
        19, 20, 21, 22, 23 attacks per player
- Returns threshold success metrics for total team damage at each checkpoint.

Output:
- CSV: output/XarpScythingSims_results_def0_to_69.csv
- Console summary per loadout and defense level
"""

import csv
from datetime import datetime
import os
import random
import sys

# Module-path aliasing (same pattern as existing simulation scripts)
app_dir = os.path.join(os.path.dirname(__file__), "app")
sys.path.insert(0, app_dir)

import NPC
import Player
import Stats
import Weapon

sys.modules["Monsters.NPC"] = sys.modules["NPC"]
sys.modules["Weapons.Weapon"] = sys.modules["Weapon"]
sys.modules["Weapons.Stats"] = sys.modules["Stats"]
sys.modules["Weapons.NPC"] = sys.modules["NPC"]
sys.modules["Loadouts.Stats"] = sys.modules["Stats"]
sys.modules["Loadouts.Weapon"] = sys.modules["Weapon"]
sys.modules["Loadouts.Player"] = sys.modules["Player"]

from Monsters.Xarpus import Xarpus
from Player import Player
from Weapons.Scythe import Scythe
from Loadouts.OathTorvaRancour import player as oath_torva_rancour
from Loadouts.TorvaRancour import player as torva_rancour

NUM_RUNS_PER_DEF = 1000
TEAM_SIZE = 3
DEF_LEVEL_MIN = 0
DEF_LEVEL_MAX = 69
DEF_LEVELS = list(range(DEF_LEVEL_MIN, DEF_LEVEL_MAX + 1))

ATTACK_CHECKPOINTS = [19, 20, 21, 22, 23]
MAX_ATTACKS_EACH = max(ATTACK_CHECKPOINTS)

THRESHOLDS = list(range(3000, 4001, 100))

SCYTHE = Scythe()

LOADOUTS = [
    {"label": "Torva", "player": torva_rancour},
    {"label": "Oath", "player": oath_torva_rancour},
]


def make_player(loadout_player) -> Player:
    p = Player(stats=loadout_player.stats.get_stats())
    p.equip_weapon(SCYTHE)
    return p


def run_once(defense_level: int, loadout_player):
    xarpus = Xarpus(TEAM_SIZE)
    xarpus.stats.def_level = defense_level

    team = [make_player(loadout_player) for _ in range(TEAM_SIZE)]

    total_damage = 0
    checkpoint_totals = {}

    # Round-robin attacks so each checkpoint means "attacks each".
    for attack_index in range(1, MAX_ATTACKS_EACH + 1):
        for player in team:
            hit = player.do_attack(xarpus, special_attack=False)
            xarpus.reduce_hp(hit)
            total_damage += hit

        if attack_index in ATTACK_CHECKPOINTS:
            checkpoint_totals[attack_index] = total_damage

    return checkpoint_totals


def evaluate_defense(defense_level: int, loadout_player):
    totals_by_checkpoint = {c: [] for c in ATTACK_CHECKPOINTS}
    for _ in range(NUM_RUNS_PER_DEF):
        run_totals = run_once(defense_level, loadout_player)
        for checkpoint in ATTACK_CHECKPOINTS:
            totals_by_checkpoint[checkpoint].append(run_totals[checkpoint])

    rows = []

    for checkpoint in ATTACK_CHECKPOINTS:
        totals = totals_by_checkpoint[checkpoint]
        for threshold in THRESHOLDS:
            success_count = sum(1 for dmg in totals if dmg >= threshold)
            success_pct = (success_count / NUM_RUNS_PER_DEF) * 100.0
            rows.append(
                {
                    "def_level": defense_level,
                    "attacks_each": checkpoint,
                    "threshold_damage": threshold,
                    "successful_runs": success_count,
                    "success_pct": success_pct,
                }
            )

    return rows


def save_csv(rows, file_path: str):
    # Wide format: one row per (loadout, def_level, attacks_each),
    # with threshold metrics in separate columns for easier charting.
    grouped = {}
    for row in rows:
        key = (row["loadout"], row["def_level"], row["attacks_each"])
        if key not in grouped:
            grouped[key] = {}
        grouped[key][row["threshold_damage"]] = {
            "successful_runs": row["successful_runs"],
            "success_pct": row["success_pct"],
        }

    header = ["loadout", "def_level", "attacks_each"]
    for threshold in THRESHOLDS:
        header.append(f"ge_{threshold}_runs")
        header.append(f"ge_{threshold}_pct")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        sort_loadout_order = {cfg["label"]: i for i, cfg in enumerate(LOADOUTS)}
        sorted_keys = sorted(
            grouped.keys(),
            key=lambda k: (k[1], sort_loadout_order.get(k[0], 999), k[2]),
        )

        for loadout, def_level, attacks_each in sorted_keys:
            per_threshold = grouped[(loadout, def_level, attacks_each)]
            csv_row = [loadout, def_level, attacks_each]
            for threshold in THRESHOLDS:
                metrics = per_threshold.get(threshold, {"successful_runs": 0, "success_pct": 0.0})
                csv_row.append(metrics["successful_runs"])
                csv_row.append(f"{metrics['success_pct']:.4f}")
            writer.writerow(csv_row)


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "XarpScythingSims_results_def0_to_69.csv")

    all_rows = []

    print("=" * 88)
    print("XARP SCYTHING SIMS")
    print("=" * 88)
    print(f"Runs per defense level: {NUM_RUNS_PER_DEF}")
    print(f"Team: Scythe + Scythe + Scythe ({TEAM_SIZE} players)")
    print(f"Attacks per player per run: fixed to {MAX_ATTACKS_EACH}")
    print("Checkpoint reporting at attacks each: " + ", ".join(str(c) for c in ATTACK_CHECKPOINTS))
    print(f"Defense levels: {DEF_LEVEL_MIN}..{DEF_LEVEL_MAX}")
    print(f"Thresholds: {', '.join(str(t) for t in THRESHOLDS)}")

    print()
    print("Results by defense level (alternating Torva/Oath):")
    for def_level in DEF_LEVELS:
        for loadout in LOADOUTS:
            label = loadout["label"]
            loadout_player = loadout["player"]

            rows = evaluate_defense(def_level, loadout_player)
            for row in rows:
                row["loadout"] = label
                all_rows.append(row)

            checkpoint_parts = []
            for checkpoint in ATTACK_CHECKPOINTS:
                threshold_rows = [r for r in rows if r["attacks_each"] == checkpoint]
                threshold_text = ", ".join(
                    f"{r['threshold_damage']} -> {r['successful_runs']:>4} ({r['success_pct']:>6.2f}%)"
                    for r in threshold_rows
                )
                checkpoint_parts.append(f"{checkpoint}ea: {threshold_text}")

            print(f"def {def_level:>2}: {label}: " + " | ".join(checkpoint_parts))

    final_csv_path = csv_path
    try:
        save_csv(all_rows, csv_path)
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_csv_path = os.path.join(out_dir, f"XarpScythingSims_results_def0_to_69_{timestamp}.csv")
        save_csv(all_rows, final_csv_path)

    print()
    print(f"CSV saved: {final_csv_path}")


if __name__ == "__main__":
    main()
