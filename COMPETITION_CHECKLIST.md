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
- [x] Finish latest alpha-beta/benchmark screening and identify eligibility failures (run 44902734559; alpha-beta clock-based cutoff is ineligible under official deterministic-search rule; fixed-node challenger remains experimental).
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

## 2026-11-21 latest benchmark and eligibility gate (run 44902734559)
- Latest Stockfish 1320 configured screening, eight games per candidate: incumbent 0W/8L/0 unfinished, alpha-beta 0W/3L/5 unfinished, fixed-node 0W/6L/2 unfinished. No crashes, illegal moves or per-move overruns. Unfinished are censored, **not draws**.
- Maximum observed move latency: incumbent 0.047s; alpha-beta 1.331s; fixed-node 0.154s. These are observations, not proven worst-case bounds.
- IMPORTANT: Official rules require fixed-depth/fixed-node deterministic search. The clock-based alpha-beta prototype is **ineligible**, irrespective of apparent game strength. Only deterministic candidates can be promoted.
- Eight-game samples are insufficient to establish strength ranking; no challenger promoted. Next: paired direct matches, tactical suite, and official-kit acceptance for fixed-node candidate.

## 2026-11-21 deterministic deeper-search challenger
- Created isolated `experiment/fixed-node-deeper-20261121` commit `98164037` from fixed-node baseline: fixed node budget 3000 -> 12000, iterative depth attempts (1,2) -> (1,2,3). `main.py` remains 4092 ASCII bytes. No clock-based search.
- Added candidate to Stockfish and rules matrices (commits 5079e78, 4069979). Pending: full Python 3.13 legality CI, no illegal moves/crashes, per-move latency below 10s, strength versus incumbent and fixed-node baseline.
- WARNING: additional depth and node budget are a hypothesis, NOT measured Elo gain; do not promote without evidence.

## 2026-11-21 ordered-search implementation gate
- [x] Implement experimental legal-move ordering and checkmate/stalemate terminal evaluation in isolated `experiment/ordered-search-20261121`, commit `4af82a3` (exactly 4096 bytes, deterministic 12000-node cap).
- [x] Register challenger in legality and Stockfish CI matrices (commits `01dca22`, `24bd304`).
- [ ] Verify candidate passes CI rules and 10s/move game runtime.
- [ ] Prove actual strength gain versus `experiment/fixed-node-deeper-20261121` and incumbent; reject otherwise.
- [ ] Implement bounded quiescence search under size/runtime constraints.
- [ ] Implement safe compact transposition table, if justified by measured benefit.
- [ ] Implement safe late-move reductions, if justified by measured benefit.
- [ ] Restore or improve tactical/positional evaluation without sacrificing stronger search.
- Note: To fit the 4096-byte cap the prototype removes attacked-piece penalty and simplifies center scoring; these are possible regressions. Move ordering by full position evaluation may cost substantial CPU; no Elo claim before tests.

## 2026-11-21 search-cost ablation
- [x] Create isolated cheap root-capture-order variant `experiment/capture-order-20261121` commit `8429689` (4051 bytes), removing full-board evaluation sorting at every internal search node while retaining capture-value root ordering.
- [x] Register cheap-order candidate in legality and Stockfish matrices (commits `3ea14a3`, `9540df0`).
- [ ] Establish cheap-order legality, runtime, and strength versus expensive-sort candidate from completed CI.
- [ ] Quiescence, transposition table and late-move reductions remain unimplemented; no claim of significant Elo increase.

## 2026-11-21 capture-order first completed run
- [x] Capture-order candidate passed candidate-rules regression in GitHub Actions run 44906293767.
- [x] Capture-order Stockfish eight-game job completed successfully in run 44906293671: 1 win, 2 draws, 4 losses, 1 unfinished/censored; maximum observed move 0.320 seconds; zero illegal moves or crashes.
- [ ] Establish a statistically reliable Elo gain. This eight-game result is insufficient, and previous 12000-node deeper candidate achieved 2 wins / 6 losses in a different run.
- [ ] Wait for expensive internal-ordering candidate results; compare paired games and avoid promoting on noise.

