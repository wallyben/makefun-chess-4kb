import sys
V=dict(zip('pnbrqk',(100,320,330,500,900,0)))
START='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
def parse(f):
 a=f.split();rows=a[0].split('/');b=[]
 if len(rows)!=8:raise ValueError('FEN ranks')
 for row in rows:
  x=[]
  for c in row:x+=['.']*int(c) if c.isdigit() else [c]
  if len(x)!=8:raise ValueError('FEN width')
  b+=x
 if any(c!='.' and c.lower() not in V for c in b):raise ValueError('FEN piece')
 return b,a[1] if len(a)>1 else 'w',a[2] if len(a)>2 else '-',a[3] if len(a)>3 else '-'
def material(f):
 b,*_=parse(f)
 return sum(V[c.lower()]*(1 if c.isupper() else -1) for c in b if c!='.')
def sq(s):return (8-int(s[1]))*8+ord(s[0])-97
def nm(i):return chr(97+i%8)+str(8-i//8)
def apply(b,m,ep='-'):
 i,j,p=m;c=b[i];n=b[:];n[i]='.'
 if c.lower()=='p' and ep!='-' and j==sq(ep) and b[j]=='.':n[j+(8 if c.isupper() else -8)]='.'
 n[j]=(p.upper() if c.isupper() else p) if p else c
 if c.lower()=='k' and abs(j-i)==2:
  r=i+3 if j>i else i-4;t=i+1 if j>i else i-1;n[t]=n[r];n[r]='.'
 return n
def king(b,w):
 try:return b.index('K' if w else 'k')
 except ValueError:return -1
def moves(b,w,castle='-',ep='-',legal=True):
 out=[]
 def add(i,j,p=''):
  if b[j]=='.' or b[j].lower()!='k' and b[j].isupper()!=w:out.append((i,j,p))
 for i,c in enumerate(b):
  if c=='.' or c.isupper()!=w:continue
  x,y=i%8,i//8;t=c.lower()
  if t=='p':
   ny=y+(-1 if w else 1)
   if 0<=ny<8:
    j=ny*8+x
    if b[j]=='.':
     for p in ('q','r','b','n') if ny in (0,7) else ('',):add(i,j,p)
     if y==(6 if w else 1) and b[j+(-8 if w else 8)]=='.':add(i,j+(-8 if w else 8))
    for dx in (-1,1):
     if 0<=x+dx<8:
      j=ny*8+x+dx
      if (b[j]!='.' and b[j].lower()!='k' and b[j].isupper()!=w) or (ep!='-' and j==sq(ep) and b[j]=='.' and b[j+(8 if w else -8)]==('p' if w else 'P')):
       for p in ('q','r','b','n') if ny in (0,7) else ('',):add(i,j,p)
  elif t=='n':
   for dx,dy in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
    if 0<=x+dx<8 and 0<=y+dy<8:add(i,(y+dy)*8+x+dx)
  else:
   ds=((1,1),(1,-1),(-1,1),(-1,-1)) if t=='b' else ((1,0),(-1,0),(0,1),(0,-1)) if t=='r' else ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1))
   for dx,dy in ds:
    nx,ny=x+dx,y+dy
    while 0<=nx<8 and 0<=ny<8:
     j=ny*8+nx;add(i,j)
     if b[j]!='.' or t=='k':break
     nx+=dx;ny+=dy
   if t=='k' and legal and not attacked(b,i,not w):
    rank=7 if w else 0;rights='KQ' if w else 'kq'
    if i==rank*8+4:
     for right,rook,dest,clear,transit in ((rights[0],7,6,(5,6),5),(rights[1],0,2,(1,2,3),3)):
      if right in castle and b[rank*8+rook]==('R' if w else 'r') and all(b[rank*8+z]=='.' for z in clear) and not attacked(b,rank*8+transit,not w):out.append((i,rank*8+dest,''))
 if not legal:return out
 legal_moves=[]
 for m in out:
  n=apply(b,m,ep)
  if not attacked(n,king(n,w),not w):legal_moves.append(m)
 return legal_moves
def attacked(b,j,w):
 if j<0:return True
 x,y=j%8,j//8
 for dx in (-1,1):
  nx=x+dx;ny=y+(1 if w else -1)
  if 0<=nx<8 and 0<=ny<8 and b[ny*8+nx]==('P' if w else 'p'):return True
 t=b[:];t[j]='.'
 return any(k==j and t[i].lower()!='p' for i,k,_ in moves(t,w,legal=False))
