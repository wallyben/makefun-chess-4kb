# TinyForge competition completion checklist

Deadline: 2026-11-24 17:00 UTC. Check boxes only with a reproducible evidence link or commit. Do not confuse a passing CI workflow with chess strength.

## 1. Establish baseline
- [ ] Complete all three Stockfish candidates (run 44898272468; tactical job still running at last inspection).
- [ ] Select strongest candidate from completed-game results; require sufficient evidence.
- [ ] Record W/D/L, unfinished, crashes, illegal moves, and per-move latency (latency instrumentation missing).

## 2. Competitive engine
- [ ] Verify castling, en passant, promotions, checkmate and stalemate.
- [ ] Implement compact alpha-beta pruning.
- [ ] Implement move ordering.
- [ ] Implement bounded quiescence search.
- [ ] Implement iterative deepening and strict move deadline.
- [ ] Implement compact pawn/king/positional evaluation.

## 3. Distillation
- [ ] Curate licensed representative opening/middlegame/endgame positions.
- [x] Generate reproducible Stockfish teacher evaluations (run 44898196403; depth 9, 160 positions, 120 train/40 holdout).
- [ ] Tune parameters with holdout improvement (run 44898196403 failed this criterion).
- [ ] Verify distilled candidate wins paired matches.

## 4. Strength and correctness
- [ ] Special-rule regression suite.
- [ ] Verify <=10s per move under target environment.
- [ ] Beat previous champion in reproducible paired matches.
- [ ] Larger Stockfish benchmark.
- [ ] Sunfish 4KB comparison.
- [ ] Official practice >=1154 Elo.

## 5. Submission
- [ ] Check every file <=4096 bytes, main.py <=4096, snapshot <=8192.
- [ ] Verify Python 3.13 and exact JSON/HTTP protocol.
- [ ] Authentic transcripts and provenance.
- [ ] Freeze best proven candidate.
- [ ] Official submission accepted.
- [ ] Preserve receipt and submitted commit.

## Verified partial evidence
- Original candidate: 3790 bytes on submission-minimal.
- Mobility challenger: 3810 bytes; teacher holdout did not improve.
- Tactical challenger: 3867 bytes, commit fed34df; pending benchmark.
- 20-game Stockfish test (run 44898272468): original 2W 13L 1D 4 unfinished; mobility 3W 13L 1D 3 unfinished. Both zero illegal moves and zero crashes.
- NO-GO for promotion/submission until gates pass.
