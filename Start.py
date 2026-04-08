#!/usr/bin/env python3
"""
OSRS Theatre of Blood Simulator - Interactive Menu
Choose your simulation type and get started in seconds
"""

import sys
import os
import subprocess

def print_banner():
    """Print welcome banner."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█  🎮 OSRS THEATRE OF BLOOD COMBAT SIMULATOR 🎮" + " "*20 + "█")
    print("█  5 Players | Max Gear | Max Buffs | Full/Partial ToB" + " "*13 + "█")
    print("█" + " "*68 + "█")
    print("█"*70 + "\n")


def print_menu():
    """Print main menu."""
    print("Choose a simulation type:\n")
    print("  [1] Pre-configured Scenarios (RECOMMENDED)")
    print("      └─ 5 different strategies, no setup needed, ~2 minutes")
    print("      └─ Perfect for: First-time users, strategy comparison\n")
    
    print("  [2] Interactive Full/Partial ToB")
    print("      └─ Choose rooms, players, and weapons")
    print("      └─ Perfect for: Custom testing, specific strategies\n")
    
    print("  [3] Single Boss Simulator")
    print("      └─ Deep dive into one boss (Nylo)")
    print("      └─ Perfect for: Optimizing individual rooms\n")
    
    print("  [4] View Documentation")
    print("      └─ Quick reference, detailed guides, etc.")
    print("      └─ Perfect for: Learning how to use\n")
    
    print("  [0] Exit\n")


def print_docs_menu():
    """Print documentation menu."""
    print("\nDocumentation:\n")
    print("  [1] INDEX.md - Overview & getting started")
    print("  [2] QUICK_REFERENCE.md - One-page command reference")
    print("  [3] HOW_TO_RUN_TOB.md - Complete technical guide")
    print("  [4] RUN_SIMULATION_GUIDE.md - Detailed walkthrough")
    print("  [0] Back\n")


def run_scenario(script_name, description):
    """Run a Python script."""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"{'='*70}\n")
    
    try:
        subprocess.run([sys.executable, script_name], check=False)
    except KeyboardInterrupt:
        print("\n\nSimulation cancelled by user.")
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        print("Make sure you're in the DpsOsrs directory with the virtual environment active.")


def view_doc(filename):
    """Display documentation file."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read()
                print(content)
            input("\nPress Enter to return to menu...")
        else:
            print(f"\n{filename} not found.")
    except Exception as e:
        print(f"Error reading {filename}: {e}")


def main():
    """Main menu loop."""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (0-4): ").strip()
        
        if choice == "1":
            run_scenario(
                "PresetScenarios.py",
                "Pre-configured Scenarios (5 strategies)"
            )
        
        elif choice == "2":
            run_scenario(
                "FullToBSimulator.py",
                "Interactive Full/Partial ToB Simulator"
            )
        
        elif choice == "3":
            run_scenario(
                "NyloBossDamage.py",
                "Single Boss Simulator (Nylo)"
            )
        
        elif choice == "4":
            while True:
                print_docs_menu()
                doc_choice = input("Enter your choice (0-4): ").strip()
                
                if doc_choice == "1":
                    view_doc("INDEX.md")
                elif doc_choice == "2":
                    view_doc("QUICK_REFERENCE.md")
                elif doc_choice == "3":
                    view_doc("HOW_TO_RUN_TOB.md")
                elif doc_choice == "4":
                    view_doc("RUN_SIMULATION_GUIDE.md")
                elif doc_choice == "0":
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == "0":
            print("\n👋 Thanks for using the ToB Simulator!")
            print("Happy simulating!\n")
            break
        
        else:
            print("Invalid choice. Please enter 0-4.")
        
        input("\nPress Enter to continue...")
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋\n")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you:")
        print("  1. Are in the DpsOsrs directory")
        print("  2. Have the virtual environment activated")
        print("  3. Have Python 3.7+ installed")
