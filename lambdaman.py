from __future__ import annotations
from enum import Enum


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


class GridElement(Enum):
    WALL = "#"
    PILL = "."
    EMPTY = "_"
    LAMBDAMAN = "L"


def _step(y: int, x: int, direction: Direction) -> tuple[int, int]:
    if direction == Direction.UP:
        return y - 1, x
    elif direction == Direction.DOWN:
        return y + 1, x
    elif direction == Direction.LEFT:
        return y, x - 1
    elif direction == Direction.RIGHT:
        return y, x + 1
    else:
        raise ValueError(f"Invalid direction {direction}")


class Grid:
    def __init__(self, grid_str: str) -> None:
        rows = grid_str.strip().split("\n")
        self.grid = [[GridElement(cell) for cell in row] for row in rows]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def _index_in_range(self, y: int, x: int) -> bool:
        if y < 0 or y > self.height - 1 or x < 0 or x > self.width - 1:
            return False
        return True

    def __getitem__(self, key: tuple[int, int]) -> GridElement:
        y, x = key

        if not self._index_in_range(y, x):
            raise ValueError(f"location outside of grid {key}")
        return self.grid[y][x]

    def __setitem__(self, key: tuple[int, int], value: GridElement) -> None:
        y, x = key
        self.grid[y][x] = value

    def __str__(self) -> str:
        res = ""
        for row in self.grid:
            res += "".join(cell.value for cell in row) + "\n"

        return res

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            return False

        return self.grid == other.grid

    def is_solved(self) -> bool:
        for row in self.grid:
            for cell in row:
                if cell == GridElement.PILL:
                    return False

        return True

    def lambdaman_loc(self) -> tuple[int, int]:
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == GridElement.LAMBDAMAN:
                    return (y, x)

        raise ValueError("No lambdaman found")

    def walk_path(self, path: str) -> Grid:
        y, x = self.lambdaman_loc()

        grid_copy = Grid(str(self))

        for direction in path:
            if grid_copy.lambdaman_loc() != (y, x):
                raise ValueError(
                    f"WRONG LAMBDAMAN LOC {grid_copy.lambdaman_loc()}, "
                    f"expected {(y, x)}, grid \n{grid_copy}"
                )
            new_y, new_x = _step(y, x, Direction(direction))

            if not self._index_in_range(new_y, new_x):
                continue

            match grid_copy[new_y, new_x]:
                case GridElement.WALL:
                    continue
                case GridElement.PILL:
                    grid_copy[new_y, new_x] = GridElement.LAMBDAMAN
                    grid_copy[y, x] = GridElement.EMPTY
                case GridElement.EMPTY:
                    grid_copy[new_y, new_x] = GridElement.LAMBDAMAN
                    grid_copy[y, x] = GridElement.EMPTY
                case _:
                    raise ValueError(f"Invalid cell {grid_copy[new_y, new_x]}")

            y, x = new_y, new_x

        return grid_copy


def _get_paths_to_visit(path: str) -> list[str]:
    return [path + direction.value for direction in Direction]


def find_path(grid: Grid, shortest: bool = True) -> str:
    seen: dict[str, tuple[int, str]] = {}
    solved: dict[int, str] = {}

    paths_to_visit = _get_paths_to_visit("")
    while paths_to_visit:
        path = paths_to_visit.pop(-1)

        new_grid = grid.walk_path(path)
        # print(f"walking {path}\n{new_grid}")

        if str(new_grid) in seen:
            continue

        seen[str(new_grid)] = len(path), path

        if new_grid.is_solved():
            if not shortest:
                return path
            solved[len(path)] = path
        else:
            paths_to_visit += _get_paths_to_visit(path)

    sorted_solved = [item[1] for item in sorted(solved.items(), key=lambda x: x[0])]

    return sorted_solved[0]
