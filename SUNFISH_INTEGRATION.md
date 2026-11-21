# Sunfish reference-engine integration — verified constraints

Official make.fun bounty: https://make.fun/bounty/tiny-chess-01
Upstream: https://github.com/thomasahle/sunfish/tree/e396948acbd80cdcbad3dccfb07e878fba9df8f4
House source: nnue_4k/pst_entry.py (42,975 source bytes), NOT a directly compliant main.py.

Critical discovery: upstream nnue_4k/README.md explicitly says its engine plus shipped net is NOT 4KB compliant: smallest shipped net is 7.5 MB. The official house claims to adapt and pack a specific Sunfish derivative to 3,649 bytes, but its exact adapted artifact must be obtained from the official kit and independently verified. Do not embed external model weights or assume upstream NNUE directly fits.

Competition constraints: Python 3.13 stdlib only; main.py <=4096 bytes; snapshot <=8192 bytes; fixed-depth/fixed-node deterministic search; 10 seconds per move; main.py must be standalone; no model calls; no external data. Sunfish GPL-3.0-only derivatives require the official makefun bundle submission route with SPDX-only LICENSE and authentic transcripts.

Execution gates:
- [x] Isolate experimental branch without touching submission-minimal.
- [x] Identify pinned upstream source, provenance, and licensing.
- [x] Identify upstream net size mismatch and correct prior assumption.
- [ ] Fetch official kit's agent/sunfish-4k/main.py and independently verify source, hash, size and Python protocol.
- [ ] Reproduce the 3,649-byte house artifact or create a licence-compliant Sunfish-derived entry under 4,096 bytes.
- [ ] Verify legal moves and deterministic node budget, 10s move latency, game-history correctness, mate/stalemate/repetition and 6-game official practice.
- [ ] Compare against current mate-terminal entry and house Sunfish in paired tournaments, including confidence intervals.
- [ ] Package GPL SPDX license, complete source bundle, actual agent transcripts and run record before submission.

Do not promote this branch until a real compliant executable passes all gates.