def search(b,w,c,e,d,alpha=-999999,beta=999999,q=0):
 # Quiescence: resolve forcing captures and promotions at the horizon.
 # In check, search every evasion; stand-pat is not legal.
 check=attacked(b,king(b,w),not w)
 ms=moves(b,w,c,e)
 if d<=0 and not check:
  stand=sum((V[p.lower()]+(10 if p.lower()=='p' and 2<i//8<6 else 0))*(1 if p.isupper()==w else -1) for i,p in enumerate(b) if p!='.')
  # Terminal stalemate must score zero even at a quiescence cutoff.
  if not ms:return 0,None
  if q>=4 or stand>=beta:return stand,None
  alpha=max(alpha,stand)
 if not ms:return (-100000-d if check else 0),None
 if d<=0:
  if not check:ms=[m for m in ms if b[m[1]]!='.' or m[2] or (b[m[0]].lower()=='p' and e!='-' and m[1]==sq(e))]
  elif q>=6:
   # Bounded check extension: evaluate legal evasions instead of inventing mate.
   return max(sum(V[p.lower()]*(1 if p.isupper()==w else -1) for p in apply(b,m,e) if p!='.') for m in ms),None
 ms.sort(key=lambda m:10*V.get(b[m[1]].lower(),0)-V[b[m[0]].lower()]+8000*bool(m[2])+(1000 if b[m[0]].lower()=='p' and e!='-' and m[1]==sq(e) else 0),reverse=True)
 best=None
 for m in ms:
  i,j,_=m;piece=b[i];nc=c;ne='-'
  if piece.lower()=='k':nc=nc.replace('K' if w else 'k','').replace('Q' if w else 'q','')
  for square,right in ((63,'K'),(56,'Q'),(7,'k'),(0,'q')):
   if i==square or j==square:nc=nc.replace(right,'')
  if piece.lower()=='p' and abs(i-j)==16:ne=nm((i+j)//2)
  v=-search(apply(b,m,e),not w,nc,ne,d-1,-beta,-alpha,q+1 if d<=0 else 0)[0]
  if v>alpha:alpha=v;best=m
  if alpha>=beta:break
 return alpha,best
def main():
 fen=START
 for line in sys.stdin:
  a=line.split()
  if not a:continue
  if a[0]=='uci':print('id name TinyForge\nid author wallyben\nuciok',flush=True)
  elif a[0]=='isready':print('readyok',flush=True)
  elif a[0]=='ucinewgame':fen=START
  elif a[0]=='position':
   if a[1]=='startpos':fen=START;idx=2
   elif a[1]=='fen':end=a.index('moves') if 'moves' in a else len(a);fen=' '.join(a[2:end]);idx=end
   else:continue
   b,w,c,e=parse(fen);w=w=='w'
   if idx<len(a) and a[idx]=='moves':
    for text in a[idx+1:]:
     m=next((m for m in moves(b,w,c,e) if nm(m[0])+nm(m[1])+m[2]==text),None)
     if m is None:break
     i,j,_=m;piece=b[i];old=e
     e=nm((i+j)//2) if piece.lower()=='p' and abs(i-j)==16 else '-'
     if piece.lower()=='k':c=c.replace('K' if w else 'k','').replace('Q' if w else 'q','')
     for square,right in ((63,'K'),(56,'Q'),(7,'k'),(0,'q')):
      if i==square or j==square:c=c.replace(right,'')
     b=apply(b,m,old);w=not w
   fen='/'.join(''.join(b[z:z+8]) for z in range(0,64,8))+' '+('w' if w else 'b')+' '+(c or '-')+' '+e+' 0 1'
  elif a[0]=='go':
   b,w,c,e=parse(fen);d=3
   if 'depth' in a:
    try:d=min(5,max(1,int(a[a.index('depth')+1])))
    except (ValueError,IndexError):pass
   _,m=search(b,w=='w',c,e,d)
   print('bestmove '+(nm(m[0])+nm(m[1])+m[2] if m else '0000'),flush=True)
  elif a[0]=='quit':break
if __name__=='__main__':main()
