import random

class Weapon():

    def __init__(self, 
        name=None,
        stats=None,
        combat_style=None, # melee, ranged, magic
        attack_type=None, # slash, crush, etc
        attack_style=None, # accurate, aggressive, etc
        attack_speed=None,
        attack_range=None,
        has_special_attack=None,
        special_attack_style=None
        ):

        if(any([
            None in [name, stats, combat_style, attack_type, attack_style, attack_speed, has_special_attack],
            has_special_attack and special_attack_style == None
        ])):
           print(f"{name.capitalize()} was not initialized with all values!")
           raise ValueError

        if(any([
            combat_style == "Melee" and attack_style not in ["Accurate", "Aggressive", "Defensive", "Controlled"],
            combat_style == "Ranged" and attack_style not in ["Accurate", "Rapid", "Defensive"],
            combat_style == "Mage" and attack_style not in ["Accurate", "Long-Range", "Autocast", "Defensive-Autocast"],
        ])):
            print(f"{combat_style} does not use style {attack_style}")

        self.name = name.capitalize()
        self.stats = stats
        self.combat_style = combat_style.capitalize()
        self.attack_type = attack_type.capitalize()
        self.attack_style = attack_style.capitalize()
        self.attack_speed = attack_speed
        self.attack_range = 1 if attack_range is None else attack_range
        self.has_special_attack = has_special_attack
        self.special_attack_style = special_attack_style.capitalize() if special_attack_style else "N/A"



    def do_attack(self, max_hit, player_attack_roll, npc_def_roll):
        hit_att_roll = random.randint(1, player_attack_roll)
        hit_def_roll = random.randint(1, npc_def_roll)

        # assuming att_roll == def_roll is a hit
        if(hit_att_roll < hit_def_roll):
            return 0
        else:
            return random.randint(1, max_hit)


