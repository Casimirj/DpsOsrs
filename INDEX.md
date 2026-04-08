# 🎮 OSRS Theatre of Blood Combat Simulator

## Your Complete Simulation Suite

**3 Ways to Run Simulations | Full ToB or Single Bosses | Max Gear & Max Buffs Always Active**

---

## 🚀 Quick Start (30 seconds)

```powershell
cd C:\Github_projects\ToB\DpsOsrs
python PresetScenarios.py
```

This will automatically run **5 pre-configured strategies** and compare them. Takes ~2 minutes, no prompts needed.

---

## 📋 Documentation Index

| Document | Purpose | Read If... |
|----------|---------|-----------|
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | One-page command reference | You want quick commands |
| [HOW_TO_RUN_TOB.md](HOW_TO_RUN_TOB.md) | Complete technical guide | You want full details |
| [RUN_SIMULATION_GUIDE.md](RUN_SIMULATION_GUIDE.md) | Detailed usage guide | You need step-by-step instructions |

---

## 🎯 Three Ways to Simulate

### 1️⃣ Pre-configured Scenarios (Recommended for First-Time)

```powershell
python PresetScenarios.py
```

**What it does:**
- Runs 5 different weapon strategies automatically
- Compares All DC vs EM→DC vs BGS→DC, etc.
- Full ToB for each scenario
- No user input required
- ~2 minute runtime

**Best for:** Quick strategy comparison, benchmarking

---

### 2️⃣ Full/Partial ToB Runner (Most Flexible)

```powershell
python FullToBSimulator.py
```

**Interactive setup:**
- Select 3-5 players
- Choose which rooms to run (full ToB or partial)
- Select weapons for each room
- Runs 1000 simulations
- Outputs accumulated damage statistics

**Best for:** Custom room combinations, testing specific strategies

---

### 3️⃣ Single Boss Simulator (For Deep Analysis)

```powershell
python NyloBossDamage.py
```

**What it does:**
- Tests a single boss encounter
- Currently hardcoded to Nylo Boss
- Runs 1000 simulations per strategy
- Per-round defense tracking
- Defense threshold success rates

**Best for:** Optimizing individual boss strategies

---

## ⚙️ Configuration

### Max Gear (Always Active)
✅ Full Torva armor set  
✅ 99 all combat skills  
✅ +140 melee attack/strength/defense  
✅ Optimal weapon selection each round  

### Max Buffs (Always Active)
✅ Super Combat (+19 to A/S/D)  
✅ Piety (+20% Attack, +23% Strength, +25% Defense)  
✅ Rigour (+20% Ranged, +23% Ranged Strength)  
✅ Augury (+25% Magic, +4% Strength)  
✅ 99 Prayer always active  

### Effective Combat Stats
```
Attack:    ~94 effective (99 + 19 + 20%)
Strength:  ~129 effective (99 + 19 + 23%)
Defense:   ~136 effective (99 + 19 + 25%)
Magic:     99 with buffs
Ranged:    99 with buffs
```

---

## 🏹 Available Weapons

| # | Weapon | Purpose | Use Case |
|---|--------|---------|----------|
| 1 | Dragon Claws | 4-hit burst | Maximum DPS |
| 2 | Crystal Halberd | Ranged AOE | Group encounters |
| 3 | Scythe | 3-hit regular | Consistent damage |
| 4 | Elder Maul | -35% defense | Defense reduction |
| 5 | BGS | Priority def | Priority reduction |
| 6 | Sulfur Blades | Multi-hit | Poison damage |
| 7 | DDS+Avernic | Defensive | Tank spec |
| 8 | Nox Halberd | Ranged attack | High accuracy |

---

## 📊 Understanding Results

### Output Includes:

**Total Damage**
- Average across all simulations
- Min/max range
- Shows consistency

**Defense Final**
- Boss defense after all specs
- Percentage meeting thresholds (≤100, ≤15)
- Indicates if strategy "works"

**Per-Player Breakdown**
- Individual contribution %
- Identifies weak weapons/players
- Team composition analysis

**Per-Room Statistics** (Full ToB only)
- Which rooms perform best
- Damage contribution per room
- Identifies skip potential

---

## 📈 Common Scenarios

### Scenario 1: Maximum DPS
```
All Dragon Claws in all rounds
→ Tests pure damage output ceiling
→ Benchmark for other strategies
```

### Scenario 2: Defense Reduction Strategy
```
Round 1: Elder Maul (reduce defense 35%)
Round 2: Dragon Claws (burst damage)
→ Tests two-phase approach
→ More realistic room strategy
```

### Scenario 3: Priority Defense
```
Round 1: BGS (priority reduction)
Round 2: Dragon Claws
→ Tests priority reduction mechanic
→ Useful for difficult bosses
```

