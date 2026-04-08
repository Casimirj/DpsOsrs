"""
Full Theatre of Blood Simulator - Supports Full Runs or Partial Room Selection
Runs complete ToB encounters with damage accumulation and detailed statistics
"""

import sys
import os
from datetime import datetime

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
from Weapons.Scythe import Scythe
from Weapons.NoxHally import NoxHally
from Weapons.Fists import Fists
from Weapons.DragonClaws import DragonClaws
from Weapons.CrystalHalberd import CrystalHalberd
from Weapons.ElderMaul import ElderMaul
from Weapons.Bgs import Bgs
from Weapons.SulfurBlades import SulfurBlades
from Weapons.DDSwAvernic import DDSwAvernic

from Monsters.Maiden import Maiden
from Monsters.Bloat import Bloat
from Monsters.Nylo_boss import P3Verzik as Nylo_boss
from Monsters.Sotetseg import Sotetseg
from Monsters.Xarpus import Xarpus

from Loadouts.OathTorvaRancour import player as oath_torva_rancour
from Loadouts.OathTorvaSalve import player as oath_torva_salve


# Player names
player_names = ["1sfrz", "2rdps", "3s", "4s", "5s"]

# Available weapons
weapon_options = {
    "1": ("Dragon Claws", DragonClaws()),
    "2": ("Crystal Halberd", CrystalHalberd()),
    "3": ("Scythe (regular)", Scythe()),
    "4": ("Elder Maul (def -35%)", ElderMaul()),
    "5": ("BGS (priority def)", Bgs()),
    "6": ("Sulfur Blades", SulfurBlades()),
    "7": ("DDS + Avernic", DDSwAvernic()),
    "8": ("Nox Halberd", NoxHally()),
}

# Theatre of Blood rooms
TOB_ROOMS = {
    "1": ("Maiden of Sugadinti", Maiden, 1),
    "2": ("Bloat", Bloat, 1),
    "3": ("Nylo Boss", Nylo_boss, 1),
    "4": ("Sotetseg", Sotetseg, 1),
    "5": ("Xarpus", Xarpus, 1),
}


def get_player_count():
    """Get number of players from user input."""
    while True:
        try:
            num = int(input("\nEnter number of players (3-5): "))
            if 3 <= num <= 5:
                return num
            print("Please enter a number between 3 and 5.")
        except ValueError:
            print("Please enter a valid number.")


def select_tob_rooms():
    """Allow user to select which ToB rooms to run."""
    print("\n" + "="*60)
    print("THEATRE OF BLOOD - ROOM SELECTION")
    print("="*60)
    
    print("\nAvailable Rooms:")
    for room_id, (room_name, _, _) in TOB_ROOMS.items():
        print(f"  [{room_id}] {room_name}")
    
    print("\nEnter room numbers to include (comma-separated):")
    print("  Example: 1,2,3,4,5 (full ToB)")
    print("  Example: 3,5 (just Nylo and Xarpus)")
    print("  Or press Enter for full ToB: ", end="")
    
    user_input = input().strip()
    
    if not user_input:
        # Default to full ToB
        selected_rooms = list(TOB_ROOMS.keys())
    else:
        try:
            selected_rooms = [r.strip() for r in user_input.split(",")]
            # Validate selections
            for room in selected_rooms:
                if room not in TOB_ROOMS:
                    print(f"Invalid room: {room}")
                    return select_tob_rooms()
        except:
            print("Invalid input. Please try again.")
            return select_tob_rooms()
    
    return selected_rooms


def get_weapon_selection(num_players, num_rounds, room_name):
    """Get weapon selections from user for all players and rounds."""
    print("\n" + "-"*60)
    print(f"WEAPON SELECTION - {room_name}")
    print("-"*60)
    
    # Display weapon options
    print("\nWEAPON OPTIONS:")
    for key, (name, _) in weapon_options.items():
        print(f"  [{key}] {name}")
    print()
    
    player_specs = []
    
    for round_num in range(num_rounds):
        print(f"\n--- Round {round_num + 1} ---")
        round_specs = []
        for player_num in range(num_players):
            while True:
                choice = input(f"Player {player_names[player_num]} weapon: ")
                if choice in weapon_options:
                    weapon_name, weapon = weapon_options[choice]
                    round_specs.append(weapon)
                    print(f"  → {player_names[player_num]} will use {weapon_name}")
                    break
                else:
                    print(f"Invalid choice. Please enter 1-{len(weapon_options)}.")
        player_specs.append(round_specs)
    
    return player_specs


