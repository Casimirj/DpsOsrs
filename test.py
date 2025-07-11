

from Monsters.Bloat import Bloat
from Monsters.Sotetseg import Sotetseg
from Player import Player
from Weapons.Scythe import Scythe
from Weapons.NoxHally import NoxHally
from Weapons.Fists import Fists

from Loadouts.OathTorvaRancour import player as oath_torva_rancour
from Loadouts.OathTorvaSalve import player as oath_torva_salve


number_of_players = 3

bloat = Bloat(number_of_players)
scythe = Scythe()
nox = NoxHally()
fists = Fists()


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

player = oath_torva_rancour
# player.equip_weapon(fists)
# print(f"Player attack roll (Fists): {player.attack_roll}")
# print(f"Player Max Hit (Fists): {player.max_hit}")

# player.equip_weapon(scythe)
# print(f"Player attack roll (Scythe): {player.attack_roll}")
# print(f"Player Max Hit (Scythe): {player.max_hit}")

# player.equip_weapon(nox)
# print(f"Player attack roll (Nox): {player.attack_roll}")
# print(f"Player Max Hit (Nox): {player.max_hit}")


print()

player.equip_weapon(nox)

total_swings_per_player=0
while(bloat.is_alive()):
    total_swings_per_player += 1
    for i in range(0, number_of_players):
        hit = player.do_attack(bloat)
        # print(f"The scythe hit a {hit}")
        # print(f"Bloat has {bloat.current_hp} health!")
        bloat.reduce_hp(hit)
    if(bloat.is_dead()):
        print(f"Bloat is dead in {total_swings_per_player} hits")


print()
print()
print()
print("Now we calc it again with salve")
print()
print()
print()
bloat = Bloat(number_of_players)


# player = oath_torva_salve
# player.equip_weapon(fists)
# print(f"Player attack roll (Fists): {player.attack_roll}")
# print(f"Player Max Hit (Fists): {player.max_hit}")

# player.equip_weapon(scythe)
# print(f"Player attack roll (Scythe): {player.attack_roll}")
# print(f"Player Max Hit (Scythe): {player.max_hit}")

# player.equip_weapon(nox)
# print(f"Player attack roll (Nox): {player.attack_roll}")
# print(f"Player Max Hit (Nox): {player.max_hit}")


print()

player.equip_weapon(nox)

total_swings_per_player=0
while(bloat.is_alive()):
    total_swings_per_player += 1
    for i in range(0, number_of_players):
        hit = player.do_attack(bloat)
        # print(f"The scythe hit a {hit}")
        # print(f"Bloat has {bloat.current_hp} health!")
        bloat.reduce_hp(hit)
    if(bloat.is_dead()):
        print(f"Bloat is dead in {total_swings_per_player} hits")







# player_salve = Player(stats=input_stats, weapon=scythe, wearing_salve=True)
# print(f"Player attack roll (w/ salve): {player_salve.calc_att_roll()}")
