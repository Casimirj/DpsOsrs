"""
XarpDefEffects.py
─────────────────
3-man, one-hit-each combo simulator for selected weapons.

Weapons:
  - Dragon Claws spec
  - Scythe
  - Crystal Halberd spec
  - Dragon Dagger spec

It tests every unique 3-player weapon combination (order ignored, duplicates allowed),
runs each combo 1000 times, and reports:
  - average total team damage
  - max observed team damage
  - top 10% damage threshold (90th percentile)
  - average damage among top 10% runs
"""

import sys
import os
import csv
import math
import itertools

# ── Module-path aliasing (same pattern as XarpDefReduc.py) ───────────────────
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

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
from Weapons.Scythe import Scythe
from Weapons.DragonClaws import DragonClaws
from Weapons.CrystalHalberd import CrystalHalberd
from Weapons.DDSwAvernic import DragonDagger1 as DragonDagger
from Weapons.ElderMaul import ElderMaul
from Loadouts.OathTorvaRancour import player as oath_torva_rancour
from Loadouts.TorvaRancour import player as torva_rancour

NUM_RUNS_PER_COMBO = 1000
TEAM_SIZE = 3
DEF_LEVEL_MIN = 0
DEF_LEVEL_MAX = 69
DEF_LEVELS = list(range(DEF_LEVEL_MIN, DEF_LEVEL_MAX + 1))

scythe = Scythe()
dragonclaws = DragonClaws()
chally = CrystalHalberd()
dds = DragonDagger()
elder_maul = ElderMaul()

WEAPON_CHOICES = [
    {"key": "claws_spec", "label": "Dragon Claws Spec", "weapon": dragonclaws, "use_spec": True},
    {"key": "scythe", "label": "Scythe", "weapon": scythe, "use_spec": False},
    {"key": "chally_spec", "label": "Chally Spec", "weapon": chally, "use_spec": True},
    {"key": "dds_spec", "label": "Dragon Dagger Spec", "weapon": dds, "use_spec": True},
    {"key": "elder_maul_spec", "label": "Elder Maul Spec", "weapon": elder_maul, "use_spec": True},
]

WEAPON_BY_KEY = {w["key"]: w for w in WEAPON_CHOICES}

LOADOUT_CONFIGS = [
    {"key": "oath_torva_rancour", "label": "OathTorvaRancour", "player": oath_torva_rancour},
    {"key": "torva_rancour",      "label": "TorvaRancour",     "player": torva_rancour},
]
PRIMARY_COMBO_ORDER = [
    ("scythe", "scythe", "scythe"),
    ("chally_spec", "chally_spec", "chally_spec"),
    ("claws_spec", "claws_spec", "claws_spec"),
    ("dds_spec", "dds_spec", "dds_spec"),
    ("elder_maul_spec", "elder_maul_spec", "elder_maul_spec"),
]


def make_player(loadout_player, spec: int = 100) -> Player:
    p = Player(stats=loadout_player.stats.get_stats())
    p.current_special_attack = spec
    return p


def format_combo_label(combo_keys):
    labels = [WEAPON_BY_KEY[k]["label"] for k in combo_keys]
    return " + ".join(labels)


def combo_sort_key(combo_keys):
    combo_tuple = tuple(combo_keys)
    if combo_tuple in PRIMARY_COMBO_ORDER:
        return (0, PRIMARY_COMBO_ORDER.index(combo_tuple), format_combo_label(combo_keys))
    return (1, 0, format_combo_label(combo_keys))


def build_unique_3man_combos():
    keys = [w["key"] for w in WEAPON_CHOICES]
    combos = [
        c for c in itertools.combinations_with_replacement(keys, TEAM_SIZE)
        if not (any(k == "elder_maul_spec" for k in c) and not all(k == "elder_maul_spec" for k in c))
    ]
    return sorted(combos, key=combo_sort_key)


def run_combo_once(combo_keys, defense_level: int, loadout_player) -> int:
    xarpus = Xarpus(TEAM_SIZE)
    xarpus.stats.def_level = defense_level

    total_damage = 0
    for key in combo_keys:
        cfg = WEAPON_BY_KEY[key]
        p = make_player(loadout_player, spec=100)
        p.equip_weapon(cfg["weapon"])
        hit = p.do_attack(xarpus, special_attack=cfg["use_spec"])
        xarpus.reduce_hp(hit)
        total_damage += hit

    return total_damage


