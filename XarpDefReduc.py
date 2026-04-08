import sys
import os

# Standalone 2-hit-per-player defense-reduction simulation
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
from Weapons.Bgs import Bgs
from Weapons.ElderMaul import ElderMaul
from Weapons.DragonClaws import DragonClaws
from Loadouts.OathTorvaRancour import player as oath_torva_rancour

TEAM_SIZE = 5
NUM_RUNS = 1000
BASE_XARPUS_DEF = 250
PERCENTILES = [50, 40, 30, 20, 10, 5]
DEF_PERCENTILES = [90, 80, 70, 60, 50, 40, 30, 20, 10, 5]
DAMAGE_THRESHOLDS = [500, 450, 400, 350, 300, 250, 200, 150, 100]
DEF_THRESHOLDS = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 2: EM+EM+BGS opener, then Dragon Claws ×3 (runs for 5/4/3-man)
DAMAGE_THRESHOLDS_2 = [400, 350, 300, 250, 200, 150, 100, 50]
DEF_THRESHOLDS_2 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 3: hit 1 = 3 Elder Mauls, hit 2 = 2 BGS, rest Dragon Claws (5/4/3-man)
DAMAGE_THRESHOLDS_3 = [500, 450, 400, 350, 300, 250, 200, 150, 100]
DEF_THRESHOLDS_3 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 4: 3-man only, hit 1 = 3 Elder Mauls, hit 2 = 1 BGS, rest Dragon Claws
DAMAGE_THRESHOLDS_4 = [400, 350, 300, 250, 200, 150, 100, 50]
DEF_THRESHOLDS_4 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 5: 3-man only, hit 1 = 3 Elder Mauls, hit 2 = 3 BGS
DAMAGE_THRESHOLDS_5 = [350, 300, 250, 200, 150, 100, 50]
DEF_THRESHOLDS_5 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 6/7: 3-man only, P1 starts at 75 spec; P2/P3 guaranteed EM first hit
DAMAGE_THRESHOLDS_6 = [400, 350, 300, 250, 200, 150, 100, 50]
DEF_THRESHOLDS_6 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]
DAMAGE_THRESHOLDS_7 = [400, 350, 300, 250, 200, 150, 100, 50]
DEF_THRESHOLDS_7 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 8/9: 3-man only, P1 starts at 50 spec; all 3 guaranteed EM first hit
DAMAGE_THRESHOLDS_8 = [400, 350, 300, 250, 200, 150, 100, 50]
DEF_THRESHOLDS_8 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]
DAMAGE_THRESHOLDS_9 = [400, 350, 300, 250, 200, 150, 100, 50]
DEF_THRESHOLDS_9 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 10: 3-man only, hit 1 = 2 Elder Mauls + 1 BGS, hit 2 = guaranteed 110s
DAMAGE_THRESHOLDS_10 = [600, 550, 500, 450, 400, 350, 300, 250, 200]
DEF_THRESHOLDS_10 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 11: 3-man only, hit 1 = 3 Elder Mauls, hit 2 = guaranteed 110s
DAMAGE_THRESHOLDS_11 = [650, 600, 550, 500, 450, 400, 350, 300, 250]
DEF_THRESHOLDS_11 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

# Model 12: 3-man only, hit 1 = 3 Elder Mauls, hit 2 = 2 guaranteed 110s + 1 BGS
DAMAGE_THRESHOLDS_12 = [550, 500, 450, 400, 350, 300, 250, 200, 150]
DEF_THRESHOLDS_12 = [0, 15, 30, 50, 75, 100, 125, 150, 175, 200]

scythe = Scythe()
bgs = Bgs()
eldermaul = ElderMaul()
dragonclaws = DragonClaws()


class SimPlayer:
    def __init__(self, name: str):
        self.name = name
        self.player = Player(stats=oath_torva_rancour.stats.get_stats())
        self.hits_done = 0
        self.next_tick = 0
        self.total_damage = 0


def get_attack_plan(index: int, hit_number: int):
    # hit_number is 1 or 2
    # Hit 1: players 0,1 Elder Maul spec; players 2,3,4 Dragon Claws
    # Hit 2: players 0,1 Dragon Claws; players 2,3 BGS spec; player 4 Dragon Claws
    if hit_number == 1:
        if index < 2:
            return eldermaul, True
        return dragonclaws, True

    if index in [2, 3]:
        return bgs, True
    return dragonclaws, True


def run_one_simulation():
    return run_one_simulation_model_1(TEAM_SIZE)


def run_one_simulation_model_1(team_size: int):
    xarpus = Xarpus(team_size)

    base_names = ["1sfrz", "2rdps", "3mdps", "4nrfz", "5mdps"]
    sim_players = [SimPlayer(n) for n in base_names[:team_size]]

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan(i, attack_number)

            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    return team_damage, final_def


def get_attack_plan_2(index: int, hit_number: int):
    # Model 2:
    # Hit 1: P0 Elder Maul spec, P1 Elder Maul spec, P2 BGS spec (fires 1 tick later)
    # Hit 2: All Dragon Claws spec
    if hit_number == 1:
        if index in [0, 1]:
            return eldermaul, True
        return bgs, True  # P2 fires BGS 1 tick after EM players
    return dragonclaws, True


def run_one_simulation_2(team_size: int):
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]
    # P3 (index 2) fires their first hit on tick 1 (1 tick after EM players on tick 0)
    sim_players[2].next_tick = 1

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_2(i, attack_number)

            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_3(index: int, hit_number: int, team_size: int):
    em_count = min(3, team_size)
    bgs_count = min(2, team_size)

    if hit_number == 1:
        if index < em_count:
            return eldermaul, True
        return dragonclaws, True

    if index < bgs_count:
        return bgs, True
    return dragonclaws, True


def run_one_simulation_3(team_size: int):
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    base_names = ["1sfrz", "2rdps", "3mdps", "4nrfz", "5mdps"]
    sim_players = [SimPlayer(n) for n in base_names[:team_size]]

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_3(i, attack_number, team_size)

            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def resolve_attack_choice(sim_p: SimPlayer, weapon, use_spec: bool):
    # If we planned Dragon Claws spec but don't have enough energy, use a Scythe hit instead.
    if weapon is dragonclaws and use_spec and sim_p.player.current_special_attack < dragonclaws.special_attack_cost:
        return scythe, False
    return weapon, use_spec


def attack_once(sim_p: SimPlayer, weapon, use_spec: bool, xarpus: Xarpus):
    actual_weapon, actual_use_spec = resolve_attack_choice(sim_p, weapon, use_spec)
    sim_p.player.equip_weapon(actual_weapon)
    hit = sim_p.player.do_attack(xarpus, special_attack=actual_use_spec)
    xarpus.reduce_hp(hit)
    sim_p.total_damage += hit
    sim_p.hits_done += 1
    return hit, actual_weapon


