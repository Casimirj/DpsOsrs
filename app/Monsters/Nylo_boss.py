from app.NPC import NPC


class P3Verzik(NPC):

    def __init__(self, scale=1):
        scale_health = {
            5: 2500,
            4: 2000,
            3: 1500,
            2: 1500,
            1: 1500
        }

      ##need to double check HP still
      
        input_stats = {
            'hp_level': scale_health[scale],
            'attack_level': 400,
            'strength_level': 350,
            'def_level': 50,
            'magic_level': 50,
            'ranged_level': 350,
            # 'prayer_level': 20,

            'attack_bonus': 0,
            'magic_attack_bonus': 600,
            'ranged_attack_bonus': 0,

            'strength_bonus': 60,
            'magic_strength_bonus': 600,
            'ranged_strength_bonus': 60,


            'stab_def': 0,
            'slash_def': 0,
            'crush_def': 0,
            'magic_def': 0,
            "ranged_def_light": 0,
            "ranged_def_med": 0,
            "ranged_def_heavy": 0
        }

        # stats = Stats(input_stats)
        super().__init__(input_stats, weak_to_salve=False)
