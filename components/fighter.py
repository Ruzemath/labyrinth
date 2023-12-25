from __future__ import annotations
from typing import TYPE_CHECKING
from components.base_component import BaseComponent
from input_handler import GameOverEventHandler
from render_order import RenderOrder
import color
if TYPE_CHECKING:
    from entities import Actor

class Fighter(BaseComponent):
    parent: Actor
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()
            
    def die(self) -> None:
        if self.generate.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
            self.generate.event_handle = GameOverEventHandler(self.generate)
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE     
    
    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp
        self.hp = new_hp_value
        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
    