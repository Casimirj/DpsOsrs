"""
Pre-configured ToB Simulation Scenarios
Run common strategies without interactive prompts
"""

import sys
import os

# Add the app directory to the Python path
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Create module aliases for import compatibility
import NPC
import Weapon
import Stats
import Player

sys.modules['Monsters.NPC'] = sys.modules['NPC']
sys.modules['Weapons.Weapon'] = sys.modules['Weapon']
sys.modules['Weapons.Stats'] = sys.modules['Stats']
sys.modules['Weapons.NPC'] = sys.modules['NPC']
sys.modules['Loadouts.Stats'] = sys.modules['Stats']
sys.modules['Loadouts.Weapon'] = sys.modules['Weapon']
sys.modules['Loadouts.Player'] = sys.modules['Player']

from Player import Player
from Weapons.DragonClaws import DragonClaws
from Weapons.ElderMaul import ElderMaul
from Weapons.Bgs import Bgs
from Weapons.Scythe import Scythe
from Weapons.CrystalHalberd import CrystalHalberd

from Monsters.Maiden import Maiden
from Monsters.Bloat import Bloat
from Monsters.Nylo_boss import P3Verzik as Nylo_boss
from Monsters.Sotetseg import Sotetseg
from Monsters.Xarpus import Xarpus

from Loadouts.OathTorvaRancour import player as oath_torva_rancour

player_names = ["1sfrz", "2rdps", "3s", "4s", "5s"]


# Weapon instances
dc = DragonClaws()
em = ElderMaul()
bgs = Bgs()
scythe = Scythe()
ch = CrystalHalberd()


def run_preset_scenario(name, description, bosses, weapon_config, num_players=5, num_simulations=1000):
    """
    Run a preset scenario and print results.
    
    Args:
        name: Scenario name
        description: Scenario description
        bosses: List of boss classes to run
        weapon_config: Dict mapping boss_name to weapon lists
                      Example: {"NyloBoss": [[dc]*5, [dc]*5]}
        num_players: Number of players
        num_simulations: Number of simulations
    """
    
    print(f"\n{'='*70}")
    print(f"SCENARIO: {name}")
    print(f"{'='*70}")
    print(f"Description: {description}")
    print(f"Players: {num_players} | Simulations: {num_simulations}")
    print()
    
    # Print weapon configuration
    for boss_name, specs in weapon_config.items():
        print(f"{boss_name}:")
        for round_num, round_weapons in enumerate(specs):
            weapon_names = [w.__class__.__name__ for w in round_weapons]
            print(f"  Round {round_num + 1}: {weapon_names[0]} (x{num_players})")
    
    results = {
        'total_damage': [],
        'damage_by_boss': {boss.__name__: [] for boss in bosses},
        'damage_per_player': {name: [] for name in player_names[:num_players]},
    }
    
    print(f"\nRunning simulations...", end="", flush=True)
    
    for sim in range(num_simulations):
        if (sim + 1) % 200 == 0:
            print(f" {sim + 1}", end="", flush=True)
        
        # Create fresh players
        players = []
        for i in range(num_players):
            player = Player(stats=oath_torva_rancour.stats.get_stats())
            player.current_special_attack = 100
            players.append((player_names[i], player))
        
        # Track damage
        sim_damage = {name: 0 for name, _ in players}
        sim_total_damage = 0
        
        # Run each boss
        for boss_class in bosses:
            boss_name = boss_class.__name__
            boss = boss_class(num_players)
            
            # Get weapon specs for this boss
            if boss_name not in weapon_config:
                print(f"\nWarning: No weapon config for {boss_name}")
                continue
            
            round_specs = weapon_config[boss_name]
            
            # Run each round
            for round_weapons in round_specs:
                for i, (name, player) in enumerate(players):
                    player.equip_weapon(round_weapons[i])
                    
                    # Check if scythe (regular hit)
                    if round_weapons[i].__class__.__name__ == 'Scythe':
                        hit = player.do_attack(boss, special_attack=False)
                    else:
                        hit = player.do_attack(boss, special_attack=True)
                    
                    boss.reduce_hp(hit)
                    sim_damage[name] += hit
                    sim_total_damage += hit
            
            results['damage_by_boss'][boss_name].append(sim_total_damage)
        
        # Store results
        results['total_damage'].append(sim_total_damage)
        for name in player_names[:num_players]:
            results['damage_per_player'][name].append(sim_damage[name])
    
    print(" Done!")
    
    # Print results
    print(f"\n{'─'*70}")
    print("RESULTS:")
    print(f"{'─'*70}")
    
    # Total damage
    avg_total = sum(results['total_damage']) / num_simulations
    min_total = min(results['total_damage'])
    max_total = max(results['total_damage'])
    
    print(f"\nTotal Damage (across all bosses):")
    print(f"  Average: {avg_total:,.2f}")
    print(f"  Min: {min_total:,}")
    print(f"  Max: {max_total:,}")
    
    # Per-player breakdown
    print(f"\nDamage by Player:")
    total_team_dmg = 0
    for name in player_names[:num_players]:
        avg_dmg = sum(results['damage_per_player'][name]) / num_simulations
        total_team_dmg += avg_dmg
        pct = (avg_dmg / avg_total) * 100 if avg_total > 0 else 0
        print(f"  {name}: {avg_dmg:,.2f} ({pct:.1f}%)")
    
    print(f"\n  Total Team: {total_team_dmg:,.2f}")
    
    return results


