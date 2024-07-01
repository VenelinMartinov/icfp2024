from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def dv_from_direction(direction: int) -> tuple[int, int]:
    dvy = 0
    dvx = 0

    if direction in [1, 2, 3]:
        dvy = -1
    if direction in [3, 6, 9]:
        dvx = 1
    if direction in [7, 8, 9]:
        dvy = 1
    if direction in [1, 4, 7]:
        dvx = -1

    return dvx, dvy


def init_list() -> list[tuple[int, int]]:
    return [(0, 0)]


@dataclass
class Spaceship:
    vx: int = 0
    vy: int = 0
    x: int = 0
    y: int = 0

    path: list[tuple[int, int]] = field(default_factory=init_list)

    def move(self, direction: int) -> Spaceship:
        if direction > 9 or direction < 1:
            raise ValueError(f"Wrong direction {direction}")
        new_ship = Spaceship(self.vx, self.vy, self.x, self.y, path=self.path.copy())

        dvx, dvy = dv_from_direction(direction)

        new_ship.vx += dvx
        new_ship.vy += dvy
        new_ship.x += new_ship.vx
        new_ship.y += new_ship.vy

        new_ship.path.append((new_ship.x, new_ship.y))

        return new_ship

    def walk_path(self, dirs: str) -> Spaceship:
        new_ship = Spaceship(self.vx, self.vy, self.x, self.y, path=self.path.copy())
        for step in dirs:
            direction = int(step)
            new_ship = new_ship.move(direction)

        return new_ship


def is_subseq(main: list[tuple[int, int]], secondary: list[tuple[int, int]]) -> bool:
    index = 0
    for p in main:
        if p == secondary[index]:
            index += 1
            if index == len(secondary) - 1:
                return True

    return False
