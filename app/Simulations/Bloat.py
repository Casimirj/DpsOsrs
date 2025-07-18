





from Monsters.Bloat import Bloat


def run_sim():
    tick = 0
    number_of_downs = 0

    bloat = Bloat()
    bloat.is_walking = True
    phase_end_time = bloat.get_walk_duration()
    
    while bloat.is_alive():
        tick += 1 
        
        if tick >= phase_end_time:
            if bloat.is_walking:
                bloat.is_walking = False
                phase_end_time = tick + bloat.down_durration

                number_of_downs += 1
            else:
                bloat.is_walking = True
                phase_end_time = tick + bloat.get_walk_duration()
        




