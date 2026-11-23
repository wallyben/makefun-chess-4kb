# Verified official gauntlet — 2026-11-22

Source: GitHub Actions run https://github.com/wallyben/makefun-chess-4kb/actions/runs/45076549510, artifact ID 14775767749 (official-practice-g1-evidence), workflow head 70c0277d4b02eab1c7e7bc42a76fe690b3789f63. Extracted official-gauntlet.json SHA-256 fcd2dceb7174d6a0397a5274e6c96f0c2db49d7dea8d1b43c3b2b32f113278dc. This is a fixed local official-kit practice gauntlet, not evidence that hosted final openings will match.

| Game | Color | Opponent | Opening | Eight opening plies |
|---|---|---|---|---|
| 1 | white | depth-2 | Semi-Slav | d2d4 d7d5 c2c4 c7c6 b1c3 g8f6 e2e3 e7e6 |
| 2 | black | depth-3 | Sicilian | e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 |
| 3 | white | depth-4 | Italian | e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 |
| 4 | black | nodes-100k | Berlin | e2e4 e7e5 g1f3 b8c6 f1b5 g8f6 e1g1 f6e4 |
| 5 | white | nodes-250k | Slav | d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4 |
| 6 | black | nodes-500k | Philidor | e2e4 e7e5 g1f3 d7d6 d2d4 g8f6 b1c3 b8d7 |

Scorer from same artifact: 1279 Elo, 2W/2D/2L for *previous passed-pawn derivative*, not a new candidate. Per-game results: game 1 draw stalemate (89 plies); game 2 win checkmate (112); game 3 draw insufficient material (134); game 4 loss checkmate (137); game 5 win checkmate (99); game 6 loss checkmate (105).

## Engineering implications and restrictions

The first eight plies are already applied by the harness: do **not** waste bytes storing these as moves to replay. A prepared continuation must match a verified board/side-to-move or history and legal move, must exit cleanly on deviation, and must retain a general fallback. The transcript contains one deterministic line per scenario for the *previous derivative*, not a proof that a new candidate will induce identical opponent responses. The observed stalemate and insufficient-material draws identify outcomes but do not establish that any untested book improves them. No >=2000 score is verified, and no new candidate has been tested. Preserve rollback ca334ddbb43253ba84db40dbd09817be5779c39e.