def main():
    """Run all preset scenarios."""
    
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█  THEATRE OF BLOOD - PRE-CONFIGURED SCENARIOS" + " "*24 + "█")
    print("█  5 Players, Max Gear, Max Buffs" + " "*35 + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Scenario 1: Full ToB - All Dragon Claws
    run_preset_scenario(
        name="Full ToB - Maximum Damage (All Dragon Claws)",
        description="All 5 players use Dragon Claws in all rounds",
        bosses=[Maiden, Bloat, Nylo_boss, Sotetseg, Xarpus],
        weapon_config={
            "Maiden": [[dc]*5],
            "Bloat": [[dc]*5],
            "Nylo_boss": [[dc]*5],
            "Sotetseg": [[dc]*5],
            "Xarpus": [[dc]*5],
        },
        num_players=5,
        num_simulations=500
    )
    
    # Scenario 2: Full ToB - Defense Reduction Strategy
    run_preset_scenario(
        name="Full ToB - Defense Reduction First (Elder Maul → Dragon Claws)",
        description="Round 1: Reduce boss defense with Elder Maul, Round 2: Burst with Dragon Claws",
        bosses=[Maiden, Bloat, Nylo_boss, Sotetseg, Xarpus],
        weapon_config={
            "Maiden": [[em]*5, [dc]*5],
            "Bloat": [[em]*5, [dc]*5],
            "Nylo_boss": [[em]*5, [dc]*5],
            "Sotetseg": [[em]*5, [dc]*5],
            "Xarpus": [[em]*5, [dc]*5],
        },
        num_players=5,
        num_simulations=500
    )
    
    # Scenario 3: Full ToB - BGS Priority Strategy
    run_preset_scenario(
        name="Full ToB - BGS Priority (BGS → Dragon Claws)",
        description="Round 1: BGS priority defense reduction, Round 2: Dragon Claws burst",
        bosses=[Maiden, Bloat, Nylo_boss, Sotetseg, Xarpus],
        weapon_config={
            "Maiden": [[bgs]*5, [dc]*5],
            "Bloat": [[bgs]*5, [dc]*5],
            "Nylo_boss": [[bgs]*5, [dc]*5],
            "Sotetseg": [[bgs]*5, [dc]*5],
            "Xarpus": [[bgs]*5, [dc]*5],
        },
        num_players=5,
        num_simulations=500
    )
    
    # Scenario 4: Partial ToB - Just Nylo Boss
    run_preset_scenario(
        name="Partial ToB - Nylo Boss Only (All Dragon Claws)",
        description="Single room test: Nylo Boss with Dragon Claws",
        bosses=[Nylo_boss],
        weapon_config={
            "Nylo_boss": [[dc]*5, [dc]*5],
        },
        num_players=5,
        num_simulations=1000
    )
    
    # Scenario 5: Partial ToB - Xarpus Skip
    run_preset_scenario(
        name="Partial ToB - Xarpus Skip (Defense Reduction)",
        description="Xarpus with Elder Maul → Dragon Claws strategy",
        bosses=[Xarpus],
        weapon_config={
            "Xarpus": [[em]*5, [dc]*5],
        },
        num_players=5,
        num_simulations=1000
    )
    
    print(f"\n{'█'*70}")
    print("All scenarios complete!")
    print(f"{'█'*70}\n")


if __name__ == "__main__":
    main()