def percentile(values, pct: float):
    values = sorted(values)
    idx = math.ceil((pct / 100.0) * len(values)) - 1
    idx = min(max(idx, 0), len(values) - 1)
    return values[idx]


def evaluate_combo(combo_keys, defense_level: int, loadout_player):
    damages = [run_combo_once(combo_keys, defense_level, loadout_player) for _ in range(NUM_RUNS_PER_COMBO)]
    damages_sorted = sorted(damages)

    avg_damage = sum(damages) / len(damages)
    max_damage = max(damages)
    p90_damage = percentile(damages, 90)

    top_n = max(1, int(0.10 * len(damages_sorted)))
    top_slice = damages_sorted[-top_n:]
    avg_top10 = sum(top_slice) / len(top_slice)

    return {
        "def_level": defense_level,
        "combo": format_combo_label(combo_keys),
        "avg_damage": avg_damage,
        "max_damage": max_damage,
        "p90_damage": p90_damage,
        "avg_top10_damage": avg_top10,
    }


def save_csv(rows, file_path: str):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "def_level",
            "combo",
            "avg_damage",
            "max_damage",
            "top10_threshold_p90",
            "top10_avg_damage",
        ])
        for r in rows:
            writer.writerow([
                r["def_level"],
                r["combo"],
                f"{r['avg_damage']:.4f}",
                r["max_damage"],
                r["p90_damage"],
                f"{r['avg_top10_damage']:.4f}",
            ])


def run_loadout(loadout_cfg, combos, out_dir):
    label = loadout_cfg["label"]
    loadout_player = loadout_cfg["player"]
    csv_path = os.path.join(out_dir, f"XarpDefEffects_3man_{label}_def0_to_69.csv")

    rows = []
    total_evaluations = len(combos) * len(DEF_LEVELS)
    completed = 0

    print()
    print(f"{'=' * 92}")
    print(f"LOADOUT: {label}")
    print(f"{'=' * 92}")

    for combo_index, combo in enumerate(combos, start=1):
        print(f"Running combo {combo_index}/{len(combos)}: {format_combo_label(combo)}", flush=True)
        for def_level in DEF_LEVELS:
            rows.append(evaluate_combo(combo, def_level, loadout_player))
            completed += 1
        pct = (completed / total_evaluations) * 100
        print(f"  -> completed through def {DEF_LEVEL_MAX} ({pct:.1f}% overall)", flush=True)

    combo_labels_in_order = [format_combo_label(combo) for combo in combos]
    rows_by_combo = {lbl: [] for lbl in combo_labels_in_order}
    for row in rows:
        rows_by_combo[row["combo"]].append(row)
    for lbl in combo_labels_in_order:
        rows_by_combo[lbl].sort(key=lambda r: r["def_level"])

    save_csv(rows, csv_path)

    print()
    print(f"3-MAN COMBO DAMAGE TEST — {label} (1000 runs per unique combo per defense level)")
    print(f"Defense levels: {DEF_LEVEL_MIN}..{DEF_LEVEL_MAX}")
    print("Weapons: Dragon Claws Spec, Scythe, Chally Spec, Dragon Dagger Spec, Elder Maul Spec")
    print(f"Unique combos tested: {len(combos)}")
    print(f"Total evaluations: {len(rows)}")
    print()

    print("Results by combo across defense 0..69:")
    for combo_label in combo_labels_in_order:
        print()
        print("-" * 92)
        print(combo_label)
        print("-" * 92)
        for row in rows_by_combo[combo_label]:
            print(
                f"  def {row['def_level']:>2}: "
                f"avg {row['avg_damage']:.2f}, "
                f"max {row['max_damage']}, "
                f"top10% threshold {row['p90_damage']}, "
                f"top10% avg {row['avg_top10_damage']:.2f}"
            )

    print()
    print(f"CSV saved: {csv_path}")


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)

    combos = build_unique_3man_combos()

    for loadout_cfg in LOADOUT_CONFIGS:
        run_loadout(loadout_cfg, combos, out_dir)


if __name__ == "__main__":
    main()
