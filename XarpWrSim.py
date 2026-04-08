import random
import statistics
from dataclasses import dataclass
from typing import Dict, List, Optional, Union


# =========================
# USER CONFIG (plug values)
# =========================

TEAM_SIZE = 3
BOSS_MAX_HP = 3810

# Tie/break target (seconds)
WR_TIME_SECONDS = 116.2
TICK_SECONDS = 0.6

# How many simulations
NUM_RUNS = 10000
RNG_SEED = 42

# Damage randomness around avg damage.
# 0.0 = fully deterministic, 0.20 = ± typical variance around avg
DEFAULT_SPREAD = 0.20

# Thrall model (for full WR window):
# 3 thralls, each attacks every 4 ticks, each hit is uniform 0..3 damage.
# Over 116.2s this is ~144 total hits => E[damage]≈216, std≈13.4.
ENABLE_THRALLS = True
THRALL_COUNT = 3
THRALL_START_TICK = 1
THRALL_INTERVAL_TICKS = 4
THRALL_HIT_MIN = 0
THRALL_HIT_MAX = 3

# Optional per-player first action delay (ticks)
# Keep all 0 unless you want staggered starts.
START_TICK_BY_PLAYER = [0, 0, 0]


# Opening: exactly 2 attacks per player.
# You can set either a single value for everyone or per-player list.
# weapon: string key from WEAPON_SPEED_TICKS
# avg_damage: float or [p1, p2, p3]
OPENING_SEQUENCE = [
    {"weapon": ["elder_maul", "elder_maul", "elder_maul"], "avg_damage": [40.0, 40.0, 40.0], "spec": True},
    {"weapon": ["elder_maul", "elder_maul", "elder_maul"], "avg_damage": [40.0, 40.0, 40.0], "spec": True},
    {"weapon": ["zcb", "zcb", "zcb"], "avg_damage": [110.0, 110.0, 110.0], "spec": True},
]

# Body phase: all scythe swings (you plug avg and your def estimate)
BODY_WEAPON = "scythe"
BODY_AVG_DAMAGE = 45.0
BODY_DEF_ESTIMATE = 69  # informational print only

# Execution trigger: when boss HP <= threshold, each player does one final attack.
EXECUTION_HP_THRESHOLD = 420

# Execution attack config per player.
# weapon/scythe + spec flag as needed.
EXECUTION_ATTACKS = [
    {"weapon": "claws", "avg_damage": 72.0, "spec": True},
    {"weapon": "claws", "avg_damage": 72.0, "spec": True},
    {"weapon": "scythe", "avg_damage": 45.0, "spec": False},
]


# =========================
# Internal configuration
# =========================

WEAPON_SPEED_TICKS: Dict[str, int] = {
    "scythe": 5,
    "claws": 4,
    "dragon_claws": 4,
    "chally": 4,
    "crystal_halberd": 4,
    "dds": 4,
    "dragon_dagger": 4,
    "bgs": 6,
    "elder_maul": 6,
    "zcb": 5,
}


@dataclass
class PlayerState:
    next_tick: int
    opening_index: int = 0
    used_execution: bool = False


def _get_for_player(value: Union[float, str, List[Union[float, str]]], player_idx: int):
    if isinstance(value, list):
        return value[player_idx]
    return value


def _weapon_speed(weapon_name: str) -> int:
    key = weapon_name.lower().strip()
    if key not in WEAPON_SPEED_TICKS:
        raise ValueError(f"Unknown weapon '{weapon_name}'. Add it to WEAPON_SPEED_TICKS.")
    return WEAPON_SPEED_TICKS[key]


def _roll_damage(avg_damage: float, rng: random.Random, spread: float = DEFAULT_SPREAD) -> float:
    if spread <= 0:
        return max(0.0, avg_damage)
    std = max(0.01, avg_damage * spread)
    dmg = rng.gauss(avg_damage, std)
    return max(0.0, dmg)


