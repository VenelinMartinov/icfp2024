import argparse
import os
from pathlib import Path
import time
import requests
import ascii_helpers
import decode as d

from ast_eval import Evaluator

TOKEN = os.getenv("TOKEN")


def send_msg(msg: str, raw: bool = False) -> str:
    encoded = "S" + ascii_helpers.encode_string(msg)

    resp = requests.post(
        "https://boundvariable.space/communicate",
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=10,
        data=encoded,
    )

    resp.raise_for_status()

    resp_toks = resp.text.split()

    if raw:
        return resp.text

    tokens = [d.parse_token(tok) for tok in resp_toks]
    res = Evaluator().eval_tokens(tokens)

    return str(res)


def get_course(title: str, length: int) -> None:
    course_dir = Path(title)
    course_dir.mkdir(exist_ok=True)

    for i in range(0, length):
        time.sleep(0.5)
        try:
            resp = send_msg(f"get {title}{i}")
            (course_dir / Path(f"{title}{i}")).write_text(resp)
        except IndexError:
            resp = send_msg(f"get {title}{i}", raw=True)
            (course_dir / Path(f"{title}{i}.raw")).write_text(resp)


def decode_raw(title: str) -> None:
    course_dir = Path(title)
    course_dir.mkdir(exist_ok=True)

    course_files = next(course_dir.walk())[2]
    raw_files = [f for f in course_files if f.endswith(".raw")]

    for raw in raw_files:
        raw_file = course_dir / raw
        encoded_tokens = raw_file.read_text().split()
        tokens = [d.parse_token(tok) for tok in encoded_tokens]
        res = Evaluator().eval_tokens(tokens)

        decoded_file = course_dir / raw.rstrip(".raw")
        decoded_file.write_text(str(res))


def send_solutions(title: str) -> None:
    course_dir = Path(title)
    course_dir.mkdir(exist_ok=True)

    course_files = next(course_dir.walk())[2]
    solution_files = [f for f in course_files if f.endswith("_solution")]

    for solution in solution_files:
        name = solution.rstrip("_solution")
        path = (course_dir / solution).read_text()
        resp = send_msg(f"solve {name} {path}")
        print(resp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("msg", nargs="+")
    ap.add_argument("--raw", action="store_true")
    args = ap.parse_args()

    print(send_msg("".join(args.msg), raw=args.raw))


if __name__ == "__main__":
    main()
    # decode_raw("lambdaman")
    # send_solutions("spaceship")
