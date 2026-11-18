"""Minimal legal-move-independent board evaluation scaffold; NOT a playing engine yet."""
VALUES={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0}
def material(fen):
    board=fen.split()[0]
    if len(board.split('/'))!=8: raise ValueError('invalid FEN ranks')
    score=0
    for rank in board.split('/'):
        count=0
        for ch in rank:
            if ch.isdigit():
                count+=int(ch)
            elif ch.lower() in VALUES:
                count+=1;score+=VALUES[ch.lower()]*(1 if ch.isupper() else -1)
            else: raise ValueError('invalid FEN piece')
        if count!=8: raise ValueError('invalid FEN width')
    return score
if __name__=='__main__':
    import sys
    print(material(sys.argv[1] if len(sys.argv)>1 else '8/8/8/8/8/8/8/8 w - - 0 1'))
