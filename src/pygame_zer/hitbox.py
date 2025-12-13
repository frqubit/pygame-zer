from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import Type, TypeAlias, TypeVar

from pygame_zer.types import Vec2f, Vec2fAble


class CollideResult(Enum):
    NO = 0
    YES = 1
    UNSURE = 2

    @staticmethod
    def for_sure(value: bool):
        return CollideResult.YES if value else CollideResult.NO

    def __bool__(self):
        return self == CollideResult.YES


AnyHitbox = TypeVar("AnyHitbox", bound="Hitbox")

CollisionMap: TypeAlias = dict[str, Callable[[AnyHitbox], CollideResult]]


class Hitbox:
    def __init__(
        self,
        variant: str,
        collides_map: CollisionMap,
        contains_map: CollisionMap,
    ):
        self._variant = variant
        self._collides_map = collides_map
        self._contains_map = contains_map

    @staticmethod
    def none():
        class NoHitbox(Hitbox):
            def collides_point(self, pt: Vec2f) -> CollideResult:
                return CollideResult.UNSURE

        return NoHitbox("", {}, {})

    @abstractmethod
    def contains_point(self, pt: Vec2fAble) -> CollideResult:
        raise NotImplementedError("Hitbox is an abstract class")

    def collides_hitbox(self, hitbox: Hitbox) -> CollideResult:
        if hitbox._variant in self._collides_map:
            return self._collides_map[hitbox._variant](hitbox)
        elif self._variant in hitbox._collides_map:
            return hitbox._collides_map[self._variant](self)
        return CollideResult.UNSURE

    def contains_hitbox(self, hitbox: Hitbox) -> CollideResult:
        if hitbox._variant in self._contains_map:
            return self._contains_map[hitbox._variant](hitbox)
        return CollideResult.UNSURE
