# How to Run ToB Simulations - Complete Guide

## Quick Start: Run a Single Boss Simulation

```powershell
# Navigate to the project directory
cd C:\Github_projects\ToB\DpsOsrs

# Activate virtual environment (if not already active)
.\.venv\Scripts\Activate.ps1

# Run the Nylo Boss simulation
python NyloBossDamage.py
```

### What Happens

1. **Interactive Setup Prompt:**
   ```
   NYLO BOSS SPEC SIMULATION SETUP
   ==================================================
   
   Boss: Nylo Boss
   Enter number of players (3-5): 5
   ```
   - Enter: `5` (for 5 players)

2. **Weapon Selection:**
   ```
   WEAPON OPTIONS:
     [1] Dragon Claws
     [2] Crystal Halberd
     [3] Scythe (regular hit)
   
   --- Round 1 ---
   Player 1sfrz weapon: 1
   → 1sfrz will use Dragon Claws
   
   Player 2rdps weapon: 1
   → 2rdps will use Dragon Claws
   ...
   (repeat for 5 players)
   
   --- Round 2 ---
   Player 1sfrz weapon: 1
   → 1sfrz will use Dragon Claws
   ...
   ```
   - Enter weapon choice (1-3) for each player in each round

3. **Automatic Output:**
   ```
   ==================================================
   SUMMARY STATISTICS (1000 simulations)
   ==================================================
   
   Round 1:
     Average defense after: 45.67
     Min defense: 10
     Max defense: 98
     Average damage dealt: 245.34
     % of time defense ≤ 100: 87.3%
   
   Round 2:
     Average defense after: 3.21
     Min defense: -50
     Max defense: 34
     Average damage dealt: 198.56
     % of time defense ≤ 15: 92.1%
   
   Average total damage (all rounds): 443.90
   Average final defense: 3.21
   
   Damage by player (total average):
     1sfrz: 89.23
     2rdps: 87.34
     3s: 88.90
     4s: 89.12
     5s: 89.31
   
   Total team damage (average): 443.90
   ```

---

## Max Gear & Max Buffs - Already Applied!

Your simulation **already includes max gear and max buffs by default**. Here's what's configured:

### Max Gear (From `OathTorvaRancour` Loadout)
- ✅ **Armor:** Full Torva (Helm, Body, Legs)
- ✅ **Weapon:** Your chosen weapon (Scythe, Dragon Claws, etc.)
- ✅ **All 11 Equipment Slots:** Optimized
- ✅ **Combat Skills:** 99 Attack, 99 Strength, 99 Defense, 99 HP, 99 Magic, 99 Ranged, 99 Prayer
- ✅ **Attack Bonuses:** +140 melee attack

### Max Buffs (Applied in Code)
```python
Player(
    stats=oath_torva_rancour.stats.get_stats(),  # Max gear
    super_combat=True,      # +19 Attack/Strength/Defense
    piety_active=True,      # +20% Attack, +23% Strength, +25% Defense
    rigour_active=True,     # +20% Ranged, +23% Ranged Strength (if ranged)
    augury_active=True      # +25% Magic, +4% Strength
)
```

**Stat Bonuses Applied:**
- Attack: +19 (Super Combat) + 20% (Piety) = ~94 total effective level
- Strength: +19 (Super Combat) + 23% (Piety) = ~129 effective level
- Defense: +19 (Super Combat) + 25% (Piety) = ~136 effective level
- Magic: +13 (Magic Potion) + 25% (Augury) = 99 Magic + buffs
- Prayer: Always at 99 (built-in to loadout)

---

## Understanding the Output

### Key Metrics

**Defense Thresholds:**
- **Round 1:** Tracks % of time defense ≤ 100 (indicates effective spec damage)
- **Round 2:** Tracks % of time defense ≤ 15 (indicates near-zero defense)

**Damage Per Round:**
- Shows how much total damage the team deals each round
- Damage is split among weapons/hits

**Damage Per Player:**
- Individual contribution of each player
- Useful for identifying weak weapons or player positions

---

## Available Weapons

1. **Dragon Claws** - 4-hit special attack
2. **Crystal Halberd** - AOE ranged attack
3. **Scythe** - 3-hit regular attack (not special)
4. **Elder Maul** - Defense reduction special
5. **Bandos Godsword** - Priority defense reduction
6. **Dark Hammer** - 30% defense reduction

*Note: More weapons available in `app/Weapons/` folder*

---

## Running Specific Scenarios