def attack_guaranteed_hit(sim_p: SimPlayer, weapon, use_spec: bool, xarpus: Xarpus):
    # Retry until non-zero hit; restore spec before each retry so only final landed spec is consumed.
    attempts = 0
    while attempts < 200:
        attempts += 1
        spec_before = sim_p.player.current_special_attack

        actual_weapon, actual_use_spec = resolve_attack_choice(sim_p, weapon, use_spec)
        sim_p.player.equip_weapon(actual_weapon)
        hit = sim_p.player.do_attack(xarpus, special_attack=actual_use_spec)

        if hit > 0:
            xarpus.reduce_hp(hit)
            sim_p.total_damage += hit
            sim_p.hits_done += 1
            return hit, actual_weapon

        sim_p.player.current_special_attack = spec_before

    # Extremely unlikely fallback
    return attack_once(sim_p, weapon, use_spec, xarpus)


def attack_fixed_damage(sim_p: SimPlayer, damage: int, xarpus: Xarpus, attack_speed: int = 5):
    xarpus.reduce_hp(damage)
    sim_p.total_damage += damage
    sim_p.hits_done += 1
    return damage, attack_speed


def get_attack_plan_4(index: int, hit_number: int):
    # 3-man only
    # Hit 1: all Elder Maul spec
    # Hit 2: P1 BGS spec, others Dragon Claws
    if hit_number == 1:
        return eldermaul, True
    if index == 0:
        return bgs, True
    return dragonclaws, True


def run_one_simulation_4():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_4(i, attack_number)

            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_5(index: int, hit_number: int):
    if hit_number == 1:
        return eldermaul, True
    return bgs, True


def run_one_simulation_5():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_5(i, attack_number)

            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_6(index: int, hit_number: int):
    # P1 starts with 75 spec.
    # Hit 1: P2/P3 Elder Maul (guaranteed to hit), P1 Dragon Claws.
    # Hit 2: P2/P3 BGS, P1 Dragon Claws.
    if hit_number == 1:
        if index in [1, 2]:
            return eldermaul, True
        return dragonclaws, True
    if index in [1, 2]:
        return bgs, True
    return dragonclaws, True


def run_one_simulation_6():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    # One player starts at 75% special.
    sim_players[0].player.current_special_attack = 75

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_6(i, attack_number)

            if attack_number == 1 and i in [1, 2] and weapon is eldermaul:
                _, used_weapon = attack_guaranteed_hit(sim_p, weapon, use_spec, xarpus)
            else:
                _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_7(index: int, hit_number: int):
    # Same as model 6, but only one BGS on hit 2.
    if hit_number == 1:
        if index in [1, 2]:
            return eldermaul, True
        return dragonclaws, True
    if index == 1:
        return bgs, True
    return dragonclaws, True


def run_one_simulation_7():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    sim_players[0].player.current_special_attack = 75

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_7(i, attack_number)

            if attack_number == 1 and i in [1, 2] and weapon is eldermaul:
                _, used_weapon = attack_guaranteed_hit(sim_p, weapon, use_spec, xarpus)
            else:
                _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_8(index: int, hit_number: int):
    # P1 starts with 50 spec.
    # Hit 1: all 3 Elder Maul (guaranteed to hit)
    # Hit 2: P2 BGS, others Dragon Claws
    if hit_number == 1:
        return eldermaul, True
    if index == 1:
        return bgs, True
    return dragonclaws, True


def run_one_simulation_8():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    sim_players[0].player.current_special_attack = 50

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_8(i, attack_number)

            if attack_number == 1 and weapon is eldermaul:
                _, used_weapon = attack_guaranteed_hit(sim_p, weapon, use_spec, xarpus)
            else:
                _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_9(index: int, hit_number: int):
    # Same as model 8 except 2 BGS on hit 2.
    if hit_number == 1:
        return eldermaul, True
    if index in [1, 2]:
        return bgs, True
    return dragonclaws, True


def run_one_simulation_9():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    sim_players[0].player.current_special_attack = 50

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1
            weapon, use_spec = get_attack_plan_9(i, attack_number)

            if attack_number == 1 and weapon is eldermaul:
                _, used_weapon = attack_guaranteed_hit(sim_p, weapon, use_spec, xarpus)
            else:
                _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_10(index: int, hit_number: int):
    # 3-man only.
    # Hit 1: P1/P2 Elder Maul spec, P3 BGS spec.
    # Hit 2: all players guaranteed 110-damage ZCB-style spec hits on a 5-tick weapon.
    if hit_number == 1:
        if index in [0, 1]:
            return eldermaul, True
        return bgs, True
    return None, False


def run_one_simulation_10():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1

            if attack_number == 2:
                _, used_speed = attack_fixed_damage(sim_p, 110, xarpus, attack_speed=5)
                if sim_p.hits_done < 2:
                    sim_p.next_tick = current_tick + used_speed
                continue

            weapon, use_spec = get_attack_plan_10(i, attack_number)
            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_11(index: int, hit_number: int):
    # 3-man only.
    # Hit 1: all 3 players Elder Maul spec.
    # Hit 2: all players guaranteed 110-damage ZCB-style spec hits on a 5-tick weapon.
    if hit_number == 1:
        return eldermaul, True
    return None, False


def run_one_simulation_11():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1

            if attack_number == 2:
                _, used_speed = attack_fixed_damage(sim_p, 110, xarpus, attack_speed=5)
                if sim_p.hits_done < 2:
                    sim_p.next_tick = current_tick + used_speed
                continue

            weapon, use_spec = get_attack_plan_11(i, attack_number)
            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def get_attack_plan_12(index: int, hit_number: int):
    # 3-man only.
    # Hit 1: all 3 players Elder Maul spec.
    # Hit 2: P1 BGS spec, P2/P3 guaranteed 110-damage ZCB-style specs.
    if hit_number == 1:
        return eldermaul, True
    if index == 0:
        return bgs, True
    return None, False


def run_one_simulation_12():
    team_size = 3
    xarpus = Xarpus(team_size)
    max_hp = xarpus.stats.hp_level

    sim_players = [
        SimPlayer("1sfrz"),
        SimPlayer("2rdps"),
        SimPlayer("3mdps"),
    ]

    while any(p.hits_done < 2 for p in sim_players):
        current_tick = min(p.next_tick for p in sim_players if p.hits_done < 2)

        for i, sim_p in enumerate(sim_players):
            if sim_p.hits_done >= 2 or sim_p.next_tick != current_tick:
                continue

            attack_number = sim_p.hits_done + 1

            if attack_number == 2 and i in [1, 2]:
                _, used_speed = attack_fixed_damage(sim_p, 110, xarpus, attack_speed=5)
                if sim_p.hits_done < 2:
                    sim_p.next_tick = current_tick + used_speed
                continue

            weapon, use_spec = get_attack_plan_12(i, attack_number)
            _, used_weapon = attack_once(sim_p, weapon, use_spec, xarpus)

            if sim_p.hits_done < 2:
                sim_p.next_tick = current_tick + used_weapon.attack_speed

    team_damage = sum(p.total_damage for p in sim_players)
    final_def = int(xarpus.stats.def_level)
    remaining_hp = max(0, xarpus.current_hp)
    return team_damage, final_def, max_hp, remaining_hp


def percentile_threshold(values, pct):
    idx = int(len(values) * (100 - pct) / 100)
    idx = min(max(idx, 0), len(values) - 1)
    return values[idx]


