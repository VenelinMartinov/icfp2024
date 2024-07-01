from pathlib import Path
import pytest
from spaceship import Spaceship, is_subseq


def get_spaceship_content(num: int) -> list[tuple[int, int]]:
    content = Path(f"spaceship/spaceship{num}").read_text(encoding="utf-8")
    content = content.strip()

    lines = [line.split() for line in content.splitlines()]
    points = [(int(p[0]), int(p[1])) for p in lines]
    return points


def get_spaceship_solution(num: int) -> str:
    solution_file = Path(f"spaceship/spaceship{num}_solution")
    if not solution_file.exists():
        return ""
    return solution_file.read_text(encoding="utf-8")


def test_example():
    path = [(0, 0), (0, -1), (1, -3), (3, -5), (6, -7), (9, -9), (13, -10)]
    dirs = "236659"

    end_ship = Spaceship().walk_path(dirs)
    assert end_ship.path == path


def test_subpath():
    path: list[tuple[int, int]] = [
        (0, 0),
        (0, -1),
        (1, -3),
        (3, -5),
        (6, -7),
        (9, -9),
        (13, -10),
    ]

    subpath: list[tuple[int, int]] = [(0, 0), (6, -7)]

    assert is_subseq(path, subpath)


@pytest.mark.parametrize("i", range(1, 11))
def test_spaceship(i: int):
    cont = get_spaceship_content(i)
    sol = get_spaceship_solution(i)

    if not sol:
        pass
        # # record
        # sol = find_path(cont)
        # solution_file = Path(f"spaceship/spaceship{i}_solution")
        # solution_file.write_text(sol, encoding="utf-8")
    else:
        assert is_subseq(Spaceship().walk_path(sol).path, cont)
