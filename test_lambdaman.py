import pytest
from pathlib import Path

from lambdaman import Grid, find_path


def get_lambdaman_content(num: int) -> str:
    content = Path(f"lambdaman/lambdaman{num}").read_text(encoding="utf-8")
    content = content.strip()
    return content


def get_lambdaman_solution(num: int) -> str:
    solution_file = Path(f"lambdaman/lambdaman{num}_solution")
    if not solution_file.exists():
        return ""
    return solution_file.read_text(encoding="utf-8")


def test_repr():
    grid_str = "#####\n#L..#\n#...#\n#####\n"
    grid = Grid(grid_str)
    assert str(grid) == grid_str


def test_example_walk():
    grid = Grid("###.#...\n...L..##\n.#######")
    end_grid = grid.walk_path("LLLDURRRUDRRURR")
    assert end_grid.is_solved()


@pytest.mark.parametrize("i", range(9, 22))
@pytest.mark.timeout(60)
def test_lambdaman(i: int):
    cont = get_lambdaman_content(i)
    grid = Grid(cont)
    sol = get_lambdaman_solution(i)

    if not sol:
        sol = find_path(grid, shortest=False)
        solution_file = Path(f"lambdaman/lambdaman{i}_solution")
        solution_file.write_text(sol, encoding="utf-8")

    else:
        assert grid.walk_path(sol).is_solved()
