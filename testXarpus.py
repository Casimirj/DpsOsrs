

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




player = oath_torva_rancour
xarpus = Xarpus(number_of_players)

print()
print()
print("Your Team is now fighting Xarpus")
print("With BIS Gear and no def reduction")
player.equip_weapon(scythe)

total_swings_per_player=0

while(xarpus.is_alive()):
    total_swings_per_player += 1
    for i in range(0, number_of_players):
        hit = player.do_attack(xarpus)
        # print(f"The scythe hit a {hit}")
        # print(f"Bloat has {Xarpus.current_hp} health!")
        xarpus.reduce_hp(hit)
    if(xarpus.is_dead()):
        print(f"Xarpus is dead in {total_swings_per_player} hits")



print()





player.equip_weapon(scythe)



print()

print("With BGS")
player = oath_torva_rancour
xarpus = Xarpus(number_of_players)
player.equip_weapon(bgs)
hit = player.do_attack(xarpus, special_attack=True)
xarpus.reduce_hp(hit)


print(f"1st BGS hit a {hit}")

hit = player.do_attack(xarpus, special_attack=True)
xarpus.reduce_hp(hit)


print(f"2nd BGS hit a {hit}")
hit = player.do_attack(xarpus, special_attack=True)
xarpus.reduce_hp(hit)


print(f"3nd BGS hit a {hit}")
hit = player.do_attack(xarpus, special_attack=True)
xarpus.reduce_hp(hit)




print("Now switching back to Scythe")
player.equip_weapon(scythe)

total_swings_per_player=0
while(xarpus.is_alive()):
    total_swings_per_player += 1
    for i in range(0, number_of_players):
        hit = player.do_attack(xarpus)
        # print(f"The scythe hit a {hit}")
        # print(f"Bloat has {bloat.current_hp} health!")
        xarpus.reduce_hp(hit)
    if(xarpus.is_dead()):
        print(f"Xarpus is dead in {total_swings_per_player} hits")



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
        print(f"Total Claw Damage {total_claw_damage}")
        print(f"Total Scythe Damage {total_scythe_damage}")
        print(f"Xarpus is dead in {total_swings_per_player} hits")






# player_salve = Player(stats=input_stats, weapon=scythe, wearing_salve=True)
# print(f"Player attack roll (w/ salve): {player_salve.calc_att_roll()}")
