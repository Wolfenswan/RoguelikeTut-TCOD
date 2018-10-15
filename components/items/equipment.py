from typing import Optional, Tuple

from dataclasses import dataclass

from components.items.moveset import Moveset


@dataclass
class Equipment():
    e_to: str
    dmg_potential: Optional[Tuple]
    av: Optional[int]
    block_def: Optional[int]
    qu_slots: Optional[int]
    attack_range: Optional[Tuple]
    l_radius: Optional[int]
    two_handed: Optional[bool]
    attack_type: Optional[str]
    moveset: Optional[Moveset]

    @property
    def name(self):
        return self.owner.owner.name

    @property
    def full_name(self):
        return self.owner.owner.full_name

    @property
    def color(self):
        return self.owner.owner.color