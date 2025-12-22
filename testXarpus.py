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
player1_sfrz.equip_weapon(eldermaul)
player2_rdps = Player(stats=oath_torva_rancour.stats.get_stats())
player2_rdps.equip_weapon(eldermaul)
player3_mdps = Player(stats=oath_torva_rancour.stats.get_stats())
player3_mdps.equip_weapon(eldermaul)
player4_nrfz = Player(stats=oath_torva_rancour.stats.get_stats())
player4_nrfz.equip_weapon(eldermaul)
player5_mdps = Player(stats=oath_torva_rancour.stats.get_stats())
player5_mdps.equip_weapon(eldermaul)

players_bgs = [
    ("1sfrz", player1_sfrz),
    ("2rdps", player2_rdps),
    ("3mdps", player3_mdps),
    ("4nrfz", player4_nrfz),
    ("5mdps", player5_mdps)
]

xarpus = Xarpus(number_of_players)

print(f"Starting defense level: {int(xarpus.stats.def_level)}")

# Each player does one Elder Maul spec
print("\nElder Maul specs:")
for name, player in players_bgs:
    hit = player.do_attack(xarpus, special_attack=True)
    xarpus.reduce_hp(hit)
    print(f"{name} Elder Maul spec: {hit}")

print(f"Defense after Elder Maul specs: {int(xarpus.stats.def_level)}")

# Each player does one BGS spec
print("\nBGS specs:")
for name, player in players_bgs:
    player.equip_weapon(bgs)
    hit = player.do_attack(xarpus, special_attack=True)
    xarpus.reduce_hp(hit)
    print(f"{name} BGS spec: {hit}")

print(f"Defense after BGS specs: {int(xarpus.stats.def_level)}")

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
    # Spec time: 6 ticks for Elder Maul + 6 ticks for BGS = 12 ticks
    spec_ticks = 12
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

