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

    'slash_attack_bonus': 2,
    'stab_attack_bonus': 2,
    'crush_attack_bonus': 2,
    'magic_attack_bonus': -4,
    'ranged_attack_bonus': 32,

    'melee_strength_bonus': 17,
    'magic_strength_bonus': 0,
    'ranged_strength_bonus': 8
}


player = Player(stats=stats, wearing_salve=False, wearing_void=True)