### Scenario 1: All Dragon Claws (Max DPS)
```
Enter number of players: 5

--- Round 1 ---
Player 1sfrz weapon: 1 (Dragon Claws)
Player 2rdps weapon: 1 (Dragon Claws)
Player 3s weapon: 1 (Dragon Claws)
Player 4s weapon: 1 (Dragon Claws)
Player 5s weapon: 1 (Dragon Claws)

--- Round 2 ---
Player 1sfrz weapon: 1 (Dragon Claws)
... (same for all players)
```
→ Tests team DPS with highest damage output weapon

### Scenario 2: Defense Reduction Strategy
```
Enter number of players: 5

--- Round 1 ---
Player 1sfrz weapon: 3 (Elder Maul - reduces defense)
Player 2rdps weapon: 3 (Elder Maul)
Player 3s weapon: 3 (Elder Maul)
Player 4s weapon: 1 (Dragon Claws)
Player 5s weapon: 1 (Dragon Claws)

--- Round 2 ---
Player 1sfrz weapon: 1 (Dragon Claws - finish with damage)
... (all Dragon Claws)
```
→ Tests defense reduction followed by burst damage

### Scenario 3: Balanced Team Composition
```
Round 1: All Elder Maul/BGS (reduce defense)
Round 2: All Dragon Claws (maximize damage)
```
→ Tests optimal boss skip strategy

---

## Creating Your Own ToB Simulator

The current system supports **only single bosses**. For a **full 5-room ToB** or **partial ToB run**, you'll need to:

### What You'll Need:
1. Sequential boss encounters (Maiden → Bloat → Nylo → Sotetseg → Xarpus)
2. Damage accumulation across all bosses
3. Player stats carried over between rooms
4. Optional room selection (run only specific bosses)

### Example: Running Full ToB
- Room 1: Maiden of Sugadinti (2 phases, 1 spec round)
- Room 2: Bloat (multi-phase, 1 spec round)
- Room 3: Nylo Boss (1 spec round)
- Room 4: Sotetseg (1 spec round)
- Room 5: Xarpus (1 spec round)

**Total team damage = sum of all room damage**

---

## Advanced: Custom Weapon Selection Script

To run more complex scenarios programmatically (instead of interactive mode), create a Python script:

```python
from NyloBossDamage import run_spec_simulation, export_to_excel
from Monsters.Nylo_boss import P3Verzik as Nylo_boss
from Weapons.DragonClaws import DragonClaws
from Weapons.ElderMaul import ElderMaul
from Weapons.Scythe import Scythe

# Define your strategy
dragon_claws = DragonClaws()
elder_maul = ElderMaul()
scythe = Scythe()

# 5 players: all Dragon Claws in round 1 and 2
player_specs = [
    [dragon_claws] * 5,  # Round 1 - all Dragon Claws
    [dragon_claws] * 5,  # Round 2 - all Dragon Claws
]

# Run 1000 simulations with this configuration
results = run_spec_simulation(
    boss_class=Nylo_boss,
    num_players=5,
    player_specs=player_specs,
    num_simulations=1000,
    verbose=True
)

# Export to Excel for analysis
export_to_excel(results, "NyloBoss", 5, player_specs, 1000)
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'Monsters'"
- **Solution:** Make sure you're in the `DpsOsrs` directory when running the script
- Run: `cd C:\Github_projects\ToB\DpsOsrs`

### "No module named 'openpyxl'"
- **Solution:** The script auto-installs it when needed for Excel export
- Or manually install: `pip install openpyxl`

### Virtual environment not activated
- **Activate with:** `.\.venv\Scripts\Activate.ps1`
- Check: You should see `(.venv)` in your PowerShell prompt

---

## File Structure

```
DpsOsrs/
├── NyloBossDamage.py          # Main simulation runner
├── app/
│   ├── Player.py              # Player class
│   ├── Weapon.py              # Weapon base class
│   ├── NPC.py                 # Boss base class
│   ├── Stats.py               # Stats container
│   ├── Weapons/               # 10 weapon implementations
│   ├── Monsters/              # 8 boss implementations
│   └── Loadouts/              # Pre-configured max gear setups
└── requirements.txt           # Dependencies
```

---

## Next Steps

1. **Try the basic simulation:** Run with Dragon Claws
2. **Experiment with different weapons:** Test Elder Maul vs Dragon Claws
3. **Create a full ToB script:** (Ask if you want help building this)
4. **Export results to Excel:** The script does this automatically
5. **Analyze the statistics:** Use Excel for charts and comparisons

Happy simulating! 🎮
