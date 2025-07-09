

from Monsters.Bloat import Bloat
from Monsters.Sotetseg import Sotetseg

bloat = Sotetseg(1)


# input_stats = {
#     'hp_level': 100,
#     'def_level': 50,
#     'prayer_level': 20,
#     'stab_def': 30
# }
# # stats = Stats.Stats(input_stats)
# # print(input_stats["hp_level"])

# bloat = NPC.NPC(input_stats)


# print(bloat.stats.get_stats())
# print()
# print()
bloat.stats.print_stats()

bloat.reduce_defense_bgs(180)

bloat.stats.print_stats()
