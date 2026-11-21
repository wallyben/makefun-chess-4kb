# TinyForge competition completion checklist

Deadline: 2026-11-24 17:00 UTC. Check boxes only with a reproducible evidence link or commit. Do not confuse a passing CI workflow with chess strength.

## 1. Establish baseline
- [x] Complete initial three-candidate Stockfish screening (run 44898748268; tactical limited to 8 games; not a statistically controlled strength ranking).
- [ ] Select strongest candidate from completed-game results; require sufficient evidence.
- [ ] Record W/D/L, unfinished, crashes, illegal moves, and per-move latency (latency instrumentation missing).

## 2. Competitive engine
- [ ] Verify castling, en passant, all promotions, checkmate and stalemate (both candidates passed targeted regression run 44899137617; underpromotions and terminal states remain untested).
- [x] Implement compact alpha-beta pruning (4096-byte prototype commit 3acea117; targeted regression passed run 44899137617; playing-strength acceptance separate).
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
- [x] Special-rule regression suite (targeted castling, en passant, queen promotions and king safety; run 44898748282).
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

## New evidence 2026-11-21
- Tactical extension: 8 games, 0W 3L 1D 4 unfinished, max observed move latency 0.289s, 0 crashes/illegal moves (run 44898748268). Reject promotion; 8-game sample is small.
- Alpha-beta prototype commit 3acea117, exactly 4096 bytes. Not yet validated or promoted.

- CI regression matrix extended to submission-minimal and experiment/alphabeta-20261121 (commit 8b78345d). No challenger correctness/strength pass claimed until rerun finishes.

- Alpha-beta and baseline both passed targeted rules matrix: run 44899137617. Benchmark run 44899137514 in progress at inspection.

## Maximum-strength finish plan (2026-11-21)

These tasks supplement the eligibility and submission gates above. A checked implementation is not a claim of competitive superiority.

### A. Correctness and runtime — mandatory
- [x] Targeted rules regression passes on both baseline and alpha-beta branches (run 44899137617).
- [x] Verify underpromotions and targeted checkmate/stalemate/en-passant reply states against python-chess (run 44899408505; not exhaustive full-state verification).
- [ ] Verify candidate's full game-state correctness, including castling rights and en-passant in deeper search (seeded midgame differential tests passed on both candidates in run 44899571298; castling rights not modeled by replies).
- [ ] Verify 10-second hard limit on every candidate move in complete games.
- [ ] Verify 4096-byte main.py, per-file limits and total snapshot limit on the exact final commit.

### B. Search strength — priority order
- [x] Build a bounded alpha-beta prototype (experiment/alphabeta-20261121, 4096 bytes; strength not established).
- [ ] Verify iterative deepening preserves a completed move on timeout.
- [ ] Add efficient move ordering (captures/promotions/checks or validated proxy).
- [ ] Add bounded quiescence or selective tactical extensions.
- [ ] Evaluate compact transposition caching or selective reductions ONLY if byte and runtime budgets permit.
- [ ] Compare depth, nodes, tactical accuracy and game results against baseline.

### C. Knowledge and endgames
- [x] Build reproducible offline Stockfish teacher evaluation pipeline (run 44898196403).
- [ ] Curate representative opening, tactical, quiet and endgame test positions with held-out validation.
- [ ] Tune evaluation weights on training set and validate on held-out positions.
- [ ] Accept learned weights only after a controlled game-strength improvement.
- [ ] Test basic endgame conversion and draw recognition.

### D. Tournament evidence
- [x] Complete initial three-candidate screening (run 44898748268).
- [ ] Finish alpha-beta Stockfish benchmark and reject invalid/time-violating candidates (focused 8-game paired-colour screening configured 4d39ae6; corrected 35-second whole-game timeout to 180 seconds in f99b297; CI pending).
- [ ] Run paired head-to-head against incumbent champion with fixed openings and alternating colors.
- [ ] Benchmark against Sunfish 4KB and record W/D/L plus confidence/uncertainty.
- [ ] Verify official practice rating >=1154 and record platform evidence.
- [ ] Promote only the strongest eligible proven candidate.

### E. Feature freeze and submission
- [ ] Freeze changes by 2026-11-23 17:00 UTC unless a critical validity defect remains.
- [ ] Run final clean-room Python 3.13 protocol and size verification.
- [ ] Collect authentic development transcripts and provenance.
- [ ] Submit official entry before 2026-11-24 17:00 UTC.
- [ ] Preserve acceptance receipt, submitted commit, test logs and final ranking.

### Stop rules
- Never trade a proven legal submission for an unverified experiment.
- Never infer Elo or strength from a small sample or teacher-evaluation MSE alone.
- Prioritize search quality and correctness over speculative features.
- At deadline, submit the strongest eligible verified version even if optimization targets remain unfinished.

- Authoritative legal-reply comparison passed on both candidates, run 44899408505. Broader castling-rights and repeated-position search tests remain open.

- Seeded randomized midgame legal-reply differential suite passed on both candidates, run 44899571298. This does not establish complete search-state correctness.

## 2026-11-21 official-rule eligibility correction and measured delta
- **PROVEN P0:** Official bounty requires fixed-depth or fixed-node deterministic search, *never a clock* (https://make.fun/bounty/tiny-chess-01). Alpha-beta `3acea117` uses `time.monotonic()` and is ineligible as written. Do not promote it.
- **PROVEN benchmark:** 8 games each against Stockfish UCI_Elo 1320, run 44899658105: submission-minimal `ca334ddb` 0W/6L/1D/1 unfinished, max move 0.061s; alpha-beta `3acea117` 3W/5L/0D/0 unfinished, max move 0.928s. Both 0 illegal/0 crashes. These are separate samples, not direct paired head-to-head; insufficient to establish a robust superiority claim.
- **New isolated challenger:** `experiment/fixed-node-20261121` commit `0d3c92d`, `main.py` 4092 bytes. Replaces clock cutoff with fixed 3000 search-node budget, retaining last-completed-depth fallback. Acceptance: Python 3.13 legality/protocol CI, <=10s/move, no crashes, and reproducible strength versus champion; stop/reject if any fail. No promotion yet.
- **Verification:** existing candidate-rules and Stockfish benchmark PR workflow matrices updated in commits `3720109`, `2496641` to include fixed-node challenger; runs 44902714890 and 44902714861 queued at inspection. Official kit acceptance, practice Elo, transcript and full snapshot size remain UNKNOWN.
- **Current champion:** `submission-minimal` `ca334ddbb43253ba84db40dbd09817be5779c39e`, 3790-byte main.py. **NO-GO** official submission pending owner approval and final gates.
