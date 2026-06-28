# OSRS Combat Calculations

This document defines exactly how a hit is calculated in Old School RuneScape for all three combat styles (Melee, Ranged, Magic). All formulas are sourced directly from the [OSRS Wiki](https://oldschool.runescape.wiki).

---

## Table of Contents

1. [Common Mechanics](#common-mechanics)
2. [Melee](#melee)
3. [Ranged](#ranged)
4. [Magic](#magic)
5. [References](#references)

---

## Common Mechanics

Every attack goes through two stages:

**Stage 1 — Accuracy Roll:** The attacker's offensive bonuses are rolled against the target's defensive bonuses. If the attack fails, the hit is a `0` (or a splash for player Magic attacks). This is **not** a successful hit.

**Stage 2 — Damage Roll:** A random integer from `0` to the attacker's maximum hit (inclusive) is rolled. Each possible value has an equal chance of being rolled. For players, a roll of `0` on a successful hit is rounded up to `1`. ([source](https://oldschool.runescape.wiki/w/Successful_hit))

**Global damage cap:** All player damage is capped at 200. ([source](https://oldschool.runescape.wiki/w/Maximum_melee_hit))

### Hit Chance Formula

```
If Attack Roll > Defence Roll:
    Hit Chance = 1 - (Def Roll + 2) / (2 × (Atk Roll + 1))

Else:
    Hit Chance = Atk Roll / (2 × (Def Roll + 1))
```

### Average Damage Per Attack

```
Avg Damage per Attack = Hit Chance × ( Max Hit / 2  +  1 / (Max Hit + 1) )
```

The small `1 / (Max Hit + 1)` term accounts for a `0` damage roll being changed to `1` on successful player hits.

**Damage Per Second (DPS):** Divide average damage per attack by the attack speed of the weapon/spell in seconds.

---

## Melee

| Source | Link |
|--------|------|
| Max Hit | https://oldschool.runescape.wiki/w/Maximum_melee_hit |
| DPS | https://oldschool.runescape.wiki/w/Damage_per_second/Melee |
| Successful Hit | https://oldschool.runescape.wiki/w/Successful_hit |

### Step 1: Calculate Effective Strength Level

```
Effective Strength = floor((
    floor( floor(Strength Level + Potion Bonus) × Prayer Bonus ) + Style Bonus + 8
) × Void Bonus)
```

**Potion Bonus (addition, not multiplier):**

| Potion | Bonus |
|--------|-------|
| Strength potion | `floor(Strength Level × 10%) + 3` |
| Zamorak brew | `floor(Strength Level × 12%) + 2` |
| Black warlock | `floor(Strength Level × 15%) + 4` |
| Super strength | `floor(Strength Level × 15%) + 5` |
| Dragon battleaxe spec | `floor( (floor(Atk × 10%) + floor(Def × 10%) + floor(Magic × 10%) + floor(Ranged × 10%)) × 25% ) + 10` |

Note: Dragon battleaxe uses the player's **visible** levels, not base levels.

**Prayer Bonus (multiplier):**

| Prayer | Multiplier |
|--------|------------|
| Burst of Strength | 1.05 |
| Superhuman Strength | 1.10 |
| Ultimate Strength | 1.15 |
| Chivalry | 1.18 |
| Piety | 1.23 |

**Style Bonus (addition):**

| Style | Bonus |
|-------|-------|
| Aggressive | 3 |
| Controlled | 1 |
| Accurate / Defensive | 0 |

**Void Bonus:**

| Condition | Multiplier |
|-----------|------------|
| Full melee void | 1.10 |
| No void | 1.00 |

### Step 2: Calculate Maximum Melee Hit

From the DPS page (which includes the gear bonus step):

```
Max Hit = floor( floor( 0.5 + Effective Strength × (Strength Bonus + 64) / 640 ) × Gear Bonus )
```

**Strength Bonus** is the "Melee Strength" value shown in the Equipment Stats window under "Other bonuses".

**Gear Bonus:**

| Condition | Multiplier |
|-----------|------------|
| Black mask / Slayer helm (on task) | 7/6 (≈1.167) |
| Salve amulet (undead) | 7/6 (≈1.167) |
| Salve amulet (e) (undead) | 1.20 |
| PvP: Protect from Melee on target | 6/10 (0.60) |

Black mask and Salve amulet do **NOT** stack — only the highest applicable bonus applies.

### Step 3: Calculate Bonus Damage (Special Attacks & Effects)

From the Max Hit page:

```
Max Hit = floor( floor( Base Damage ) × Special Bonus )
```

**Special Attack Multipliers:**

| Attack / Effect | Multiplier |
|-----------------|------------|
| Armadyl godsword | 1.375 |
| Bandos godsword | 1.21 |
| Ancient / Saradomin / Zamorak godsword | 1.10 |
| Dragon dagger | 1.15 + 1.15 (two hits) |
| Dragon halberd / Crystal halberd | 1.10 |
| Dragon hasta | 1.0 + (0.5 × Special bar %) |
| Dragon longsword | 1.25 |
| Dragon mace | 1.50 |
| Dragon warhammer | 1.50 |
| Rune claws | 1.10 |
| Abyssal dagger | 0.85 |
| Abyssal bludgeon | 1.0 + 0.005 × (Prayer points missing) |
| Saradomin sword | 1.10 (plus magic component — see Special Cases below) |
| Saradomin's blessed sword | 1.25 |

**Passive Effect Multipliers:**

| Attack / Effect | Multiplier |
|-----------------|------------|
| Dharok's set | `1 + ((Max HP − Current HP) / 100) × (Max HP / 100)` |
| Berserker necklace + Obsidian armour (helm/body/legs) + Obsidian weapon | 1.30 |
| Castle wars bracelet (attacking flag bearer) | 1.20 |
| Blisterwood flail (vs vampyres) | 1.25 |
| Ivandis flail (vs vampyres) | 1.20 |
| Viggora's chainmace / Ursine chainmace (charged, wilderness) | 1.50 |
| Black mask / Slayer helm (on task) | 7/6 (≈1.167) |
| Salve amulet (undead) | 7/6 (≈1.167) |
| Salve amulet (e) (undead) | 1.20 |
| Inquisitor's armour (crush) | 1.025 |
| Colossal blade | `1 + (2 × MonsterSize)` (additive to max hit, not multiplicative) |
| Osmumten's fang | 0.85 (minimum hit becomes `0.15 × Base Max Hit`) |

**Black mask / Salve amulet do NOT stack** — only the highest applicable bonus applies between the two.

#### Special Cases

**Saradomin sword:** The special attack's magic component deals up to an extra 16 magic-based damage:

```
Max Hit = floor( Base Damage + 16 )
```

This is in addition to the 1.10 multiplier on the melee component.

**Keris and Keris partisan (vs kalphites/scabarites):**

```
Max Hit_normal   = floor( Base Damage × 1.33 )
Max Hit_critical = floor( Base Damage × 1.33 × 3 )
```

**Dharok's set:** Damage scales with current HP. At 99 HP and 1 current HP: multiplier = 1 + ((99-1)/100) × (99/100) = 1.9702. At lower Max HP the ceiling is lower.

**PvP Protection Prayer:** If the target has Protect from Melee active, multiply by `6/10` (0.60) at the Gear Bonus stage.

### Step 4: Calculate Effective Attack Level

```
Effective Attack = floor((
    floor( (Attack Level + Boost) × Prayer Bonus ) + Style Bonus + 8
) × Void Bonus)
```

**Style Bonus (addition):**

| Style | Bonus |
|-------|-------|
| Accurate | 3 |
| Controlled | 1 |
| Aggressive / Defensive | 0 |

**Prayer Bonus (multiplier):**

| Prayer | Multiplier |
|--------|------------|
| Clarity of Thought | 1.05 |
| Improved Reflexes | 1.10 |
| Incredible Reflexes | 1.15 |
| Chivalry | 1.15 |
| Piety | 1.20 |

**Void Bonus:** 1.10 if wearing full melee void.

### Step 5: Calculate the Attack Roll

```
Atk Roll = floor( Effective Attack × (Equipment Attack Bonus + 64) × Gear Bonus )
```

The **Equipment Attack Bonus** is the Stab, Slash, or Crush value in the Equipment Stats window, depending on which attack style you are using.

**Gear Bonus** is the same as in Step 2 (slayer helm, salve amulet, PvP protection, etc.).

### Step 6: Calculate Effective Defence Level (Players Only)

```
Effective Defence = floor( (Defence Level + Boost) × Prayer Bonus ) + Style Bonus + 8
```

**Style Bonus (addition):**

| Style | Bonus |
|-------|-------|
| Defensive | 3 |
| Controlled | 1 |
| Accurate / Aggressive | 0 |

### Step 7: Calculate the Defence Roll

**For a monster (NPC):**

```
Def Roll = (Target Defence Level + 9) × (Target Style Defence Bonus + 64)
```

**For a player:**

```
Def Roll = Effective Defence × (Equipment Style Defence Bonus + 64)
```

The **Target Style Defence Bonus** is the target's Stab, Slash, or Crush defence stat, matching the attacker's chosen style.

### Step 8: Calculate Hit Chance

```
If Atk Roll > Def Roll:
    Hit Chance = 1 - (Def Roll + 2) / (2 × (Atk Roll + 1))

Else:
    Hit Chance = Atk Roll / (2 × (Def Roll + 1))
```

### Step 9: Calculate Melee Damage Output

```
Avg Damage per Attack = Hit Chance × ( Max Hit / 2  +  1 / (Max Hit + 1) )
DPS = Avg Damage per Attack / Weapon Speed (seconds)
```

---

## Ranged

| Source | Link |
|--------|------|
| Max Hit | https://oldschool.runescape.wiki/w/Maximum_ranged_hit |
| DPS | https://oldschool.runescape.wiki/w/Damage_per_second/Ranged |

### Step 1: Calculate Effective Ranged Strength

```
Effective Ranged Strength = floor((
    floor( (Ranged Level + Boost) × Prayer Bonus ) + Atk Style + 8
) × Void Modifier)
```

**Atk Style Bonus (addition):**

| Style | Bonus |
|-------|-------|
| Accurate | 3 |
| Rapid / Longrange | 0 |

**Void Modifier:**

| Condition | Multiplier |
|-----------|------------|
| Full ranged void | 1.10 |
| Full elite ranged void | 1.125 |
| No void | 1.00 |

**Prayer Bonus (multiplier):**

| Prayer | Multiplier |
|--------|------------|
| Sharp Eye | 1.05 |
| Hawk Eye | 1.10 |
| Eagle Eye | 1.15 |
| Deadeye | 1.18 |
| Rigour | 1.23 |

### Step 2: Calculate Maximum Ranged Hit

```
Max Hit = floor( floor( 0.5 + Effective Ranged Strength × (Equipment Ranged Strength + 64) / 640 ) × Gear Bonus )
```

**Equipment Ranged Strength** is the "Ranged strength" value shown in Equipment Stats under "Other bonuses".

**Gear Bonus:**

| Condition | Multiplier |
|-----------|------------|
| Black mask (i) / Slayer helm (i) on task | 1.15 |
| Salve amulet (i) vs undead | 7/6 (≈1.167) |
| Salve amulet (ei) vs undead | 1.20 |
| Craw's bow / Webweaver bow (wilderness) | 1.50 |
| Craw's/Webweaver + Slayer on task (additive) | 1.65 |
| PvP: Protect from Missiles | 6/10 (0.60) |

**Black mask and Salve amulet do NOT stack.** Twisted bow damage modifier also multiplies here (see the [Twisted bow page](https://oldschool.runescape.wiki/w/Twisted_bow) for the formula based on opponent Magic level/accuracy). Tbow stacks multiplicatively with slayer/salve.

### Step 3: Calculate Bonus Damage (Special Attacks & Enchanted Bolts)

```
Max Hit = floor( Base Damage × Special Bonus )
```

Bolt effects **only** apply when the special effect activates:

| Attack / Effect | Multiplier |
|-----------------|------------|
| Dark bow + dragon arrows | 1.50 |
| Dark bow + other arrows | 1.30 |
| Zaryte crossbow + enchanted bolts | 1.10 |
| Diamond bolts (e) | 1.15 |
| Dragonstone bolts (e) | 1.45 |
| Onyx bolts (e) | 1.15 |
| Opal bolts (e) | 1.25 |

### Step 4: Calculate Effective Ranged Attack

```
Effective Ranged Attack = floor((
    floor( (Ranged Level + Boost) × Prayer Bonus ) + Atk Style + 8
) × Void Modifier)
```

**Atk Style Bonus (addition):**

| Style | Bonus |
|-------|-------|
| Accurate | 3 |
| Rapid / Longrange | 0 |

**Void Modifier:** 1.10 if wearing either full ranged void or full elite ranged void (both use 1.10 for attack).

**Prayer Bonus (multiplier):**

| Prayer | Multiplier |
|--------|------------|
| Sharp Eye | 1.05 |
| Hawk Eye | 1.10 |
| Eagle Eye | 1.15 |
| Deadeye | 1.18 |
| Rigour | 1.20 |

Note: The only differences between effective ranged strength and effective ranged attack are Rigour (1.23 vs 1.20) and void (strength uses 1.125 for elite, attack uses 1.10 for both).

### Step 5: Calculate the Attack Roll

```
Atk Roll = floor( Effective Ranged Attack × (Equipment Ranged Attack + 64) × Gear Bonus )
```

The **Equipment Ranged Attack** is the "Ranged Attack" value from Equipment Stats.

**Gear Bonus** is the same as in Step 2. Twisted bow accuracy modifier also stacks multiplicatively with slayer/salve bonuses.

### Step 6: Calculate the Defence Roll

```
Def Roll = (Target Defence Level + 9) × (Target Ranged Defence Bonus + 64)
```

**Target Defence Level** is denoted by a shield icon on the target's wiki page.
**Target Ranged Defence** can be found under "Defensive stats".

### Step 7: Calculate Hit Chance

```
If Atk Roll > Def Roll:
    Hit Chance = 1 - (Def Roll + 2) / (2 × (Atk Roll + 1))

Else:
    Hit Chance = Atk Roll / (2 × (Def Roll + 1))
```

### Step 8: Calculate Ranged Damage Output

```
Avg Damage per Hit = Hit Chance × ( Max Hit / 2  +  1 / (Max Hit + 1) )
DPS = Avg Damage per Hit / Weapon Speed (seconds)
```

Note: The rapid attack style decreases attack speed by 1 tick.

---

## Magic

| Source | Link |
|--------|------|
| Max Hit | https://oldschool.runescape.wiki/w/Maximum_magic_hit |
| DPS | https://oldschool.runescape.wiki/w/Damage_per_second/Magic |

### Overview of Magic Max Hit Calculation

All Magic damage starts with a magic attack: a combat spell from a spellbook, a charged powered staff, or a magic special attack. The "base max damage" undergoes several mathematical operations. A floor operation is applied after every step.

The full chain of equations:

```
BaseDamageModifier  = floor( BaseMaxDamage + ChaosGauntlets + Charge )

PrimaryMagicDamage  = floor( BaseDamageModifier × ( 1 + min(1, (VisibleBonuses - Void) × ShadowBonus )
                        + Void + Salve + Avarice + SmokeBattlestaff
                        + VirtusRobesAncientBonus + Prayer ) )
                      + floor( BaseDamageModifier × ElementalWeakness )

PreHitRoll  = floor( floor( floor( floor( PrimaryMagicDamage × (1 + Slayer) )
                      × (1 + SceptreWilderness) )
                      × (1 + AccursedSceptreSpecialAttack) )
                      × (1 + Tomes) )

HitRoll     = floor( max( 1, random(0, PreHitRoll) ) )

PostHitRoll = floor( floor( ( HitRoll + floor( floor(HitRoll × MarkOfDarkness) × DemonbaneEff ) )
                      × (1 + AhrimsDamned) )
                      × (1 + CastleWarsBracelet) )
```

### Base Max Damage

The player's Magic level does **not** affect the max damage for spells, except for **Magic Dart** and **standard spellbook elemental spells** (wind, water, earth — fire is fixed). The max damage for all **powered staves** and **special attacks** does depend on the player's Magic level.

#### Standard Spellbook

| Spell | Base Max |
|-------|----------|
| Wind Strike | 8 |
| Water Strike | 8 |
| Earth Strike | 8 |
| Fire Strike | 8 |
| Wind Bolt | 12 |
| Water Bolt | 12 |
| Earth Bolt | 12 |
| Fire Bolt | 12 |
| Crumble Undead | 15 |
| Wind Blast | 16 |
| Water Blast | 16 |
| Earth Blast | 16 |
| Fire Blast | 16 |
| Iban Blast | 25 |
| Saradomin Strike | 20 (30 with Charge + Saradomin cape) |
| Claws of Guthix | 20 (30 with Charge + Guthix cape) |
| Flames of Zamorak | 20 (30 with Charge + Zamorak cape) |
| Wind Wave | 20 |
| Water Wave | 20 |
| Earth Wave | 20 |
| Fire Wave | 20 |
| Wind Surge | 24 |
| Water Surge | 24 |
| Earth Surge | 24 |
| Fire Surge | 24 |
| Magic Dart | depends on Magic level |

Note: Elemental spells (wind, water, earth) increase to match the highest unlocked spell of that tier once your Magic level is high enough to use it.

#### Ancient Magicks

| Spell | Base Max |
|-------|----------|
| Smoke Rush | 13 |
| Shadow Rush | 14 |
| Blood Rush | 15 |
| Ice Rush | 16 |
| Smoke Burst | 17 |
| Shadow Burst | 18 |
| Blood Burst | 21 |
| Ice Burst | 22 |
| Smoke Blitz | 23 |
| Shadow Blitz | 24 |
| Blood Blitz | 25 |
| Ice Blitz | 26 |
| Smoke Barrage | 27 |
| Shadow Barrage | 28 |
| Blood Barrage | 29 |
| Ice Barrage | 30 |

#### Arceuus Spellbook

| Spell | Base Max |
|-------|----------|
| Ghostly Grasp | 12 |
| Skeletal Grasp | 17 |
| Undead Grasp | 24 |
| Inferior Demonbane | 16 |
| Superior Demonbane | 23 |
| Dark Demonbane | 30 |

### Base Damage Modifier

**Chaos Gauntlets:** If equipped while casting a bolt spell, add **+3**.

**Charge:** If Charge is active with the matching god cape while casting a god spell (Saradomin Strike, Claws of Guthix, or Flames of Zamorak), add **+10**.

### Primary Magic Damage (Additive Phase)

Different bonuses are added together before being multiplied against the base damage modifier.

**Visible Bonuses:** Sum of all magic damage bonuses displayed in Equipment Stats (e.g. Occult necklace, Tormented bracelet, Ancestral robes, etc.), **excluding** elite void's 5%.

**Shadow Bonus:** Tumeken's shadow passive effect.
- ×4 inside Tombs of Amascut
- ×3 outside TOA
- ×1 when not equipped

**min(1, (VisibleBonuses - Void) × ShadowBonus):** Caps the shadow's passive effect at 100%. The shadow does **not** multiply salve, void, or slayer bonuses.

**Void:** Elite void set + void mage helm: add **+5%** (0.05).

**Salve:** Salve amulet(i) vs undead: add **+15%** (0.15). Salve amulet(ei) vs undead: add **+20%** (0.20).

**Avarice:** Amulet of avarice vs revenants: add **+20%** (0.20). With Forinthry Surge active: add an additional +15% for **+35%** total.

**Smoke Battlestaff / Twinflame Staff:** Equipped while casting a standard spellbook spell: add **+10%** (0.10).

**Virtus Robes Ancient Bonus:** Any piece of Virtus robes worn while casting Ancient Magicks: add **+3%** (0.03) per piece.

**Prayer:**

| Prayer | Additive Bonus |
|--------|---------------|
| Mystic Lore | +1% (0.01) |
| Mystic Might | +2% (0.02) |
| Mystic Vigour | +3% (0.03) |
| Augury | +4% (0.04) |

**Elemental Weakness:** Computed separately as `floor( BaseDamageModifier × ElementalWeakness )` and added to the PrimaryMagicDamage total. Due to floor operations being applied twice (once for gear bonuses and again for elemental weakness), the final max hit may be lower than expected.

### Pre Hit Roll (Multiplicative Phase)

Each bonus is sequentially multiplied then rounded down.

**Slayer:** Black mask (i) / Slayer helm (i) while attacking the player's current slayer task, and **NOT** wearing an amulet of avarice or salve amulet (or at least not attacking revenants/undead): multiply by **1.15**.

**Sceptre Wilderness:** Wielding a charged Thammaron's sceptre / Accursed sceptre (or their autocast variants) and attacking in the Wilderness: multiply by **1.50**.

**Accursed Sceptre Special Attack:** Using the special attack of a charged Accursed sceptre: multiply by **1.50**. (Even with autocast, the special attack uses the sceptre's built-in spell.)

**Tomes:**

| Tome | Spell Type | PvM | PvP |
|------|-----------|-----|-----|
| Tome of Fire | Fire spells (standard spellbook) | ×1.10 | ×1.50 |
| Tome of Water | Water spells (standard spellbook) | ×1.10 | ×1.20 |
| Tome of Earth | Earth spells (standard spellbook) | ×1.10 | — |

### Hit Roll

```
HitRoll = floor( max( 1, random(0, PreHitRoll) ) )
```

A random integer from 0 to PreHitRoll (inclusive). Zero is changed to 1.

### Post Hit Roll

Each modifier is applied sequentially, multiplied, and rounded down.

**Mark of Darkness:** If cast by the player and active when casting a Demonbane spell from the Arceuus spellbook: multiply added damage by **1.25**. With a Purging staff: multiply by **1.50** instead.

**Demonbane Effectiveness:** Multiply the added Mark of Darkness damage by the demonic enemy's demonbane effectiveness percentage (baseline is 100%).

**Ahrim's Damned:** Ahrim's set + Amulet of the damned equipped: 25% chance for any magic attack to deal **+30%** extra damage. This effect never triggers at a combat dummy. Multiply by **1.30**.

**Castle Wars Bracelet:** Equipped at the start of Castle Wars and attacking the flag bearer: multiply by **1.20**.

**Twinflame Staff:** When casting a bolt, blast, or wave spell with the Twinflame staff, a second hit deals **40%** of the initial damage. Multiply by **1.40** for the second hit.

### Effective Magic Level (for Accuracy)

```
Effective Magic = floor( floor( (Magic Level + Boost) × Prayer Effect ) × VoidMagic + Style + 9 )
```

**VoidMagic:** 1.45 if wearing full void mage set.

**Style (addition, powered staves only):**

| Style | Bonus |
|-------|-------|
| Accurate | 3 |
| Longrange | 1 |
| Other (or non-powered staff) | 0 |

**Prayer Multiplier:**

| Prayer | Multiplier |
|--------|------------|
| Mystic Will | 1.05 |
| Mystic Lore | 1.10 |
| Mystic Might | 1.15 |
| Mystic Vigour | 1.18 |
| Augury | 1.25 |

Note: Temporarily increasing Magic level only increases accuracy, not max hit (except for Magic Dart, salamanders, trident of the seas/swamp, and sanguinesti staff).

### Magic Accuracy Roll

```
Acc Roll = floor( Effective Magic × (Equipment Magic Attack + 64) × Gear Bonus )
```

**Equipment Magic Attack** is the Magic Attack value from Equipment Stats.

**Gear Bonus:** Multiply by 1.15 if wearing a slayer helm (i) on task, or killing undead with an imbued salve amulet.

### Magic Defence Roll

```
Def Roll = (9 + NPC Magic Level) × (NPC Magic Defence + 64)
```

### Magic Hit Chance

```
If Acc Roll > Def Roll:
    Hit Chance = 1 - (Def Roll + 2) / (2 × (Acc Roll + 1))

Else:
    Hit Chance = Acc Roll / (2 × (Def Roll + 1))
```

### Magic Damage Output

```
Avg Damage per Hit = Hit Chance × ( Max Hit / 2  +  1 / (Max Hit + 1) )
DPS = Avg Damage per Hit / Spell Speed (seconds)
```

**Spell Speed:** Standard and Ancient spellbook spells have a 5-tick (3.0s) attack speed. Powered staves (trident, sanguinesti, shadow) have a 4-tick (2.4s) attack speed.

For AOE (burst/barrage) spells, multiply DPS by the number of targets hit (max 9).

---

## References

- [Maximum melee hit — OSRS Wiki](https://oldschool.runescape.wiki/w/Maximum_melee_hit)
- [Maximum ranged hit — OSRS Wiki](https://oldschool.runescape.wiki/w/Maximum_ranged_hit)
- [Maximum magic hit — OSRS Wiki](https://oldschool.runescape.wiki/w/Maximum_magic_hit)
- [Damage per second / Melee — OSRS Wiki](https://oldschool.runescape.wiki/w/Damage_per_second/Melee)
- [Damage per second / Ranged — OSRS Wiki](https://oldschool.runescape.wiki/w/Damage_per_second/Ranged)
- [Damage per second / Magic — OSRS Wiki](https://oldschool.runescape.wiki/w/Damage_per_second/Magic)
- [Successful hit — OSRS Wiki](https://oldschool.runescape.wiki/w/Successful_hit)
- [Temporary skill boost — OSRS Wiki](https://oldschool.runescape.wiki/w/Temporary_skill_boost)
