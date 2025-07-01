
import math
import Stats

class NPC:

    def __init__(self, stats=None):
        if stats == None:
            raise ValueError("Stats cannot be null")
        self.stats = Stats.Stats(stats)




    def calc_def_roll(self):
        def_roll = (self.stats.def_level + 9) * (self.stats.slash_def + 64)
        return def_roll
    

    def reduce_defense(self, damage_amount):
        self.stats.def_level = self.stats.def_level - damage_amount
        self.stats.def_level = self.stats.def_level if self.stats.def_level >= 0 else 0
        return self.stats.def_level

    def reduce_defense_with_bgs(self, damage_amount):
        remaining_damage = damage_amount
        # Defense reduction
        if remaining_damage > 0 and self.stats.def_level > 0:
            reduction = min(remaining_damage, self.stats.def_level)
            self.stats.def_level -= reduction
            remaining_damage -= reduction
        # Strength reduction
        if remaining_damage > 0 and self.stats.strength_level > 0:
            reduction = min(remaining_damage, self.stats.strength_level)
            self.stats.strength_level -= reduction
            remaining_damage -= reduction
        # Prayer reduction
        if remaining_damage > 0 and self.stats.prayer_level > 0:
            reduction = min(remaining_damage, self.stats.prayer_level)
            self.stats.prayer_level -= reduction
            remaining_damage -= reduction
        # Attack reduction
        if remaining_damage > 0 and self.stats.attack_level > 0:
            reduction = min(remaining_damage, self.stats.attack_level)
            self.stats.attack_level -= reduction
            remaining_damage -= reduction
        # Magic reduction
        if remaining_damage > 0 and self.stats.magic_level > 0:
            reduction = min(remaining_damage, self.stats.magic_level)
            self.stats.magic_level -= reduction
            remaining_damage -= reduction
        # Ranged reduction
        if remaining_damage > 0 and self.stats.ranged_level > 0:
            reduction = min(remaining_damage, self.stats.ranged_level)
            self.stats.ranged_level -= reduction
            remaining_damage -= reduction

    def reduce_defense_dwh(self):
        current_def = self.stats.def_level
        reduce_amount = current_def * .30
        return self.reduce_defense(reduce_amount)

    def reduce_defense_maul(self):
        current_def = self.stats.def_level
        reduce_amount = current_def * .35
        return self.reduce_defense(reduce_amount)



    def reduce_defense_bgs(self, amount):
        return self.reduce_defense_with_bgs(amount)



# print(f"Monster Def Roll {calc_def_roll()}")



