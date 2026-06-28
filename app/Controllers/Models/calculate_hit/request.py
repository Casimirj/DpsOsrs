from pydantic import BaseModel, ConfigDict, Field

from .monster import MonsterInput


class CalculateHitInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    weapon: str = Field(alias="Weapon")
    monster: MonsterInput = Field(alias="Monster")
    scale: int = Field(alias="Scale")
