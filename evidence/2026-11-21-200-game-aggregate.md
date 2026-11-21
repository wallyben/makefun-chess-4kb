# 200-game Stockfish screening — 2026-11-21

Source: https://github.com/wallyben/makefun-chess-4kb/actions/runs/44922619709 (head 250046259037dc6c2cbc43a9c4e1991c82c3ee3f). Aggregated 20 job logs, 10 shards x 10 games per candidate, parsing each emitted game JSON and interpreting wins by our_color. Unfinished games are censored, NOT draws.

| Candidate (job matrix label) | W | D | L | Unfinished | Max observed move seconds | Illegal | Crashes |
|---|---:|---:|---:|---:|---:|---:|---:|
| experiment/phase-eval-20261121 | 20 | 8 | 45 | 27 | 0.763 | 0 | 0 |
| experiment/mate-terminal-20261121 | 22 | 7 | 46 | 25 | 0.481 | 0 | 0 |

Caution: The embedded script in the job logs hardcodes the output JSON `candidate` field as `experiment/mate-terminal-20261121` even in phase-eval matrix jobs. Candidate assignment here uses GitHub job matrix labels, not that incorrect embedded field. These are separate matches against Stockfish UCI_Elo 1320, not direct head-to-head, and are NOT make.fun practice Elo. Completion-conditioned score: phase 24/73 (32.9%), mate 25.5/75 (34.0%). The 1.1 percentage point difference is not compelling evidence of superior playing strength, especially with censored games. No promotion. Official acceptance, transcript eligibility and practice Elo remain UNKNOWN.

Protected champion: submission-minimal ca334ddbb43253ba84db40dbd09817be5779c39e; no changes. Highest priority remains official runner/provenance eligibility, then direct paired comparison.