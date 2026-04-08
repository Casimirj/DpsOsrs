from Player import Player

##actually infernal cape!!!
stats = {
    'hp_level': 99,
    'attack_level': 99,
    'strength_level': 99,
    'def_level': 99,
    'magic_level': 99,
    'ranged_level': 99,
    'prayer_level': 99,

    'slash_attack_bonus': 71,
    'stab_attack_bonus': 43,
    'crush_attack_bonus': 43,
    'magic_attack_bonus': -59,
    'ranged_attack_bonus': -44,

    'melee_strength_bonus': 57,
    'magic_strength_bonus': 0,
    'ranged_strength_bonus': 3
}


player = Player(stats=stats, wearing_salve=False, wearing_void=False)
