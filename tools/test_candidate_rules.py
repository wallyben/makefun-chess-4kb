"""Deterministic regression checks for exact competition candidate's move model."""
import importlib.util
import os
import pathlib
import chess

os.environ.setdefault("MAKEFUN_ENV_URL", "http://127.0.0.1:1")
spec = importlib.util.spec_from_file_location("candidate", "/tmp/tiny_chess_candidate.py")
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


def check(fen, uci):
    b = chess.Board(fen)
    move = chess.Move.from_uci(uci)
    assert move in b.legal_moves, (fen, uci, "invalid test")
    expected = b.copy()
    expected.push(move)
    actual = candidate.move(candidate.board(fen), uci)
    got = "".join(actual)
    want = "".join(candidate.board(expected.fen()))
    assert got == want, (fen, uci, got, want)


def main():
    check(chess.STARTING_FEN, "e2e4")
    check("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", "e1g1")
    check("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", "e1c1")
    check("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1", "e8g8")
    check("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1", "e8c8")
    check("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1", "e5d6")
    check("4k3/8/8/8/3Pp3/8/8/4K3 b - d3 0 1", "e4d3")
    check("4k3/P7/8/8/8/8/8/4K3 w - - 0 1", "a7a8q")
    check("4k3/8/8/8/8/8/p7/4K3 b - - 0 1", "a2a1q")
    # The move generator must never yield positions exposing its own king.
    for fen in [
        "4k3/8/8/8/8/8/4r3/4K3 w - - 0 1",
        "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
        "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1",
    ]:
        b = chess.Board(fen)
        for next_board in candidate.replies(candidate.board(fen), b.turn):
            king = next_board.index("K" if b.turn else "k")
            assert king not in candidate.attacks(next_board, not b.turn)
    print("Candidate board-state and king-safety regression checks passed")


if __name__ == "__main__":
    main()
