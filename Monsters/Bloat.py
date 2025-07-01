import NPC
import Stats

input_stats = {
    'hp_level': 100,
    'def_level': 50,
    'prayer_level': 20,
    'stab_def': 30
}

scale_health = {
    5: 2000,
    4: 1750,
    3: 1500,
    2: 1500,
    1: 1500
}

# stats = Stats.Stats(input_stats)
# print(input_stats["hp_level"])

bloat = NPC.NPC(input_stats)