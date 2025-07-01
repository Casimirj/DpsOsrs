import NPC
import Stats

input_stats = {
    'hp_level': 100,
    'def_level': 50,
    'stab_def': 30
}
# stats = Stats.Stats(input_stats)
# print(input_stats["hp_level"])

bloat = NPC.NPC(input_stats)


print(bloat.stats.get_stats())
print()
print()
bloat.stats.print_stats()