## Search-budget calibration and strategic-depth upgrade (2026-11-21)
- [x] Define deterministic search-budget calibration plan; respect competition fixed-node/fixed-depth rule, never use wall-clock cutoff.
- [ ] Benchmark node limits 25000, 50000, 100000 and 200000 across opening, middlegame, tactics and endgame, including worst-case move time and HTTP overhead.
- [ ] Choose a safe fixed-node cap from worst-case measurements, targeting <=8.5 seconds search and <=10 seconds total per move (not a clock-based stopping condition).
- [ ] Implement iterative deepening that retains the last fully completed depth result and deterministic move ordering.
- [ ] Implement and verify quiescence search and mate-aware terminal scoring with correct checkmate/stalemate detection.
- [ ] Evaluate transposition table and late-move reductions under the 4096-byte limit; only mark complete if actually implemented and validated.
- [ ] Run paired head-to-head games and Stockfish tests with consistent openings, color swaps, crash/illegal/timeout gates; measure Elo with uncertainty.
- [ ] Promote only a legal, runtime-safe challenger with reproducible strength improvement; preserve incumbent until then.

### First search-budget calibration implementation
- [x] Create isolated deterministic 25000-node candidate `experiment/nodes-25000-20261121` at `048a6c6`, 4092 bytes, otherwise identical to 12000-node baseline.
- [x] Register 25000-node candidate in rules and Stockfish CI matrices (`d109074`, `bf8f66e`).
- [ ] Measure its game runtime and strength; 50000/100000/200000 remain untested.

### 2026-11-21 fixed-node budget decision (run 44906594246)
- [x] Paired benchmark screen at the same Stockfish setting and eight-game schedule: 12000 nodes 5W/0D/1L/2 censored, max observed 0.660s; 25000 nodes 3W/0D/3L/2 censored, max observed 1.497s. Both zero reported illegal moves and crashes. These are censored screening games, NOT a validated Elo estimate or complete head-to-head match.
- [x] REJECT promotion of 25000-node challenger for now: no demonstrated strength advantage over 12000-node baseline, despite longer runtime. Preserve both branch histories and submission-minimal champion.
- [ ] Run direct same-opening, color-swapped 12000-vs-25000 matches before making a statistically confident strength ranking; official kit/practice Elo still UNKNOWN.

## 2026-11-21 isolated checkmate-terminal experiment
- [x] Implement internal checkmate-vs-stalemate scoring in isolated `experiment/mate-terminal-20261121`, commit `27f363b`, 4043 bytes, deterministic 12000-node cap.
- [x] Add candidate to legality and Stockfish CI matrices (`a7b11fe`, `bdd5d32`).
- [ ] Confirm rules, runtime, and tournament strength against original 12000-node engine; do not promote until evidence.
- [ ] Restore hanging-piece evaluation or replace with a stronger byte-efficient tactical evaluator; prototype removed it to fit mate scoring.
- [ ] Larger paired games and statistically justified Elo gain remain pending.

## 2026-11-21 checkmate-aware benchmark results
- [x] GitHub Actions rules regression succeeded: run 44909682967.
- [x] Stockfish benchmark succeeded: run 44909683001. Checkmate-aware 12000-node candidate 5W/1D/1L/1 unfinished (censored), maximum observed move 0.229s, 0 illegal moves, 0 crashes.
- [x] Same run original 12000-node candidate 0W/0D/4L/4 unfinished; 25000-node candidate 1W/0D/6L/1 unfinished; ordered-search candidate 3W/2D/3L/0 unfinished.
- [ ] Confirm mate-aware improvement with larger, paired head-to-head tests and position-level tactical checks; eight-game benchmark is not enough to prove Elo improvement.
- [ ] Reassess hanging-piece penalty removal and test worst-case latency; do not automatically promote to submission branch.