def _build_attack_for_player(attack_cfg: dict, player_idx: int) -> dict:
    weapon = _get_for_player(attack_cfg["weapon"], player_idx)
    avg_damage = float(_get_for_player(attack_cfg["avg_damage"], player_idx))
    spec = bool(attack_cfg.get("spec", False))
    return {
        "weapon": weapon,
        "avg_damage": avg_damage,
        "spec": spec,
        "speed": _weapon_speed(str(weapon)),
    }


def run_one_sim(rng: random.Random) -> dict:
    wr_tick_limit = WR_TIME_SECONDS / TICK_SECONDS

    boss_hp = float(BOSS_MAX_HP)
    players = [PlayerState(next_tick=START_TICK_BY_PLAYER[i]) for i in range(TEAM_SIZE)]
    thrall_next_ticks = [THRALL_START_TICK for _ in range(THRALL_COUNT)] if ENABLE_THRALLS else []

    current_tick = 0
    total_damage = 0.0
    thrall_total_damage = 0.0
    thrall_total_hits = 0

    while boss_hp > 0 and current_tick <= wr_tick_limit:
        next_player_tick = min(p.next_tick for p in players)
        next_thrall_tick = min(thrall_next_ticks) if ENABLE_THRALLS else float("inf")
        active_tick = min(next_player_tick, next_thrall_tick)
        if active_tick > wr_tick_limit:
            break

        current_tick = active_tick

        for i, p in enumerate(players):
            if p.next_tick != current_tick or boss_hp <= 0:
                continue

            # Phase selection
            if p.opening_index < len(OPENING_SEQUENCE):
                attack = _build_attack_for_player(OPENING_SEQUENCE[p.opening_index], i)
                p.opening_index += 1
            elif (not p.used_execution) and boss_hp <= EXECUTION_HP_THRESHOLD:
                attack = _build_attack_for_player(EXECUTION_ATTACKS[i], i)
                p.used_execution = True
            else:
                attack = {
                    "weapon": BODY_WEAPON,
                    "avg_damage": float(BODY_AVG_DAMAGE),
                    "spec": False,
                    "speed": _weapon_speed(BODY_WEAPON),
                }

            hit = _roll_damage(attack["avg_damage"], rng)
            boss_hp -= hit
            total_damage += hit
            p.next_tick = current_tick + attack["speed"]

        # Thrall hits on their scheduled ticks.
        if ENABLE_THRALLS and boss_hp > 0:
            for t in range(THRALL_COUNT):
                if thrall_next_ticks[t] != current_tick:
                    continue
                thrall_hit = rng.randint(THRALL_HIT_MIN, THRALL_HIT_MAX)
                boss_hp -= thrall_hit
                total_damage += thrall_hit
                thrall_total_damage += thrall_hit
                thrall_total_hits += 1
                thrall_next_ticks[t] = current_tick + THRALL_INTERVAL_TICKS

    killed = boss_hp <= 0
    kill_time_sec = (current_tick * TICK_SECONDS) if killed else None
    tied_or_broke = bool(killed and kill_time_sec <= WR_TIME_SECONDS)
    strictly_broke = bool(killed and kill_time_sec < WR_TIME_SECONDS)

    return {
        "killed": killed,
        "kill_time_sec": kill_time_sec,
        "tied_or_broke": tied_or_broke,
        "strictly_broke": strictly_broke,
        "remaining_hp": max(0.0, boss_hp),
        "total_damage": total_damage,
        "thrall_damage": thrall_total_damage,
        "thrall_hits": thrall_total_hits,
    }


