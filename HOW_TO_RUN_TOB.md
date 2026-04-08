# Complete Guide: Running ToB Simulations with Max Gear & Max Buffs

## Overview

Your OSRS combat simulator is **fully configured for max gear and max buffs**. You now have **three ways to run simulations**:

1. **Single Boss** (`NyloBossDamage.py`) - Test individual bosses
2. **Full/Partial ToB** (`FullToBSimulator.py`) - Custom room selection
3. **Pre-configured Scenarios** (`PresetScenarios.py`) - Run strategies without prompts

---

## Method 1: Single Boss Simulation

### Run Command
```powershell
cd C:\Github_projects\ToB\DpsOsrs
python NyloBossDamage.py
```

### What Happens
1. Enter number of players: `5`
2. Select weapons for Round 1 and Round 2
3. Automatically runs 1000 simulations
4. Outputs statistics with average damage, defense reduction, per-player breakdown

### Best For
- Testing weapon combinations quickly
- Individual boss analysis
- Optimizing one room's strategy

---

## Method 2: Full/Partial Theatre of Blood

### Run Command
```powershell
cd C:\Github_projects\ToB\DpsOsrs
python FullToBSimulator.py
```

### Interactive Prompts
```
Enter number of players (3-5): 5

THEATRE OF BLOOD - ROOM SELECTION
Available Rooms:
  [1] Maiden of Sugadinti
  [2] Bloat
  [3] Nylo Boss
  [4] Sotetseg
  [5] Xarpus

Enter room numbers to include (comma-separated):
Example: 1,2,3,4,5 (full ToB)
Example: 3,5 (just Nylo and Xarpus)
Or press Enter for full ToB: 1,2,3,4,5
```

### Weapon Selection
- For each selected room, choose weapons for each player
- Accumulates damage across all selected bosses
- Tracks per-room damage contribution

### Output
- **Total Team Damage**: Sum across all rooms
- **Per-Room Statistics**: Individual boss damage
- **Per-Player Breakdown**: Each player's contribution

### Best For
- Testing complete ToB strategies
- Comparing room performance
- Identifying weak links in team composition
- Analyzing accumulated fatigue effects (if implemented)

---

## Method 3: Pre-configured Scenarios (No Prompts)

### Run Command
```powershell
cd C:\Github_projects\ToB\DpsOsrs
python PresetScenarios.py
```

### Built-in Scenarios
1. **Full ToB - Maximum Damage** (All Dragon Claws)
   - Best for raw DPS testing
   
2. **Full ToB - Defense Reduction First** (Elder Maul → Dragon Claws)
   - Tests defense reduction strategy
   
3. **Full ToB - BGS Priority** (BGS → Dragon Claws)
   - Tests priority defense mechanic
   
4. **Partial ToB - Nylo Only** (Dragon Claws)
   - Single boss baseline
   
5. **Partial ToB - Xarpus Skip** (Defense Reduction)
   - Boss-specific optimization

### Output
- Runs all scenarios automatically
- Compares strategies side-by-side
- No user input required (~2-3 minutes total)

### Best For
- Quick strategy comparison
- Benchmarking different weapons
- Understanding which strategies work best
- Batch testing without prompts

---

## Max Gear & Max Buffs - Technical Details

### Gear (From `OathTorvaRancour` Loadout)
```
Equipment:
  Head: Torva Full Helm
  Body: Torva Platebody
  Legs: Torva Platelegs
  Hands: Torva Gloves (or similar)
  Feet: Rune Boots (or Primordial)
  Back: Avernic Defender
  Weapon: Your chosen weapon
  Ring: Ultor Ring (melee DPS)
  Cape: Max Cape (99 all)
  Amulet: Amulet of Fury (+20 all defensive bonuses)

Combat Skills: 99 All (Attack, Strength, Defense, Ranged, Magic, Prayer, HP)
Bonuses: +140 melee attack, +140 melee strength, +140 melee defense
```

### Buffs (Applied Automatically)
```python
super_combat=True       # +19 to Attack/Strength/Defense (3 ticks)
piety_active=True       # +20% Attack, +23% Strength, +25% Defense
rigour_active=True      # +20% Ranged, +23% Ranged Strength (if ranged)
augury_active=True      # +25% Magic, +4% Strength bonus
```

### Effective Combat Stats
```
Attack:    99 + 19 (SuperCombat) + 20% (Piety) = ~94 effective level
Strength:  99 + 19 (SuperCombat) + 23% (Piety) = ~129 effective level
Defense:   99 + 19 (SuperCombat) + 25% (Piety) = ~136 effective level
Magic:     99 + 13 (Magic Potion) + 25% (Augury) = Maxed with buffs
Ranged:    99 + 20% (Rigour) = Maxed
Prayer:    99 (always active)
```

---

## Weapon Comparison

| Weapon | Type | Hit Pattern | Best For |
|--------|------|-----------|----------|
| Dragon Claws | Melee Special | 4-hit burst | Maximum damage output |
| Elder Maul | Melee Special | Single hit | 35% defense reduction |
| BGS | Melee Special | Single hit | Priority defense reduction |
| Scythe | Melee Regular | 3-hit attack | Consistent damage (no spec) |
| Crystal Halberd | Ranged Attack | Single hit | AOE ranged attacks |
| Sulfur Blades | Melee | Multiple hits | Poison damage |
| DDS+Avernic | Melee | 2-hit combo | Defensive special |
| Nox Halberd | Ranged | Multiple hits | High accuracy ranged |

