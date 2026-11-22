# COMPETITION EXECUTION LOCK — Tiny Chess 4KB

Status: ACTIVE. Deadline: 2026-11-24 17:00 UTC. Submission target: 2026-11-24 12:00 UTC. Feature freeze: 2026-11-23 17:00 UTC.

## Single objective
Deliver the strongest **officially scored, eligible, accepted** Tiny Chess entry. Passing CI, winning small Stockfish samples, and implementing new features are NOT success criteria.

## Strict sequential gates (never skip)
G0. Reproduce the official make.fun kit/scorer and confirm exact protocol, constraints, submission process.
G1. Obtain official practice score for a current eligible candidate; capture run, commit SHA, W/D/L, Elo and errors.
G2. Verify official qualification >=1154 Elo; if below, diagnose from official game evidence, not guesses.
G3. If time allows, evaluate MIT-licensed Xyzar29 candidate under identical official conditions; preserve provenance/license.
G4. Choose one champion plus protected fallback, based on official evidence and legality, determinism, runtime.
G5. At most ONE targeted optimization based on measured weakness, accepted only with reproducible official improvement; revert otherwise.
G6. Prepare minimal exact release snapshot: main.py <=4096 bytes; total <=8192 bytes; per-file limits; Python 3.13; deterministic fixed-node search; API; 10s; authentic transcripts; license; legal moves.
G7. Submit before target time and verify accepted receipt, exact SHA, official score; fix only blocking failures.

## Hard guardrails
- Exactly ONE active candidate experiment. No concurrent benchmark matrix or duplicate Actions workflows.
- Do not repeat Stockfish 1320 screens. No architecture rewrites, agent frameworks, or speculative feature development.
- Never confuse a GitHub Actions success with official qualification.
- Never overwrite submission-minimal until a validated promotion is ready; record rollback SHA.
- If a gate is blocked, work ONLY on resolving that gate or explicitly request the missing user authorization/action.
- Stop optional feature development at freeze time. After 2026-11-24 12:00 UTC focus on accepted submission; after 17:00 UTC stop.
- No unverified claims. Use PROVEN / SUPPORTED / UNKNOWN labels.
- This document and the automation prompt govern every run. Any departure needs an explicit user decision.

## Evidence ledger — current
PROVEN: PV-first smoke/regression passed; local Stockfish 1320 screening performed; Xyzar29 public engine compiled and ran six simulated games with no crashes/illegal moves, 3W 2L 1 unfinished (GitHub Actions run 44971972717).
PROVEN (2026-11-22): Official bundled scorer executed successfully for PV-first candidate on commit e85a1653102f8f0eb26674bd527077defe139a1b; Actions run 45001637940, job 137144255431: scores.json = {wins:0, draws:0, losses:6, elo:0, working:1, spare_plies:0}. Entry main.py 4092 bytes (SHA256 039fbfd3bce848bc9b36d3026c29c2841250da45ba0e0636a0d3a61dda86af5b). G1 verified; G2 fails 1154 threshold by 1154 Elo. No promotion or submission.\nUNKNOWN: Official practice Elo of other candidates, exact final release eligibility, accepted entry.
PROVEN (2026-11-22 12:14 UTC): Single check-evasion challenger experiment/check-evasion-depth-20261121 tested with official bundled kit/scorer via workflow commit 17a7ec97013da80f216ace0fb70317614c89cbc2, Actions run 45020997332, job 137203649370. Entry SHA256 2dce6ae738be549f9516c6ac03511fae48a41e35cccc21cb75af7f2c583b3036, 4096 bytes. scores.json = {wins:0,draws:0,losses:6,elo:0,working:1,spare_plies:0}; six checkmate losses. No improvement versus PV-first; G2 remains unverified, no promotion. Evidence artifact 14753517426.\nProtected incumbent: submission-minimal at ca334ddbb43253ba84db40dbd09817be5779c39e.
Public engine reproduction branch: experiment/public-engine-reproduction-20261122.

## Mandatory run report
CURRENT GATE:
EVIDENCE (with exact run/SHA):
ACTION TAKEN:
NEXT BLOCKER:
TIME TO DEADLINE:
