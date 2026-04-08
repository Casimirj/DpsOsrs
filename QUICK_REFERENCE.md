# ToB Simulation Quick Reference

## Run Single Boss (Nylo)
```powershell
cd C:\Github_projects\ToB\DpsOsrs
python NyloBossDamage.py
```
- Select 5 players
- Choose weapons for rounds
- Get statistics + 1000 simulations

---

## Run Full/Partial ToB
```powershell
cd C:\Github_projects\ToB\DpsOsrs
python FullToBSimulator.py
```
- Select player count (3-5)
- Select rooms: `1,2,3,4,5` (full) or `3,5` (partial)
- Choose weapons for each room
- Get accumulated damage statistics

---

## What's Already Max Geared & Buffed

✅ **Gear:** Full Torva + 99 all stats  
✅ **Buffs:** Super Combat (Str +19), Piety (+20% attack/+25% def), Rigour/Augury  
✅ **Prayer:** 99 Prayer always active  
✅ **Weapon:** Your chosen weapon each round  

---

## Available Weapons in Simulator

| #  | Weapon | Purpose |
|----|----|---------|
| 1  | Dragon Claws | 4-hit burst damage |
| 2  | Crystal Halberd | Ranged AOE attacks |
| 3  | Scythe | 3-hit regular attack (no spec) |
| 4  | Elder Maul | Reduces boss def by 35% |
| 5  | BGS | Priority defense reduction |
| 6  | Sulfur Blades | Melee damage |
| 7  | DDS + Avernic | Defensive dagger |
| 8  | Nox Halberd | High accuracy halberd |

---

## Example Strategies

### Max DPS (All Dragon Claws)
```
Round 1: All players = Dragon Claws (1)
Round 2: All players = Dragon Claws (1)
```

### Defense Reduction → Burst (Elder Maul → Dragon Claws)
```
Round 1: All players = Elder Maul (4)
Round 2: All players = Dragon Claws (1)
```

### Partial ToB: Just Nylo + Xarpus
```
Select rooms: 3,5
```

---

## Output Interpretation

- **Average Damage**: Mean damage dealt across all simulations
- **Defense Final**: Boss defense level after all hits
- **Per Player**: Individual contribution (useful for comparing DPS)
- **% Success Rate**: How often defense reaches threshold (≤100 in round 1)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | cd to DpsOsrs folder first |
| Virtual env not active | `.\.venv\Scripts\Activate.ps1` |
| openpyxl not found | Auto-installs when needed |
| Invalid weapon choice | Enter 1-8 |
| Too few/many players | Enter 3-5 |

---

## File Locations

| File | Purpose |
|------|---------|
| `NyloBossDamage.py` | Single boss simulator |
| `FullToBSimulator.py` | Full/partial ToB simulator |
| `RUN_SIMULATION_GUIDE.md` | Detailed guide |
| `app/Weapons/` | 10 weapon implementations |
| `app/Monsters/` | All boss implementations |
| `app/Loadouts/` | Max gear presets |

---

## Next Steps

1. Try single boss: `python NyloBossDamage.py`
2. Try full ToB: `python FullToBSimulator.py`
3. Experiment with different weapons
4. Export results to Excel (auto-generated)
5. Analyze which weapon combos are best

Happy simulating! 🎮