---

## Example Commands

### Full ToB - All Dragon Claws
```powershell
python NyloBossDamage.py
# Select: 5 players
# R1: 1,1,1,1,1 (Dragon Claws x5)
# R2: 1,1,1,1,1 (Dragon Claws x5)
# → Average team damage across all bosses
```

### Full ToB - Mixed Strategy
```powershell
python FullToBSimulator.py
# Select: 5 players
# Rooms: 1,2,3,4,5 (all rooms)
# Maiden R1: 4,4,4,1,1 (3x Elder Maul, 2x Dragon Claws)
# Bloat R1: 1,1,1,1,1 (5x Dragon Claws)
# ... (continue for each room)
# → Shows which rooms perform best with mixed strategy
```

### Quick Scenario Comparison
```powershell
python PresetScenarios.py
# Automatically runs 5 different strategies
# Compares: All DC vs EM→DC vs BGS→DC, etc.
# → Identifies best overall strategy (~2 min)
```

---

## Interpreting Results

### Key Metrics

**Average Damage**
- Mean damage dealt in a single simulation
- Used to compare strategies
- Higher = better performance

**Min/Max Damage**
- Range of possible damage outcomes
- Shows consistency vs variance
- Tight range = predictable, wide range = risky

**Defense Final**
- Boss defense level after all spec hits
- Negative values = below minimum (effective death)
- Track % of time ≤100 or ≤15 (threshold success)

**Per-Player Contribution**
- Individual damage output
- Percentage of team damage
- Identifies weak players or weapons

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named" errors | Make sure you're in `DpsOsrs` directory |
| Virtual environment issues | Run: `.\.venv\Scripts\Activate.ps1` |
| Slow performance | Reduce simulations (default 1000, try 100) |
| Out of memory | Run fewer simulations or on fewer bosses |
| Missing weapons | All 8 weapons are pre-configured, no custom needed |
| Results seem wrong | Check if you selected correct players/rounds |

---

## File Structure

```
DpsOsrs/
├── NyloBossDamage.py              ← Single boss simulator
├── FullToBSimulator.py            ← Full/partial ToB runner
├── PresetScenarios.py             ← Pre-configured strategies
├── RUN_SIMULATION_GUIDE.md        ← Detailed usage guide
├── QUICK_REFERENCE.md             ← Quick commands
├── HOW_TO_RUN_TOB.md              ← This file
│
├── app/
│   ├── Player.py                  ← Player class
│   ├── NPC.py                     ← Boss base class
│   ├── Weapon.py                  ← Weapon base class
│   ├── Stats.py                   ← Stats container
│   │
│   ├── Weapons/                   ← 8 weapon implementations
│   │   ├── DragonClaws.py
│   │   ├── ElderMaul.py
│   │   ├── Bgs.py
│   │   ├── Scythe.py
│   │   ├── CrystalHalberd.py
│   │   ├── SulfurBlades.py
│   │   ├── DDSwAvernic.py
│   │   └── NoxHally.py
│   │
│   ├── Monsters/                  ← 5 ToB boss implementations
│   │   ├── Maiden.py
│   │   ├── Bloat.py
│   │   ├── Nylo_boss.py
│   │   ├── Sotetseg.py
│   │   └── Xarpus.py
│   │
│   └── Loadouts/                  ← Max gear presets
│       ├── OathTorvaRancour.py
│       ├── OathTorvaSalve.py
│       ├── TbowQuiver.py
│       ├── Tbow_void.py
│       ├── OathFireRancour.py
│       └── OathFireSalve.py
│
└── requirements.txt               ← Dependencies
```

---

## Customization

To modify gear/buffs, edit `app/Loadouts/OathTorvaRancour.py`:

```python
# Example: Reduce buffs
player = Player(
    stats=oath_torva_rancour.stats.get_stats(),
    super_combat=False,    # Disable potion
    piety_active=False,    # Disable prayer
    rigour_active=True,    # Keep ranged
    augury_active=True     # Keep magic
)
```

To add custom weapons, create a new file in `app/Weapons/`:

```python
from Weapon import Weapon

class CustomWeapon(Weapon):
    def __init__(self):
        super().__init__(
            attack_speed=4,
            attack_bonus=50,
            strength_bonus=40,
            accuracy_bonus=30,
            combat_style="Melee",
            attack_type="Slash"
        )
```

---

## Next Steps

1. **Start with Method 3** (`PresetScenarios.py`) to see 5 different strategies compared
2. **Try Method 1** (`NyloBossDamage.py`) to fine-tune a single room
3. **Use Method 2** (`FullToBSimulator.py`) to build your custom full-run strategy
4. **Export Results** to Excel for detailed analysis (auto-generated)
5. **Iterate** on strategy based on results

---

## Performance Notes

- **Single simulation**: ~0.05 seconds
- **1000 simulations**: ~50 seconds
- **All 5 bosses x1000 sims**: ~250 seconds (~4 minutes)
- **All preset scenarios**: ~2-3 minutes total

For faster iteration, reduce simulations to 100-200 during testing, then use 1000+ for final analysis.

---

## Questions?

Refer to:
- `RUN_SIMULATION_GUIDE.md` - Detailed walkthrough
- `QUICK_REFERENCE.md` - Command quick reference
- `PresetScenarios.py` - See example code for custom configurations

Happy simulating! 🎮