def run_tob_simulation(selected_rooms, num_players, weapon_configs, num_simulations=1000):
    """
    Run a full or partial Theatre of Blood simulation.
    
    Args:
        selected_rooms: List of room IDs to run (e.g., ["1", "2", "3", "4", "5"])
        num_players: Number of players (3-5)
        weapon_configs: Dict mapping room_id to player weapon specs
                       Example: {"1": [[dc]*5, [dc]*5], "3": [[em]*5, [dc]*5]}
        num_simulations: Number of simulations to run (default 1000)
    
    Returns:
        Dictionary with comprehensive statistics
    """
    
    # Build room list
    rooms = [(TOB_ROOMS[room_id][0], TOB_ROOMS[room_id][1], room_id) 
             for room_id in selected_rooms]
    
    results = {
        'total_damage': [],
        'damage_per_room': {room_id: [] for room_id in selected_rooms},
        'damage_per_player': {name: [] for name in player_names[:num_players]},
        'room_details': {room_id: {
            'defense_final': [],
            'defense_threshold_met': 0
        } for room_id in selected_rooms},
    }
    
    print(f"\n{'='*60}")
    print(f"Running {num_simulations} ToB simulations")
    print(f"Rooms: {', '.join([TOB_ROOMS[r][0] for r in selected_rooms])}")
    print(f"Players: {num_players}")
    print('='*60)
    
    for sim in range(num_simulations):
        if num_simulations > 1 and (sim + 1) % 100 == 0:
            print(f"Progress: {sim + 1}/{num_simulations} simulations completed...")
        
        # Create fresh players for this simulation
        players = []
        for i in range(num_players):
            player = Player(stats=oath_torva_rancour.stats.get_stats())
            player.current_special_attack = 100
            players.append((player_names[i], player))
        
        # Track damage per player this simulation
        sim_damage = {name: 0 for name, _ in players}
        sim_total_damage = 0
        
        # Run each room
        for room_name, boss_class, room_id in rooms:
            # Create boss for this room
            boss = boss_class(num_players)
            
            # Get weapon specs for this room
            room_specs = weapon_configs[room_id]
            
            # Run each round (most rooms have 1 round, some have 2)
            for round_num, round_specs in enumerate(room_specs):
                # Each player attacks
                for i, (name, player) in enumerate(players):
                    player.equip_weapon(round_specs[i])
                    
                    # Check if weapon is scythe (regular hit, not special)
                    if round_specs[i].__class__.__name__ == 'Scythe':
                        hit = player.do_attack(boss, special_attack=False)
                    else:
                        hit = player.do_attack(boss, special_attack=True)
                    
                    boss.reduce_hp(hit)
                    sim_damage[name] += hit
                    sim_total_damage += hit
            
            # Record room statistics
            final_def = int(boss.stats.def_level)
            results['room_details'][room_id]['defense_final'].append(final_def)
            results['damage_per_room'][room_id].append(sim_total_damage)
        
        # Store results
        results['total_damage'].append(sim_total_damage)
        for name in player_names[:num_players]:
            results['damage_per_player'][name].append(sim_damage[name])
    
    return results


def print_tob_results(results, selected_rooms, num_players, num_simulations):
    """Print comprehensive ToB simulation results."""
    
    print(f"\n{'='*60}")
    print(f"THEATRE OF BLOOD SIMULATION RESULTS")
    print(f"Simulations: {num_simulations}")
    print(f"Players: {num_players}")
    print('='*60)
    
    # Overall statistics
    print(f"\nOVERALL STATISTICS")
    print("-"*60)
    avg_total = sum(results['total_damage']) / num_simulations
    min_total = min(results['total_damage'])
    max_total = max(results['total_damage'])
    print(f"Total Team Damage:")
    print(f"  Average: {avg_total:.2f}")
    print(f"  Min: {min_total}")
    print(f"  Max: {max_total}")
    
    # Per-room statistics
    print(f"\nPER-ROOM STATISTICS")
    print("-"*60)
    for room_id in selected_rooms:
        room_name = TOB_ROOMS[room_id][0]
        room_damage = results['damage_per_room'][room_id]
        avg_room_dmg = sum(room_damage) / num_simulations
        print(f"\n{room_name}:")
        print(f"  Average damage: {avg_room_dmg:.2f}")
        print(f"  Min damage: {min(room_damage)}")
        print(f"  Max damage: {max(room_damage)}")
    
    # Per-player statistics
    print(f"\nDPER-PLAYER STATISTICS (Total Average)")
    print("-"*60)
    total_team_damage = 0
    for name in player_names[:num_players]:
        avg_dmg = sum(results['damage_per_player'][name]) / num_simulations
        total_team_damage += avg_dmg
        percentage = (avg_dmg / (avg_total + 0.001)) * 100
        print(f"{name}: {avg_dmg:.2f} ({percentage:.1f}%)")
    print(f"\nTotal Team Damage: {total_team_damage:.2f}")


def main():
    """Main entry point for ToB simulator."""
    print("\n" + "="*60)
    print("THEATRE OF BLOOD - FULL/PARTIAL SIMULATOR")
    print("="*60)
    
    # Get player count
    num_players = get_player_count()
    
    # Select which rooms to run
    selected_rooms = select_tob_rooms()
    room_names = [TOB_ROOMS[r][0] for r in selected_rooms]
    
    print(f"\nRunning: {', '.join(room_names)}")
    
    # Get weapon selections for each room
    weapon_configs = {}
    for room_id in selected_rooms:
        room_name = TOB_ROOMS[room_id][0]
        # Most rooms have 1 spec round, but some might have 2
        num_rounds = 1
        weapon_specs = get_weapon_selection(num_players, num_rounds, room_name)
        weapon_configs[room_id] = weapon_specs
    
    # Run simulations
    results = run_tob_simulation(
        selected_rooms=selected_rooms,
        num_players=num_players,
        weapon_configs=weapon_configs,
        num_simulations=1000
    )
    
    # Print results
    print_tob_results(results, selected_rooms, num_players, 1000)
    
    print(f"\n{'='*60}")
    print("Simulation complete!")
    print('='*60)


if __name__ == "__main__":
    main()