def build_method_row(name: str, def_specs: int, damages, defs):
    def15_count = sum(1 for d in defs if d <= 15)
    def30_count = sum(1 for d in defs if d <= 30)
    avg_ending_def = sum(defs) / len(defs)
    return {
        "name": name,
        "def_specs": def_specs,
        "def15_count": def15_count,
        "def15_rate": (def15_count / NUM_RUNS) * 100,
        "def30_count": def30_count,
        "def30_rate": (def30_count / NUM_RUNS) * 100,
        "avg_damage": sum(damages) / len(damages),
        "max_damage": max(damages),
        "avg_ending_def": avg_ending_def,
        "avg_def_reduction": BASE_XARPUS_DEF - avg_ending_def,
    }


def elder_maul_landing_effects(start_def: int = BASE_XARPUS_DEF, hits: int = 3):
    rows = []
    current_def = start_def
    for landed_hits in range(1, hits + 1):
        hit_reduction = int(current_def * 0.35)
        current_def = max(current_def - hit_reduction, 0)
        total_reduction = start_def - current_def
        rows.append({
            "landed_hits": landed_hits,
            "hit_reduction": hit_reduction,
            "ending_def": current_def,
            "total_reduction": total_reduction,
            "reduction_rate": (total_reduction / start_def) * 100,
        })
    return rows


