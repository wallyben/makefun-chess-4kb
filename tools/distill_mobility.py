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
SAMPLES = 120
DEPTH = 9
COEFFICIENTS = (-8, -4, -2, 0, 1, 2, 4, 8, 12, 16)
PIECE_VALUES = {chess.PAWN:100, chess.KNIGHT:320, chess.BISHOP:330,
                chess.ROOK:500, chess.QUEEN:900, chess.KING:0}


def material(board):
    return sum((1 if piece.color else -1) * PIECE_VALUES[piece.piece_type]
               for piece in board.piece_map().values())


def mobility(board):
    white = board.copy(stack=False)
    black = board.copy(stack=False)
    white.turn = chess.WHITE
    black.turn = chess.BLACK
    return len(white.attacks(chess.E4)) - len(black.attacks(chess.E4))


def controlled_squares(board):
    return sum(any(board.is_attacked_by(chess.WHITE, s) for s in [i]) -
               any(board.is_attacked_by(chess.BLACK, s) for s in [i])
               for i in chess.SQUARES)


def positions():
    rng = random.Random(SEED)
    out = []
    while len(out) < SAMPLES:
        b = chess.Board()
        for _ in range(rng.randrange(8, 54)):
            if b.is_game_over(): break
            b.push(rng.choice(list(b.legal_moves)))
        if not b.is_game_over() and abs(material(b)) < 1400:
            out.append(b)
    return out


def mse(rows, weight):
    return statistics.mean((teacher - mat - weight * mobility_score) ** 2
                           for teacher, mat, mobility_score in rows)


def main():
    binary = shutil.which('stockfish') or '/usr/games/stockfish'
    rows = []
    with chess.engine.SimpleEngine.popen_uci(binary) as teacher:
        teacher.configure({'Threads': 1, 'Hash': 16})
        for b in positions():
            info = teacher.analyse(b, chess.engine.Limit(depth=DEPTH))
            score = info['score'].white().score(mate_score=10000)
            rows.append((score, material(b), controlled_squares(b)))
    # Hold out every fourth position, never tune on evaluation samples.
    train = [row for i, row in enumerate(rows) if i % 4 != 0]
    holdout = [row for i, row in enumerate(rows) if i % 4 == 0]
    ranked = sorted(COEFFICIENTS, key=lambda w: mse(train, w))
    report = {
        'status': 'offline_teacher_fit_only',
        'teacher': f'Stockfish depth {DEPTH}',
        'seed': SEED, 'samples': len(rows),
        'train': len(train), 'holdout': len(holdout),
        'baseline_coefficient': 0,
        'candidate_coefficients': list(COEFFICIENTS),
        'best_train_coefficient': ranked[0],
        'holdout_mse_baseline': round(mse(holdout, 0), 2),
        'holdout_mse_best': round(mse(holdout, ranked[0]), 2),
        'holdout_mse_current_2': round(mse(holdout, 2), 2),
        'note': 'Teacher fit does not establish playing strength. Do not promote without paired games.'
    }
    print(json.dumps(report, indent=2))
    with open('distillation-results.json', 'w') as f:
        json.dump(report, f, indent=2)


if __name__ == '__main__':
    main()
