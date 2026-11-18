# TinyForge — chess bounty research prototype

Official bounty: https://make.fun/bounty/tiny-chess-01 (deadline **2026-11-24 17:00 UTC**).

## Current code
`engine.py` is a dependency-free Python UCI prototype, with board parsing, legal move generation, castling, en passant, promotion and alpha-beta search. Search now propagates castling and en-passant rights through recursive plies. Run `python engine.py` for local UCI testing or `python -m unittest discover -s tests -v` for local tests.

## Critical official-rule blockers
The official bounty **does not use UCI over stdin as its submission interface**. The submitted `main.py` must interact with the house HTTP environment at `MAKEFUN_ENV_URL`, using routes specified in the official downloadable kit. That kit and its route schema have not yet been verified here.

The rules require **root `main.py` <= 4,096 bytes**, and **the entire submitted repository snapshot <= 8,192 bytes, with no individual file over 4,096 bytes**. The current development repository exceeds these caps and has no `main.py`. Tests, this README and the existing development engine cannot all be included in the final snapshot. Prepare a separate minimal submission snapshot/branch after verifying the kit; do not assume a Python UCI wrapper qualifies.

Other requirements: Python 3.13 standard library only; deterministic fixed-depth/node search; <=10 seconds per move; <=1,800 seconds per trial; practice Elo >=1,154 to reach the final. To win a prize the entry must beat the sunfish house baseline. Actual match strength is unknown.

Submission also requires authentic AI coding-agent transcripts. No official practice trial, Python 3.13 verification, or competition submission has been completed.

## Next priorities
1. Obtain and inspect official kit and env HTTP route schema.
2. Build standalone <=4096-byte `main.py` implementing the real HTTP trial protocol and robust legal chess.
3. Run local Python tests, perft comparisons and deterministic game trials; measure source and snapshot bytes.
4. Test against the official practice gauntlet, then decide whether to submit with the user's approval.