def main():
    team_damages = []
    ending_defs = []
    model1_3_results = {"damages": [], "defs": []}

    # Model 2: collect results per team size
    model2_results = {}  # team_size -> {damages, defs, remaining_hps, max_hp}
    model3_results = {}  # team_size -> {damages, defs, remaining_hps, max_hp}
    model4_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model5_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model6_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model7_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model8_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model9_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model10_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model11_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    model12_results = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
    for ts in [5, 4, 3]:
        model2_results[ts] = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}
        model3_results[ts] = {"damages": [], "defs": [], "remaining_hps": [], "max_hp": 0}

    print(f"Running {NUM_RUNS} simulations (model 1: {TEAM_SIZE}-man, model 2/3: 5/4/3-man, model 4/5/6/7/8/9/10/11/12: 3-man)...")
    print("(0% progress)", end="", flush=True)

    for run in range(NUM_RUNS):
        dmg, final_def = run_one_simulation()
        team_damages.append(dmg)
        ending_defs.append(final_def)

        dmg1_3, final_def1_3 = run_one_simulation_model_1(3)
        model1_3_results["damages"].append(dmg1_3)
        model1_3_results["defs"].append(final_def1_3)

        for ts in [5, 4, 3]:
            dmg2, final_def2, max_hp2, rem_hp2 = run_one_simulation_2(ts)
            model2_results[ts]["damages"].append(dmg2)
            model2_results[ts]["defs"].append(final_def2)
            model2_results[ts]["remaining_hps"].append(rem_hp2)
            model2_results[ts]["max_hp"] = max_hp2

            dmg3, final_def3, max_hp3, rem_hp3 = run_one_simulation_3(ts)
            model3_results[ts]["damages"].append(dmg3)
            model3_results[ts]["defs"].append(final_def3)
            model3_results[ts]["remaining_hps"].append(rem_hp3)
            model3_results[ts]["max_hp"] = max_hp3

        dmg4, final_def4, max_hp4, rem_hp4 = run_one_simulation_4()
        model4_results["damages"].append(dmg4)
        model4_results["defs"].append(final_def4)
        model4_results["remaining_hps"].append(rem_hp4)
        model4_results["max_hp"] = max_hp4

        dmg5, final_def5, max_hp5, rem_hp5 = run_one_simulation_5()
        model5_results["damages"].append(dmg5)
        model5_results["defs"].append(final_def5)
        model5_results["remaining_hps"].append(rem_hp5)
        model5_results["max_hp"] = max_hp5

        dmg6, final_def6, max_hp6, rem_hp6 = run_one_simulation_6()
        model6_results["damages"].append(dmg6)
        model6_results["defs"].append(final_def6)
        model6_results["remaining_hps"].append(rem_hp6)
        model6_results["max_hp"] = max_hp6

        dmg7, final_def7, max_hp7, rem_hp7 = run_one_simulation_7()
        model7_results["damages"].append(dmg7)
        model7_results["defs"].append(final_def7)
        model7_results["remaining_hps"].append(rem_hp7)
        model7_results["max_hp"] = max_hp7

        dmg8, final_def8, max_hp8, rem_hp8 = run_one_simulation_8()
        model8_results["damages"].append(dmg8)
        model8_results["defs"].append(final_def8)
        model8_results["remaining_hps"].append(rem_hp8)
        model8_results["max_hp"] = max_hp8

        dmg9, final_def9, max_hp9, rem_hp9 = run_one_simulation_9()
        model9_results["damages"].append(dmg9)
        model9_results["defs"].append(final_def9)
        model9_results["remaining_hps"].append(rem_hp9)
        model9_results["max_hp"] = max_hp9

        dmg10, final_def10, max_hp10, rem_hp10 = run_one_simulation_10()
        model10_results["damages"].append(dmg10)
        model10_results["defs"].append(final_def10)
        model10_results["remaining_hps"].append(rem_hp10)
        model10_results["max_hp"] = max_hp10

        dmg11, final_def11, max_hp11, rem_hp11 = run_one_simulation_11()
        model11_results["damages"].append(dmg11)
        model11_results["defs"].append(final_def11)
        model11_results["remaining_hps"].append(rem_hp11)
        model11_results["max_hp"] = max_hp11

        dmg12, final_def12, max_hp12, rem_hp12 = run_one_simulation_12()
        model12_results["damages"].append(dmg12)
        model12_results["defs"].append(final_def12)
        model12_results["remaining_hps"].append(rem_hp12)
        model12_results["max_hp"] = max_hp12

        if (run + 1) % 100 == 0:
            pct = int((run + 1) / NUM_RUNS * 100)
            print(f"\r({pct}% progress)", end="", flush=True)

    print("\r(100% progress)")
    print()

    team_damages.sort()
    ending_defs.sort()

    print("=" * 88)
    print("XARPUS DEF REDUCTION TEST: EXACTLY 2 HITS PER PLAYER (TICK-BASED)")
    print("=" * 88)
    print("Attack model:")
    print("- Hit 1: P1/P2 Elder Maul spec, P3/P4/P5 Dragon Claws")
    print("- Hit 2: P1/P2 Dragon Claws, P3/P4 BGS spec, P5 Dragon Claws")
    print("- Tick engine: each player's next hit is scheduled by the speed of the weapon used")
    print()

    print("Team total damage after all 10 hits (2 each):")
    print(f"- Min: {min(team_damages)}")
    print(f"- Max: {max(team_damages)}")
    print(f"- Avg: {sum(team_damages) / len(team_damages):.2f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(team_damages, p)
        print(f"- {p:>2}% of runs: {t}+ team damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS:
        count = sum(1 for d in team_damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print("Ending Xarpus defense after all 10 hits:")
    print(f"- Min ending defense: {min(ending_defs)}")
    print(f"- Max ending defense: {max(ending_defs)}")
    print(f"- Avg ending defense: {sum(ending_defs) / len(ending_defs):.2f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(ending_defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS:
        count = sum(1 for d in ending_defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    # ── Model 2 output — loop over team sizes ───────────────────────────────────
    print("=" * 88)
    print("ATTACK MODEL 2: EM + EM + BGS opener, then Dragon Claws ×3  (5/4/3-man)")
    print("=" * 88)
    print("Attack model:")
    print("- Tick 1: P1/P2 Elder Maul spec")
    print("- Tick 2: P3 BGS spec")
    print("- Next available tick per player: Dragon Claws spec")
    print("  (P1+P2 claws on tick 7 [0+6+1], P3 claws on tick 8 [1+6+1])")
    print()

    for ts in [5, 4, 3]:
        r = model2_results[ts]
        damages = sorted(r["damages"])
        defs = sorted(r["defs"])
        rem_hps = sorted(r["remaining_hps"])
        max_hp = r["max_hp"]

        print(f"{'─' * 60}")
        print(f"  {ts}-MAN  (Xarpus HP: {max_hp})")
        print(f"{'─' * 60}")

        print("Team total damage after all 6 hits (2 each):")
        avg_dmg = sum(damages) / len(damages)
        print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
        print()

        print("Damage percentile thresholds:")
        for p in PERCENTILES:
            t = percentile_threshold(damages, p)
            print(f"- {p:>2}% of runs: {t}+ damage")
        print()

        print("Damage threshold hit rates:")
        for threshold in DAMAGE_THRESHOLDS_2:
            count = sum(1 for d in damages if d >= threshold)
            rate = (count / NUM_RUNS) * 100
            print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
        print()

        print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
        avg_rem = sum(rem_hps) / len(rem_hps)
        print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
        print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
        print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
        print()

        print("Ending Xarpus defense after all 6 hits:")
        avg_def = sum(defs) / len(defs)
        print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
        print()

        print("Ending defense percentile thresholds (lower is better):")
        for p in DEF_PERCENTILES:
            t = percentile_threshold(defs, p)
            print(f"- {p:>2}% of runs: ending defense <= {t}")
        print()

        print("Defense reduction hit rates:")
        for threshold in DEF_THRESHOLDS_2:
            count = sum(1 for d in defs if d <= threshold)
            rate = (count / NUM_RUNS) * 100
            print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
        print()

    # ── Model 3 output — loop over team sizes ───────────────────────────────────
    print("=" * 88)
    print("ATTACK MODEL 3: hit 1 = 3 Elder Mauls, hit 2 = 2 BGS, rest Dragon Claws")
    print("=" * 88)
    print("Attack model:")
    print("- Hit 1: first 3 players Elder Maul spec, remaining players Dragon Claws spec")
    print("- Hit 2: first 2 players BGS spec, remaining players Dragon Claws spec")
    print()

    for ts in [5, 4, 3]:
        r = model3_results[ts]
        damages = sorted(r["damages"])
        defs = sorted(r["defs"])
        rem_hps = sorted(r["remaining_hps"])
        max_hp = r["max_hp"]

        print(f"{'─' * 60}")
        print(f"  {ts}-MAN  (Xarpus HP: {max_hp})")
        print(f"{'─' * 60}")

        print(f"Team total damage after all {ts * 2} hits (2 each):")
        avg_dmg = sum(damages) / len(damages)
        print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
        print()

        print("Damage percentile thresholds:")
        for p in PERCENTILES:
            t = percentile_threshold(damages, p)
            print(f"- {p:>2}% of runs: {t}+ damage")
        print()

        print("Damage threshold hit rates:")
        for threshold in DAMAGE_THRESHOLDS_3:
            count = sum(1 for d in damages if d >= threshold)
            rate = (count / NUM_RUNS) * 100
            print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
        print()

        print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
        avg_rem = sum(rem_hps) / len(rem_hps)
        print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
        print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
        print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
        print()

        print("Ending Xarpus defense after opener:")
        avg_def = sum(defs) / len(defs)
        print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
        print()

        print("Ending defense percentile thresholds (lower is better):")
        for p in DEF_PERCENTILES:
            t = percentile_threshold(defs, p)
            print(f"- {p:>2}% of runs: ending defense <= {t}")
        print()

        print("Defense reduction hit rates:")
        for threshold in DEF_THRESHOLDS_3:
            count = sum(1 for d in defs if d <= threshold)
            rate = (count / NUM_RUNS) * 100
            print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
        print()

    # ── Model 4 output — 3-man only ────────────────────────────────────────────
    damages = sorted(model4_results["damages"])
    defs = sorted(model4_results["defs"])
    rem_hps = sorted(model4_results["remaining_hps"])
    max_hp = model4_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 4: 3-MAN — hit 1 = 3 Elder Mauls, hit 2 = 1 BGS + 2 Claws")
    print("=" * 88)
    print("Attack model:")
    print("- Hit 1: all 3 players Elder Maul spec")
    print("- Hit 2: P1 BGS spec, P2/P3 Dragon Claws spec")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_4:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_4:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    # ── Model 5 output — 3-man only ────────────────────────────────────────────
    damages = sorted(model5_results["damages"])
    defs = sorted(model5_results["defs"])
    rem_hps = sorted(model5_results["remaining_hps"])
    max_hp = model5_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 5: 3-MAN — hit 1 = 3 Elder Mauls, hit 2 = 3 BGS")
    print("=" * 88)
    print("Attack model:")
    print("- Hit 1: all 3 players Elder Maul spec")
    print("- Hit 2: all 3 players BGS spec")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_5:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_5:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    # ── Model 6 output — 3-man only ────────────────────────────────────────────
    damages = sorted(model6_results["damages"])
    defs = sorted(model6_results["defs"])
    rem_hps = sorted(model6_results["remaining_hps"])
    max_hp = model6_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 6: 3-MAN — P1 starts 75 spec; P2/P3 guaranteed EM, then 2 BGS")
    print("=" * 88)
    print("Attack model:")
    print("- P1 starts at 75 spec")
    print("- Hit 1: P2/P3 guaranteed Elder Maul hits, P1 Dragon Claws")
    print("- Hit 2: P2/P3 BGS, P1 Dragon Claws")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_6:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_6:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    # ── Model 7 output — 3-man only ────────────────────────────────────────────
    damages = sorted(model7_results["damages"])
    defs = sorted(model7_results["defs"])
    rem_hps = sorted(model7_results["remaining_hps"])
    max_hp = model7_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 7: 3-MAN — P1 starts 75 spec; P2/P3 guaranteed EM, then 1 BGS")
    print("=" * 88)
    print("Attack model:")
    print("- P1 starts at 75 spec")
    print("- Hit 1: P2/P3 guaranteed Elder Maul hits, P1 Dragon Claws")
    print("- Hit 2: P2 BGS, P1/P3 Dragon Claws")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_7:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_7:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    # ── Model 8 output — 3-man only ────────────────────────────────────────────
    damages = sorted(model8_results["damages"])
    defs = sorted(model8_results["defs"])
    rem_hps = sorted(model8_results["remaining_hps"])
    max_hp = model8_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 8: 3-MAN — P1 starts 50 spec; 3 guaranteed EM, then 1 BGS")
    print("=" * 88)
    print("Attack model:")
    print("- P1 starts at 50 spec")
    print("- Hit 1: all 3 players guaranteed Elder Maul hits")
    print("- Hit 2: P2 BGS, P1/P3 Dragon Claws")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_8:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_8:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    # ── Model 9 output — 3-man only ────────────────────────────────────────────
    damages = sorted(model9_results["damages"])
    defs = sorted(model9_results["defs"])
    rem_hps = sorted(model9_results["remaining_hps"])
    max_hp = model9_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 9: 3-MAN — P1 starts 50 spec; 3 guaranteed EM, then 2 BGS")
    print("=" * 88)
    print("Attack model:")
    print("- P1 starts at 50 spec")
    print("- Hit 1: all 3 players guaranteed Elder Maul hits")
    print("- Hit 2: P2/P3 BGS, P1 Dragon Claws")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_9:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_9:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")

    # ── Model 10 output — 3-man only ───────────────────────────────────────────
    damages = sorted(model10_results["damages"])
    defs = sorted(model10_results["defs"])
    rem_hps = sorted(model10_results["remaining_hps"])
    max_hp = model10_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 10: 3-MAN — 2 EM + 1 BGS, then guaranteed 110 ZCB specs")
    print("=" * 88)
    print("Attack model:")
    print("- Hit 1: P1/P2 Elder Maul spec, P3 BGS spec")
    print("- Hit 2: all 3 players deal guaranteed 110 damage")
    print("- Second-hit timing uses a 5-tick weapon (ZCB-style spec)")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_10:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_10:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")

    # ── Model 11 output — 3-man only ───────────────────────────────────────────
    damages = sorted(model11_results["damages"])
    defs = sorted(model11_results["defs"])
    rem_hps = sorted(model11_results["remaining_hps"])
    max_hp = model11_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 11: 3-MAN — 3 EM, then guaranteed 110 ZCB specs")
    print("=" * 88)
    print("Attack model:")
    print("- Hit 1: all 3 players Elder Maul spec")
    print("- Hit 2: all 3 players deal guaranteed 110 damage")
    print("- Second-hit timing uses a 5-tick weapon (ZCB-style spec)")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_11:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_11:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")

    # ── Model 12 output — 3-man only ───────────────────────────────────────────
    damages = sorted(model12_results["damages"])
    defs = sorted(model12_results["defs"])
    rem_hps = sorted(model12_results["remaining_hps"])
    max_hp = model12_results["max_hp"]

    print("=" * 88)
    print("ATTACK MODEL 12: 3-MAN — 3 EM, then 2 guaranteed 110 ZCB specs + 1 BGS")
    print("=" * 88)
    print("Attack model:")
    print("- Hit 1: all 3 players Elder Maul spec")
    print("- Hit 2: P1 BGS spec, P2/P3 deal guaranteed 110 damage")
    print("- Guaranteed second-hit timing uses a 5-tick weapon (ZCB-style spec)")
    print()

    print("Team total damage after all 6 hits (2 each):")
    avg_dmg = sum(damages) / len(damages)
    print(f"- Min: {min(damages)}  /  Max: {max(damages)}  /  Avg: {avg_dmg:.1f}")
    print()

    print("Damage percentile thresholds:")
    for p in PERCENTILES:
        t = percentile_threshold(damages, p)
        print(f"- {p:>2}% of runs: {t}+ damage")
    print()

    print("Damage threshold hit rates:")
    for threshold in DAMAGE_THRESHOLDS_12:
        count = sum(1 for d in damages if d >= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- {threshold:>3}+ damage: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")
    print()

    print(f"Remaining Xarpus HP after opener (out of {max_hp}):")
    avg_rem = sum(rem_hps) / len(rem_hps)
    print(f"- Min remaining: {min(rem_hps)} ({min(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Max remaining: {max(rem_hps)} ({max(rem_hps)/max_hp*100:.1f}%)")
    print(f"- Avg remaining: {avg_rem:.0f} ({avg_rem/max_hp*100:.1f}%)")
    print()

    print("Ending Xarpus defense after opener:")
    avg_def = sum(defs) / len(defs)
    print(f"- Min: {min(defs)}  /  Max: {max(defs)}  /  Avg: {avg_def:.1f}")
    print()

    print("Ending defense percentile thresholds (lower is better):")
    for p in DEF_PERCENTILES:
        t = percentile_threshold(defs, p)
        print(f"- {p:>2}% of runs: ending defense <= {t}")
    print()

    print("Defense reduction hit rates:")
    for threshold in DEF_THRESHOLDS_12:
        count = sum(1 for d in defs if d <= threshold)
        rate = (count / NUM_RUNS) * 100
        print(f"- ending defense <= {threshold:>3}: {count:>4}/{NUM_RUNS} ({rate:5.1f}%)")

    # ── 3-man method comparison summary ─────────────────────────────────────────
    method_rows = []

    # Model 2 (3-man)
    m2_damages = model2_results[3]["damages"]
    m2_defs = model2_results[3]["defs"]
    method_rows.append(build_method_row("Model 2 (2 EM + 1 BGS, then claws)", 3, m2_damages, m2_defs))

    # Model 1 (3-man)
    m1_damages = model1_3_results["damages"]
    m1_defs = model1_3_results["defs"]
    method_rows.append(build_method_row("Model 1 (2 EM + 2 BGS in 5-man pattern, else claws)", 3, m1_damages, m1_defs))

    # Model 3 (3-man)
    m3_damages = model3_results[3]["damages"]
    m3_defs = model3_results[3]["defs"]
    method_rows.append(build_method_row("Model 3 (3 EM, 2 BGS, rest claws)", 5, m3_damages, m3_defs))

    # Model 4 (3-man)
    m4_damages = model4_results["damages"]
    m4_defs = model4_results["defs"]
    method_rows.append(build_method_row("Model 4 (3 EM, 1 BGS, rest claws)", 4, m4_damages, m4_defs))

    # Model 5 (3-man)
    m5_damages = model5_results["damages"]
    m5_defs = model5_results["defs"]
    method_rows.append(build_method_row("Model 5 (3 EM, 3 BGS)", 6, m5_damages, m5_defs))

    # Model 6 (3-man)
    m6_damages = model6_results["damages"]
    m6_defs = model6_results["defs"]
    method_rows.append(build_method_row("Model 6 (P1 75 spec, 2 guaranteed EM, 2 BGS, rest claws)", 4, m6_damages, m6_defs))

    # Model 7 (3-man)
    m7_damages = model7_results["damages"]
    m7_defs = model7_results["defs"]
    method_rows.append(build_method_row("Model 7 (P1 75 spec, 2 guaranteed EM, 1 BGS, rest claws)", 3, m7_damages, m7_defs))

    # Model 8 (3-man)
    m8_damages = model8_results["damages"]
    m8_defs = model8_results["defs"]
    method_rows.append(build_method_row("Model 8 (P1 50 spec, 3 guaranteed EM, 1 BGS, rest claws)", 4, m8_damages, m8_defs))

    # Model 9 (3-man)
    m9_damages = model9_results["damages"]
    m9_defs = model9_results["defs"]
    method_rows.append(build_method_row("Model 9 (P1 50 spec, 3 guaranteed EM, 2 BGS, rest claws)", 5, m9_damages, m9_defs))

    # Model 10 (3-man)
    m10_damages = model10_results["damages"]
    m10_defs = model10_results["defs"]
    method_rows.append(build_method_row("Model 10 (2 EM + 1 BGS, then 3 guaranteed 110 ZCB specs)", 3, m10_damages, m10_defs))

    # Model 11 (3-man)
    m11_damages = model11_results["damages"]
    m11_defs = model11_results["defs"]
    method_rows.append(build_method_row("Model 11 (3 EM, then 3 guaranteed 110 ZCB specs)", 3, m11_damages, m11_defs))

    # Model 12 (3-man)
    m12_damages = model12_results["damages"]
    m12_defs = model12_results["defs"]
    method_rows.append(build_method_row("Model 12 (3 EM, then 2 guaranteed 110 ZCB specs + 1 BGS)", 4, m12_damages, m12_defs))

    # Weighted ranking system:
    # 1) def<=15 rate (most important), capped at target 50% -> max 50 points
    # 2) average damage (second) -> max 35 points
    # 3) max damage (third) -> max 15 points
    DEF15_TARGET = 50.0
    DEF15_WEIGHT = 50.0
    AVG_DMG_WEIGHT = 35.0
    MAX_DMG_WEIGHT = 15.0

    avg_values = [r["avg_damage"] for r in method_rows]
    max_values = [r["max_damage"] for r in method_rows]

    avg_min, avg_max = min(avg_values), max(avg_values)
    max_min, max_max = min(max_values), max(max_values)
    avg_span = avg_max - avg_min
    max_span = max_max - max_min

    for row in method_rows:
        def15_component = (min(row["def15_rate"], DEF15_TARGET) / DEF15_TARGET) * DEF15_WEIGHT
        avg_component = ((row["avg_damage"] - avg_min) / avg_span) * AVG_DMG_WEIGHT if avg_span > 0 else AVG_DMG_WEIGHT
        max_component = ((row["max_damage"] - max_min) / max_span) * MAX_DMG_WEIGHT if max_span > 0 else MAX_DMG_WEIGHT

        row["score_def15"] = def15_component
        row["score_avg"] = avg_component
        row["score_max"] = max_component
        row["score_total"] = def15_component + avg_component + max_component

    ranked_rows = sorted(
        method_rows,
        key=lambda r: (-r["score_total"], -r["def15_rate"], -r["avg_damage"], -r["max_damage"])
    )
    best = ranked_rows[0]

    print()
    print("=" * 88)
    print("3-MAN SUMMARY: WEIGHTED METHOD RANKING")
    print("=" * 88)
    print(f"Best method: {best['name']}")
    print(f"- Weighted score: {best['score_total']:.2f} / 100")
    print(
        f"  (def<=15 score {best['score_def15']:.2f}/50, "
        f"avg dmg score {best['score_avg']:.2f}/35, "
        f"max dmg score {best['score_max']:.2f}/15)"
    )
    print(f"- Defense-reduction specs used: {best['def_specs']}")
    print(f"- Defense <= 15: {best['def15_count']}/{NUM_RUNS} ({best['def15_rate']:.1f}%)")
    print(f"- Defense <= 30: {best['def30_count']}/{NUM_RUNS} ({best['def30_rate']:.1f}%)")
    print(f"- Avg ending defense: {best['avg_ending_def']:.1f}")
    print(f"- Avg defense reduction: {best['avg_def_reduction']:.1f}")
    print(f"- Avg team damage: {best['avg_damage']:.1f}")
    print(f"- Max team damage: {best['max_damage']}")
    print()
    print("All 3-man methods:")
    for row in ranked_rows:
        print(
            f"- {row['name']}: score {row['score_total']:.2f}, "
            f"def<=15 {row['def15_count']}/{NUM_RUNS} ({row['def15_rate']:.1f}%), "
            f"def<=30 {row['def30_count']}/{NUM_RUNS} ({row['def30_rate']:.1f}%), "
            f"avg def red {row['avg_def_reduction']:.1f}, "
            f"avg dmg {row['avg_damage']:.1f}, max dmg {row['max_damage']}, def specs {row['def_specs']}"
        )

    print()
    print("=" * 88)
    print("ELDER MAUL LANDING EFFECTS")
    print("=" * 88)
    print(f"Starting Xarpus defense: {BASE_XARPUS_DEF}")
    for row in elder_maul_landing_effects():
        print(
            f"- {row['landed_hits']} Elder Maul landings: ending def {row['ending_def']}, "
            f"total reduction {row['total_reduction']} ({row['reduction_rate']:.1f}%), "
            f"last hit reduced {row['hit_reduction']}"
        )


if __name__ == "__main__":
    main()
    raise SystemExit

import sys
import os

# Add the app directory to the Python path FIRST
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Pre-load the correct modules and create aliases in sys.modules
# This ensures all submodules use the same class instances
import NPC
import Weapon
import Stats
import Player

# Create module aliases so Weapons.Weapon, Monsters.NPC, etc. all resolve to the same modules
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
from Weapons.NoxHally import NoxHally
from Weapons.Fists import Fists
from Weapons.Bgs import Bgs
from Weapons.ElderMaul import ElderMaul 
from Weapons.DragonClaws import DragonClaws



from Loadouts.OathTorvaRancour import player as oath_torva_rancour
from Loadouts.OathTorvaSalve import player as oath_torva_salve


number_of_players = 5

scythe = Scythe()
nox = NoxHally()
fists = Fists()
bgs = Bgs()
dragon_claws = DragonClaws()
eldermaul = ElderMaul()  # Assuming ElderMaul is defined somewhere



# input_stats = {
#     'hp_level': 99,
#     'attack_level': 99,
#     'strength_level': 99,
#     'def_level': 99,
#     'magic_level': 99,
#     'ranged_level': 99,
#     'prayer_level': 99,

#     'slash_attack_bonus': 0,
#     'magic_attack_bonus': 0,
#     'ranged_attack_bonus': 0,

#     'strength_bonus': 0,
#     'magic_strength_bonus': 0,
#     'ranged_strength_bonus': 0,
# }

# print(player.stats.get_stats())

# hit = player.do_attack(bloat)
# print(f"Player attack roll (Fists): {player.attack_roll}")
# print(f"Player Max Hit (Fists): {player.max_hit}")

# player.equip_weapon(scythe)
# hit = player.do_attack(bloat)
# print(f"Player attack roll (Scythe): {player.attack_roll}")
# print(f"Player Max Hit (Scythe): {player.max_hit}")

# player.equip_weapon(nox)
# hit = player.do_attack(bloat)
# print(f"Player attack roll (Nox): {player.attack_roll}")
# print(f"Player Max Hit (Nox): {player.max_hit}")




# Create individual players with names (create without weapon, then equip)
player1_sfrz = Player(stats=oath_torva_rancour.stats.get_stats())
player1_sfrz.equip_weapon(scythe)
player2_rdps = Player(stats=oath_torva_rancour.stats.get_stats())
player2_rdps.equip_weapon(scythe)
player3_mdps = Player(stats=oath_torva_rancour.stats.get_stats())
player3_mdps.equip_weapon(scythe)
player4_nrfz = Player(stats=oath_torva_rancour.stats.get_stats())
player4_nrfz.equip_weapon(scythe)
player5_mdps = Player(stats=oath_torva_rancour.stats.get_stats())
player5_mdps.equip_weapon(scythe)

'''# Debug: Check if boosts are applied 
print("Debug - Player 1 settings:")
print(f"  Super Combat: {player1_sfrz.super_combat}")
print(f"  Piety Active: {player1_sfrz.piety_active}")
print(f"  Attack Level: {player1_sfrz.stats.attack_level}")
print(f"  Strength Level: {player1_sfrz.stats.strength_level}")
print(f"  Slash Attack Bonus: {player1_sfrz.stats.slash_attack_bonus}")
print(f"  Melee Strength Bonus: {player1_sfrz.stats.melee_strength_bonus}")
'''
# Calculate and display effective levels and max hit
player1_sfrz.calc_all_the_things(player1_sfrz.weapon.attack_type)
print(f"  Effective Attack Level: {player1_sfrz.effective_att_level}")
print(f"  Effective Strength Level: {player1_sfrz.effective_str_level}")
print(f"  Max Hit: {player1_sfrz.max_hit}")
print(f"  Attack Roll: {player1_sfrz.attack_roll}")
print()

# Store players in a list with their names
players = [
    ("1sfrz", player1_sfrz),
    ("2rdps", player2_rdps),
    ("3mdps", player3_mdps),
    ("4nrfz", player4_nrfz),
    ("5mdps", player5_mdps)
]

# Initialize damage and hit tracking
damage_tracker = {name: 0 for name, _ in players}
hit_tracker = {name: 0 for name, _ in players}
successful_hits = {name: 0 for name, _ in players}

xarpus = Xarpus(number_of_players)

print()
print()
print("Your Team is now fighting Xarpus")
print("With BIS Gear and no def reduction")
print(f"Xarpus Defense Level: {xarpus.stats.def_level}")
print(f"Xarpus Slash Defense Bonus: {xarpus.stats.slash_def}")

# Calculate Xarpus's defense roll
xarpus.calc_def_roll("Slash")
print(f"Xarpus Defense Roll: {xarpus.def_roll}")
print(f"Player Attack Roll: {player1_sfrz.attack_roll}")
print(f"Hit Chance (approximate): {min(100, player1_sfrz.attack_roll / (xarpus.def_roll + player1_sfrz.attack_roll) * 100):.1f}%")
print()

total_swings_per_player=0
scythe_attack_speed = 5  # Attack speed in ticks (5 ticks = 3.0 seconds)

# Track when each player can attack next (in ticks)
player_attack_timers = {name: 0 for name, _ in players}
current_tick = 0
last_spec_regen_tick = 0

while(xarpus.is_alive()):
    # Regenerate spec energy every 50 ticks (10% per 30 seconds)
    if current_tick - last_spec_regen_tick >= 50:
        for name, player in players:
            player.current_special_attack = min(100, player.current_special_attack + 10)
        last_spec_regen_tick = current_tick
    
    # Check which players can attack on this tick
    for name, player in players:
        if player_attack_timers[name] <= current_tick:
            hit = player.do_attack(xarpus)
            damage_tracker[name] += hit
            hit_tracker[name] += 1
            if hit > 0:
                successful_hits[name] += 1
            xarpus.reduce_hp(hit)
            # Set next attack time
            player_attack_timers[name] = current_tick + scythe_attack_speed
            
            if xarpus.is_dead():
                break
    
    current_tick += 1
    
if(xarpus.is_dead()):
    # Calculate fight duration based on total ticks
    fight_duration_seconds = current_tick * 0.6
    minutes = int(fight_duration_seconds // 60)
    seconds = fight_duration_seconds % 60
    
    total_attacks = sum(hit_tracker.values())
    print(f"Xarpus is dead after {current_tick} ticks ({total_attacks} total attacks)")
    print("\nDamage and hits by each player:")
    for name, player in players:
        avg_damage = damage_tracker[name] / hit_tracker[name] if hit_tracker[name] > 0 else 0
        accuracy = (successful_hits[name] / hit_tracker[name] * 100) if hit_tracker[name] > 0 else 0
        print(f"{name}: {damage_tracker[name]} damage in {hit_tracker[name]} hits (avg: {avg_damage:.2f} per hit, {accuracy:.1f}% accuracy) - {player.current_special_attack}% spec remaining")
    
    print(f"\nFight duration: {minutes}:{seconds:05.2f} ({fight_duration_seconds:.2f} seconds)")



print()





player.equip_weapon(scythe)



print()

print("With Elder Maul and BGS")
# Re-create players for new fight
player1_sfrz = Player(stats=oath_torva_rancour.stats.get_stats())
player2_rdps = Player(stats=oath_torva_rancour.stats.get_stats())
player3_mdps = Player(stats=oath_torva_rancour.stats.get_stats())
player4_nrfz = Player(stats=oath_torva_rancour.stats.get_stats())
player5_mdps = Player(stats=oath_torva_rancour.stats.get_stats())

players_bgs = [
    ("1sfrz", player1_sfrz),
    ("2rdps", player2_rdps),
    ("3mdps", player3_mdps),
    ("4nrfz", player4_nrfz),
    ("5mdps", player5_mdps)
]

xarpus = Xarpus(number_of_players)

print(f"Starting defense level: {int(xarpus.stats.def_level)}")

# Hit 1: 2 Elder Maul specs (players 0,1), 3 Scythe hits (players 2,3,4)
print("\nHit 1 (2 Elder Maul, 3 Scythe):")
for index, (name, player) in enumerate(players_bgs):
    if index < 2:
        player.equip_weapon(eldermaul)
        hit = player.do_attack(xarpus, special_attack=True)
        attack_label = "Elder Maul spec"
    else:
        player.equip_weapon(scythe)
        hit = player.do_attack(xarpus)
        attack_label = "Scythe hit"
    xarpus.reduce_hp(hit)
    print(f"{name} {attack_label}: {hit}")

print(f"Defense after Hit 1: {int(xarpus.stats.def_level)}")

# Hit 2: 2 BGS specs (from original scythe players 2,3), 3 Scythe hits (players 0,1,4)
print("\nHit 2 (2 BGS from original Scythe, 3 Scythe):")
attack_sequence_hit2 = [
    (0, "Scythe"),   # player1_sfrz: Scythe (was Elder Maul)
    (1, "Scythe"),   # player2_rdps: Scythe (was Elder Maul)
    (2, "BGS"),      # player3_mdps: BGS spec (was Scythe)
    (3, "BGS"),      # player4_nrfz: BGS spec (was Scythe)
    (4, "Scythe"),   # player5_mdps: Scythe (was Scythe)
]
for index, (name, player) in enumerate(players_bgs):
    attack_type = attack_sequence_hit2[index][1]
    if attack_type == "BGS":
        player.equip_weapon(bgs)
        hit = player.do_attack(xarpus, special_attack=True)
    else:
        player.equip_weapon(scythe)
        hit = player.do_attack(xarpus)
    xarpus.reduce_hp(hit)
    print(f"{name} {attack_type}: {hit}")

print(f"Defense after Hit 2: {int(xarpus.stats.def_level)}")

# Hit 3: All players with 50+ spec use Dragon Claws, else Scythe
print("\nHit 3 (Dragon Claws if 50+ spec, else Scythe):")
for name, player in players_bgs:
    if player.current_special_attack >= 50:
        player.equip_weapon(dragon_claws)
        hit = player.do_attack(xarpus, special_attack=True)
        attack_label = "Dragon Claws spec"
    else:
        player.equip_weapon(scythe)
        hit = player.do_attack(xarpus)
        attack_label = "Scythe hit"
    xarpus.reduce_hp(hit)
    print(f"{name} {attack_label}: {hit}")

print(f"Defense after Hit 3: {int(xarpus.stats.def_level)}")

# Hit 4: All players with 50+ spec use Dragon Claws again, else Scythe
print("\nHit 4 (Dragon Claws if 50+ spec, else Scythe):")
for name, player in players_bgs:
    if player.current_special_attack >= 50:
        player.equip_weapon(dragon_claws)
        hit = player.do_attack(xarpus, special_attack=True)
        attack_label = "Dragon Claws spec"
    else:
        player.equip_weapon(scythe)
        hit = player.do_attack(xarpus)
        attack_label = "Scythe hit"
    xarpus.reduce_hp(hit)
    print(f"{name} {attack_label}: {hit}")

print(f"Defense after Hit 4: {int(xarpus.stats.def_level)}")

print("\nSpec remaining after opening sequence:")
for name, player in players_bgs:
    print(f"{name}: {player.current_special_attack}%")

print("\nNow switching back to Scythe")

# Debug: Check what happens with 0 defense
print(f"\nDebug - After specs:")
print(f"Xarpus Defense Level: {xarpus.stats.def_level}")
xarpus.calc_def_roll("Slash")
print(f"Xarpus Defense Roll: {xarpus.def_roll}")
player1_sfrz.equip_weapon(scythe)
player1_sfrz.calc_all_the_things(player1_sfrz.weapon.attack_type)
print(f"Player Attack Roll: {player1_sfrz.attack_roll}")
print(f"Player Max Hit: {player1_sfrz.max_hit}")
print(f"Hit Chance (approximate): {min(100, player1_sfrz.attack_roll / (xarpus.def_roll + player1_sfrz.attack_roll) * 100):.1f}%")
print()

# Initialize tracking for BGS fight
damage_tracker_bgs = {name: 0 for name, _ in players_bgs}
hit_tracker_bgs = {name: 0 for name, _ in players_bgs}
successful_hits_bgs = {name: 0 for name, _ in players_bgs}

# Switch all players to scythe
for name, player in players_bgs:
    player.equip_weapon(scythe)

# Track when each player can attack next (in ticks)
player_attack_timers_bgs = {name: 0 for name, _ in players_bgs}
current_tick = 0
last_spec_regen_tick = 0

while(xarpus.is_alive()):
    # Regenerate spec energy every 50 ticks (10% per 30 seconds)
    if current_tick - last_spec_regen_tick >= 50:
        for name, player in players_bgs:
            player.current_special_attack = min(100, player.current_special_attack + 10)
        last_spec_regen_tick = current_tick
    
    # Check which players can attack on this tick
    for name, player in players_bgs:
        if player_attack_timers_bgs[name] <= current_tick:
            hit = player.do_attack(xarpus)
            damage_tracker_bgs[name] += hit
            hit_tracker_bgs[name] += 1
            if hit > 0:
                successful_hits_bgs[name] += 1
            xarpus.reduce_hp(hit)
            # Set next attack time
            player_attack_timers_bgs[name] = current_tick + scythe_attack_speed
            
            if xarpus.is_dead():
                break
    
    current_tick += 1
    
if(xarpus.is_dead()):
    # Calculate fight duration
    # Opening time: first attack cycle + second attack cycle + Dragon Claws cycle
    spec_ticks = 18
    fight_duration_seconds = (current_tick + spec_ticks) * 0.6
    minutes = int(fight_duration_seconds // 60)
    seconds = fight_duration_seconds % 60
    
    total_attacks = sum(hit_tracker_bgs.values())
    print(f"Xarpus is dead after {current_tick} ticks ({total_attacks} total attacks)")
    print("\nDamage and hits by each player:")
    for name, player in players_bgs:
        avg_damage = damage_tracker_bgs[name] / hit_tracker_bgs[name] if hit_tracker_bgs[name] > 0 else 0
        accuracy = (successful_hits_bgs[name] / hit_tracker_bgs[name] * 100) if hit_tracker_bgs[name] > 0 else 0
        print(f"{name}: {damage_tracker_bgs[name]} damage in {hit_tracker_bgs[name]} hits (avg: {avg_damage:.2f} per hit, {accuracy:.1f}% accuracy) - {player.current_special_attack}% spec remaining")
    
    print(f"\nFight duration: {minutes}:{seconds:05.2f} ({fight_duration_seconds:.2f} seconds)")



print()
print("With Bgs and Claws")
player = oath_torva_salve
xarpus = Xarpus(number_of_players)
player.equip_weapon(bgs)
hit = player.do_attack(xarpus, special_attack=True)
xarpus.reduce_hp(hit)

print(f"Bgs hit a {hit}")

player.equip_weapon(scythe)

total_swings_per_player=0
total_claw_damage=0
total_scythe_damage=0
while(xarpus.is_alive()):
    total_swings_per_player += 1
    for i in range(0, number_of_players):
        if(total_swings_per_player in [1,2]):
            player.current_special_attack = 100
            player.equip_weapon(dragon_claws)
            hit = player.do_attack(xarpus, special_attack=True)
            # print(f"The scythe hit a {hit}")
            # print(f"Bloat has {bloat.current_hp} health!")
            xarpus.reduce_hp(hit)
            total_claw_damage += hit

        else:
            player.equip_weapon(scythe)
            hit = player.do_attack(xarpus)
            # print(f"The scythe hit a {hit}")
            # print(f"Bloat has {bloat.current_hp} health!")
            xarpus.reduce_hp(hit)
            total_scythe_damage += hit
    if(xarpus.is_dead()):
        # Calculate fight duration
        # All players spec simultaneously, so BGS = 1 attack of 6 ticks, Claws = 2 attacks of 4 ticks each
        bgs_time = 6 * 0.6  # 1 BGS spec (all players at once)
        claw_time = 2 * 4 * 0.6  # 2 rounds of claws (all players at once each round)
        scythe_swings = (total_swings_per_player - 2) * number_of_players  # Rounds 3+ only
        scythe_time = scythe_swings * scythe_attack_speed * 0.6
        total_duration = bgs_time + claw_time + scythe_time
        minutes = int(total_duration // 60)
        seconds = total_duration % 60
        
        print(f"Total Claw Damage {total_claw_damage}")
        print(f"Total Scythe Damage {total_scythe_damage}")
        print(f"Xarpus is dead in {total_swings_per_player} hits")
        print(f"\nFight duration: {minutes}:{seconds:05.2f} ({total_duration:.2f} seconds)")






# player_salve = Player(stats=input_stats, weapon=scythe, wearing_salve=True)
# print(f"Player attack roll (w/ salve): {player_salve.calc_att_roll()}")
