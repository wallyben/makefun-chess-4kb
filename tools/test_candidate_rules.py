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
    for promotion in "rbn":
        check("4k3/P7/8/8/8/8/8/4K3 w - - 0 1", "a7a8"+promotion)
        check("4k3/8/8/8/8/8/p7/4K3 b - - 0 1", "a2a1"+promotion)
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
    # Validate all generated replies against the authoritative legal board states.
    # Exclude positions with castling rights: candidate.replies does not model castling.
    for fen in [
        chess.STARTING_FEN,
        "4k3/8/8/8/8/8/4r3/4K3 w - - 0 1",
        "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1",
        "7k/6Q1/6K1/8/8/8/8/8 b - - 0 1",
        "4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1",
    ]:
        b=chess.Board(fen)
        ep=candidate.sq(chess.square_name(b.ep_square)) if b.ep_square is not None else -1
        actual={"".join(x) for x in candidate.replies(candidate.board(fen),b.turn,ep)}
        expected=set()
        for m in b.legal_moves:
            n=b.copy();n.push(m)
            expected.add("".join(candidate.board(n.fen())))
        assert actual==expected,(fen,len(actual),len(expected),len(actual^expected))
    # Reproducible diverse midgame states; exclude features not represented by
    # replies(): castling and underpromotions, which require separate handling.
    import random
    rng=random.Random(20261121)
    for game in range(8):
        b=chess.Board()
        for ply in range(30):
            if b.is_game_over():break
            choices=sorted(b.legal_moves,key=lambda m:m.uci())
            b.push(rng.choice(choices))
            if b.castling_rights or b.is_game_over():continue
            if any(m.promotion in (chess.ROOK,chess.BISHOP,chess.KNIGHT) for m in b.legal_moves):continue
            ep=candidate.sq(chess.square_name(b.ep_square)) if b.ep_square is not None else -1
            actual={"".join(x) for x in candidate.replies(candidate.board(b.fen()),b.turn,ep)}
            expected=set()
            for m in b.legal_moves:
                n=b.copy();n.push(m)
                expected.add("".join(candidate.board(n.fen())))
            assert actual==expected,(game,ply,b.fen(),len(actual),len(expected),len(actual^expected))
    # Regression for a pinned en-passant capture: it must not expose the king.
    pinned_ep="4r1k1/8/8/3pP3/8/8/8/4K3 w - d6 0 1"
    pinned=chess.Board(pinned_ep)
    assert chess.Move.from_uci("e5d6") not in pinned.legal_moves
    ep=candidate.sq("d6")
    generated={"".join(x) for x in candidate.replies(candidate.board(pinned_ep),True,ep)}
    expected=set()
    for m in pinned.legal_moves:
        nxt=pinned.copy();nxt.push(m)
        expected.add("".join(candidate.board(nxt.fen())))
    assert generated==expected,("pinned en-passant",generated^expected)
    # A candidate must never claim a checkmated position has legal evasions.
    for fen in [
        "7k/6Q1/6K1/8/8/8/8/8 b - - 0 1",
        "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1",
    ]:
        position=chess.Board(fen)
        assert position.is_checkmate() or position.is_stalemate()
        assert not list(candidate.replies(candidate.board(fen),position.turn)),fen
    print("Candidate board-state, legal-reply, terminal-state and king-safety regression checks passed")


if __name__ == "__main__":
    main()
