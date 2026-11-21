"""Offline Stockfish-guided mobility distillation; never imported by main.py.

This is a bounded, deterministic teacher/student experiment, not a chess Elo claim.
Teacher scores are centipawns from White's perspective; tune only mobility coefficient.
"""
import json
import random
import shutil
import statistics
import chess
import chess.engine

SEED = 20261121
SAMPLES = 160
DEPTH = 9
COEFFICIENTS = (-8, -4, -2, 0, 1, 2, 4, 8, 12, 16)
PIECE_VALUES = {chess.PAWN:100, chess.KNIGHT:320, chess.BISHOP:330,
                chess.ROOK:500, chess.QUEEN:900, chess.KING:0}


def material(board):
    return sum((1 if piece.color else -1) * PIECE_VALUES[piece.piece_type]
               for piece in board.piece_map().values())


def controlled_squares(board):
    return sum(int(board.is_attacked_by(chess.WHITE, s)) -
               int(board.is_attacked_by(chess.BLACK, s)) for s in chess.SQUARES)


OPENINGS = (
    ('e2e4','e7e5','g1f3','b8c6'),
    ('d2d4','d7d5','c2c4','e7e6'),
    ('e2e4','c7c5','g1f3','d7d6'),
    ('d2d4','g8f6','c2c4','g7g6'),
    ('e2e4','e7e6','d2d4','d7d5'),
    ('c2c4','e7e5','b1c3','g8f6'),
    ('g1f3','d7d5','d2d4','g8f6'),
    ('e2e4','c7c6','d2d4','d7d5'),
)


def positions():
    """Opening-family split prevents train/validation continuation leakage."""
    rng = random.Random(SEED)
    out = []
    for family, opening in enumerate(OPENINGS):
        for _ in range(SAMPLES // len(OPENINGS)):
            b = chess.Board()
            for u in opening:
                b.push_uci(u)
            for _ in range(rng.randrange(2, 19)):
                if b.is_game_over(): break
                b.push(rng.choice(list(b.legal_moves)))
            if not b.is_game_over() and abs(material(b)) < 1400:
                out.append((family, b))
    return out


def mse(rows, weight):
    return statistics.mean((teacher - mat - weight * mobility_score) ** 2
                           for teacher, mat, mobility_score in rows)


def main():
    binary = shutil.which('stockfish') or '/usr/games/stockfish'
    rows = []
    with chess.engine.SimpleEngine.popen_uci(binary) as teacher:
        teacher.configure({'Threads': 1, 'Hash': 16})
        for family, b in positions():
            info = teacher.analyse(b, chess.engine.Limit(depth=DEPTH))
            score = info['score'].white().score(mate_score=10000)
            if abs(score) > 2000: continue
            rows.append((family, score, material(b), controlled_squares(b)))
    # Hold out every fourth position, never tune on evaluation samples.
    train = [row[1:] for row in rows if row[0] < 6]
    holdout = [row[1:] for row in rows if row[0] >= 6]
    assert len(train) >= 50 and len(holdout) >= 15, 'Insufficient eligible samples'
    ranked = sorted(COEFFICIENTS, key=lambda w: mse(train, w))
    report = {
        'status': 'offline_teacher_fit_only',
        'teacher': f'Stockfish depth {DEPTH}',
        'seed': SEED, 'samples': len(rows),
        'train': len(train), 'holdout': len(holdout),
        'split': 'six opening families train, two held out',
        'baseline_coefficient': 0,
        'candidate_coefficients': list(COEFFICIENTS),
        'best_train_coefficient': ranked[0],
        'holdout_mse_baseline': round(mse(holdout, 0), 2),
        'holdout_mse_best': round(mse(holdout, ranked[0]), 2),
        'holdout_mse_current_2': round(mse(holdout, 2), 2),
        'holdout_improved': mse(holdout, ranked[0]) < mse(holdout, 0),
        'note': 'Teacher fit does not establish playing strength. Do not promote without paired games.'
    }
    print(json.dumps(report, indent=2))
    with open('distillation-results.json', 'w') as f:
        json.dump(report, f, indent=2)


if __name__ == '__main__':
    main()
