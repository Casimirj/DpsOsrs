from app.Controllers.Models.calculate_hit import CalculateHitInput
from app.Monsters import Bloat, Maiden, P1Verzik, P2Verzik, P3Verzik, Sotetseg, Xarpus
from app.Loadouts import OathTorvaRancour
from app.Weapons.Scythe import Scythe


MONSTER_CLASSES = {
    "Bloat": Bloat,
    "Maiden": Maiden,
    "P1Verzik": P1Verzik,
    "P2Verzik": P2Verzik,
    "P3Verzik": P3Verzik,
    "Sotetseg": Sotetseg,
    "Xarpus": Xarpus,
}


def calculate_hit_damage(payload: CalculateHitInput) -> tuple[int, int]:
    monster_name = payload.monster.name

    if monster_name not in MONSTER_CLASSES:
        raise ValueError(f"Unknown monster: {monster_name}")

    monster = MONSTER_CLASSES[monster_name](scale=payload.scale)

    if payload.monster.reduce_defense:
        monster.stats.def_level = int(payload.monster.defense)

    weapon_name = payload.weapon

    if weapon_name == "Scythe of Vitur":
        player = OathTorvaRancour.player
        player.equip_weapon(Scythe())
        damage = player.do_attack(monster)
    else:
        damage = payload.scale

    return damage, monster.stats.def_level
