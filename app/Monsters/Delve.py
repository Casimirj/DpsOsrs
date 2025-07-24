from Monsters.NPC import NPC


class Delve(NPC):

    def __init__(self, delve_level=1):
        scale_health = {
            8: 700,
            7: 675,
            6: 650, ##6+pet drops
            5: 625,
            4: 600,
            3: 575,
            2: 550,
            1: 525
        }

        ##when boss goes into 70% hp, it will change to 500hp shield phase, 
        ##then it switches back to normal HP

      
      
        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 300,
            'strength_level': 190,
            'def_level': 90,
            'magic_level': 275,
            'ranged_level': 110,
            # 'prayer_level': 20,

            'attack_bonus': 210,
            'magic_attack_bonus': 125,
            'ranged_attack_bonus': 120,

            'strength_bonus': 45,
            'magic_strength_bonus':30,
            'ranged_strength_bonus': 50,


            'stab_def': 300,
            'slash_def': 300,
            'crush_def': 60,
            'magic_def': 160,
            "ranged_def_light": 160,
            "ranged_def_med": 140,
            "ranged_def_heavy": 160
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=False, can_be_poisoned=True, can_be_venomed=False, weak_to_synapse=True)
        self.delve_level = delve_level
        self.is_shield_phase = False

        if delve_level == 1:
            self.is_shield_phase = False
            self.current_hp = scale_health[1]
                if self.current_hp <= (0.70 * scale_health[1]):
                    ##some way to temporarily store last self.current_hp
                    self.is_shield_phase = True
                    self.current_shield_hp = 500
                     print("Delve now has a shield phase")
                        if current_shield_hp <= 0:
                            self.is_shield_phase = False
                            self.current_hp = scale_health[1] * 0.70
                            ##some way to return the last self.current_hp
                            if self.current_hp <= 0:
                                self.is_dead = False
                                print("You follow Delve underground, Delve is now in 2nd phase")
        elif delve_level == 2:
            self.hp_level = scale_health[2]
            if self.current_hp <= scale_health[2] * 0.70:
                ##some way to temporarily store last self.current_hp
                self.is_shield_phase = True
                self.current_shield_hp = 500
                print("Delve now has a shield phase")
                if current_shield_hp <= 0:
                    self.is_shield_phase = False
                    self.current_hp = scale_health[2] * 0.70)
                    ##some way to return the last self.current_hp
                    if self.current_hp <= 0:
                        self.is_dead = True
                        print("You follow Delve underground, Delve is now in 3rd phase")
    