### Scenario 4: Partial ToB
```
Rooms: 3,5 (Nylo + Xarpus)
→ Tests specific room combinations
→ Useful for learning/testing
```

---

## 🔧 File Structure

```
DpsOsrs/
├── 📄 INDEX.md                    ← You are here
├── 📄 QUICK_REFERENCE.md
├── 📄 HOW_TO_RUN_TOB.md
├── 📄 RUN_SIMULATION_GUIDE.md
│
├── 🐍 PresetScenarios.py          ← Pre-configured (no prompts)
├── 🐍 FullToBSimulator.py         ← Full/partial ToB (interactive)
├── 🐍 NyloBossDamage.py           ← Single boss (interactive)
│
└── app/
    ├── 🐍 Player.py               ← Player simulation
    ├── 🐍 NPC.py                  ← Boss base class
    ├── 🐍 Weapon.py               ← Weapon base class
    ├── 🐍 Stats.py                ← Combat stats
    │
    ├── Weapons/                   ← 8 weapon implementations
    ├── Monsters/                  ← 5 ToB bosses (Maiden, Bloat, Nylo, Sotetseg, Xarpus)
    └── Loadouts/                  ← Max gear presets (OathTorva, etc.)
```

---

## 💡 Examples

### Example 1: Quick Comparison of All Strategies
```powershell
# 2-minute test of 5 strategies
python PresetScenarios.py
```

### Example 2: Test Full ToB with Custom Strategy
```powershell
# Interactive setup
python FullToBSimulator.py
# Select: 5 players
# Rooms: 1,2,3,4,5 (full ToB)
# Weapons: Your choice for each room
```

### Example 3: Optimize Single Boss
```powershell
# Test Nylo with different weapons
python NyloBossDamage.py
# Select: 5 players
# Try different weapon combos
# Compare results
```

---

## 🎮 Typical Workflow

1. **Start here:** Run `PresetScenarios.py` to see example strategies (~2 min)
2. **Analyze:** Look at results to understand what works
3. **Customize:** Use `FullToBSimulator.py` to test your own combinations
4. **Optimize:** Use `NyloBossDamage.py` to deep-dive on specific rooms
5. **Export:** Results automatically save to Excel for further analysis

---

## ⚡ Performance

| Test | Duration |
|------|----------|
| 1 simulation | 0.05 seconds |
| 100 simulations | 5 seconds |
| 1000 simulations (1 boss) | 50 seconds |
| 1000 simulations (all 5 bosses) | 250 seconds (~4 min) |
| All 5 preset scenarios | 2-3 minutes |

**Tip:** Use 100-200 simulations during testing, 1000+ for final analysis

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| "ModuleNotFoundError" | Change to `DpsOsrs` directory first |
| Virtual env not active | Run `.\.venv\Scripts\Activate.ps1` |
| Missing openpyxl | Auto-installs or run `pip install openpyxl` |
| No results output | Check simulation completed without errors |

---

## 📚 Next Steps

1. **Read:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md) (1 min) - Commands overview
2. **Try:** `python PresetScenarios.py` (2 min) - See it in action
3. **Explore:** [HOW_TO_RUN_TOB.md](HOW_TO_RUN_TOB.md) (10 min) - Full technical details
4. **Experiment:** Use `FullToBSimulator.py` to build your strategies
5. **Analyze:** Export results to Excel for detailed comparison

---

## 🎯 Key Features

✅ **5 Theatre of Blood Bosses** - Maiden, Bloat, Nylo, Sotetseg, Xarpus  
✅ **8 Weapons** - DC, EM, BGS, Scythe, CH, and more  
✅ **Full/Partial Room Selection** - Run any combination  
✅ **Max Gear Always** - Torva + 99 all skills  
✅ **Max Buffs Always** - Piety, Rigour, Augury active  
✅ **1000 Simulations** - Statistical significance  
✅ **Per-Player Breakdown** - Individual contribution tracking  
✅ **Excel Export** - Analysis and charts  
✅ **Pre-configured Scenarios** - No setup needed  
✅ **Interactive Customization** - Full flexibility  

---

## 🚀 Ready?

### For Immediate Results:
```powershell
python PresetScenarios.py
```

### For Custom Testing:
```powershell
python FullToBSimulator.py
```

### For Quick Reference:
See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### For Complete Details:
Read [HOW_TO_RUN_TOB.md](HOW_TO_RUN_TOB.md)

---

## 📞 Support

- Command reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Detailed guide: [HOW_TO_RUN_TOB.md](HOW_TO_RUN_TOB.md)
- Usage walkthrough: [RUN_SIMULATION_GUIDE.md](RUN_SIMULATION_GUIDE.md)

---

**Happy simulating!** 🎮

*Last updated: 2024*