def summarize(results: List[dict]) -> None:
    kills = [r for r in results if r["killed"]]
    kill_times = [r["kill_time_sec"] for r in kills if r["kill_time_sec"] is not None]

    tied_or_broke_count = sum(1 for r in results if r["tied_or_broke"])
    strictly_broke_count = sum(1 for r in results if r["strictly_broke"])
    kill_count = len(kills)

    rem_hp_avg = statistics.mean(r["remaining_hp"] for r in results)
    dmg_avg = statistics.mean(r["total_damage"] for r in results)
    dmg_max = max(r["total_damage"] for r in results)
    thrall_avg = statistics.mean(r["thrall_damage"] for r in results)
    thrall_std = statistics.pstdev(r["thrall_damage"] for r in results)
    thrall_hits_avg = statistics.mean(r["thrall_hits"] for r in results)

    print("=" * 90)
    print("XARP WR SIM")
    print("=" * 90)
    print(f"Team size: {TEAM_SIZE}")
    print(f"Boss HP: {BOSS_MAX_HP}")
    print(f"WR time target: {WR_TIME_SECONDS:.2f}s")
    print(f"Body weapon: {BODY_WEAPON}, body avg dmg: {BODY_AVG_DAMAGE:.2f}, def est: {BODY_DEF_ESTIMATE}")
    print(f"Execution threshold HP: {EXECUTION_HP_THRESHOLD}")
    if ENABLE_THRALLS:
        print(
            f"Thralls: {THRALL_COUNT} active, {THRALL_HIT_MIN}-{THRALL_HIT_MAX} dmg every {THRALL_INTERVAL_TICKS} ticks"
        )
    print(f"Runs: {len(results)}")
    print()

    print(f"Kill rate: {kill_count}/{len(results)} ({(kill_count/len(results))*100:.2f}%)")
    print(f"Tie or break WR rate: {tied_or_broke_count}/{len(results)} ({(tied_or_broke_count/len(results))*100:.2f}%)")
    print(f"Strict break WR rate: {strictly_broke_count}/{len(results)} ({(strictly_broke_count/len(results))*100:.2f}%)")
    print(f"Avg total damage by timer end: {dmg_avg:.2f}")
    print(f"Max total damage observed: {dmg_max:.2f}")
    print(f"Avg remaining HP by timer end: {rem_hp_avg:.2f}")
    if ENABLE_THRALLS:
        print(f"Avg thrall damage: {thrall_avg:.2f}")
        print(f"Thrall damage std dev: {thrall_std:.2f}")
        print(f"Avg thrall attacks landed: {thrall_hits_avg:.1f}")

    if kill_times:
        kill_times_sorted = sorted(kill_times)
        p50 = kill_times_sorted[int(0.50 * (len(kill_times_sorted) - 1))]
        p10 = kill_times_sorted[int(0.10 * (len(kill_times_sorted) - 1))]
        p90 = kill_times_sorted[int(0.90 * (len(kill_times_sorted) - 1))]
        print()
        print("Kill-time stats (kills only):")
        print(f"- Min: {min(kill_times):.2f}s")
        print(f"- P10: {p10:.2f}s")
        print(f"- P50: {p50:.2f}s")
        print(f"- P90: {p90:.2f}s")
        print(f"- Max: {max(kill_times):.2f}s")


def validate_config():
    if TEAM_SIZE != 3:
        raise ValueError("Current config expects TEAM_SIZE=3 because opening/execution examples are per 3 players.")
    if len(OPENING_SEQUENCE) != 3:
        raise ValueError("OPENING_SEQUENCE must have exactly 3 attacks (your opener has 3 attacks).")
    if len(START_TICK_BY_PLAYER) != TEAM_SIZE:
        raise ValueError("START_TICK_BY_PLAYER length must match TEAM_SIZE.")
    if len(EXECUTION_ATTACKS) != TEAM_SIZE:
        raise ValueError("EXECUTION_ATTACKS length must match TEAM_SIZE.")
    if ENABLE_THRALLS:
        if THRALL_COUNT < 0:
            raise ValueError("THRALL_COUNT must be >= 0.")
        if THRALL_INTERVAL_TICKS <= 0:
            raise ValueError("THRALL_INTERVAL_TICKS must be > 0.")
        if THRALL_HIT_MIN > THRALL_HIT_MAX:
            raise ValueError("THRALL_HIT_MIN cannot be greater than THRALL_HIT_MAX.")


def main():
    validate_config()
    rng = random.Random(RNG_SEED)
    results = [run_one_sim(rng) for _ in range(NUM_RUNS)]
    summarize(results)


if __name__ == "__main__":
    main()
