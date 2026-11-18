# TinyForge — Chess 4 KB bounty entry (work in progress)

A dependency-free Python UCI chess engine prototype. Supports board parsing, legal move generation, check detection, castling, en passant, promotion, and alpha-beta search (depth 1–5).

## Run

```sh
python engine.py
```

Send UCI commands such as:

```
uci
isready
position startpos moves e2e4 e7e5
go depth 3
quit
```

## Tests

```sh
python -m unittest discover -s tests -v
```

## Competition blockers

- **Source size currently 4,888 bytes**, above the presumed 4,096-byte target. Must reduce below the official measured limit and verify the precise counting rule.
- UCI is a minimal subset. Search does not propagate castling rights or en passant to deeper plies; this can affect tactical accuracy. No time management, quiescence search, repetition detection or fifty-move rule.
- No official make.fun kit/test suite or rating benchmark has been verified.
- No verified GitHub Actions test result or actual tournament result yet.
- Native coding-agent provenance and any submission eligibility remain unverified.

Do not submit as competition-ready until these are resolved.
