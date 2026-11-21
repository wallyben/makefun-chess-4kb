import os,json,urllib.request
U=os.environ['MAKEFUN_ENV_URL'].rstrip('/')
V=dict(zip('pnbrqk',(100,320,330,500,900,0)))
def post(p,d):
 r=urllib.request.Request(U+p,json.dumps(d).encode(),{'Content-Type':'application/json'})
 with urllib.request.urlopen(r,timeout=9) as f:return json.load(f)
def board(f):
 b=[]
 for row in f.split()[0].split('/'):
  for c in row:b+=['.']*int(c) if c.isdigit() else [c]
 return b
def sq(s):return (8-int(s[1]))*8+ord(s[0])-97
def move(b,m):
 i,j=sq(m[:2]),sq(m[2:4]);p=b[i];n=b[:];n[i]='.'
 if p.lower()=='p' and i%8!=j%8 and b[j]=='.':n[j+(8 if p.isupper() else -8)]='.'
 n[j]=m[4].upper() if len(m)>4 and p.isupper() else m[4] if len(m)>4 else p
 if p.lower()=='k' and abs(i-j)==2:
  r=i+3 if j>i else i-4;t=i+1 if j>i else i-1;n[t]=n[r];n[r]='.'
 return n
def attacks(b,w):
 a=set()
 for i,p in enumerate(b):
  if p=='.' or p.isupper()!=w:continue
  x,y=i%8,i//8;t=p.lower()
  if t=='p':ds=[(-1,-1),(1,-1)] if w else [(-1,1),(1,1)]
  elif t=='n':ds=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
  else:ds=([(1,1),(-1,1),(1,-1),(-1,-1)] if t=='b' else [(1,0),(-1,0),(0,1),(0,-1)] if t=='r' else [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)])
  for dx,dy in ds:
   xx,yy=x+dx,y+dy
   while 0<=xx<8 and 0<=yy<8:
    j=yy*8+xx;a.add(j)
    if t in 'pnk' or b[j]!='.':break
    xx+=dx;yy+=dy
 return a
def score(b,w):
 own=attacks(b,w);opp=attacks(b,not w);v=0
 for i,p in enumerate(b):
  if p=='.':continue
  friendly=p.isupper()==w;t=p.lower();x=i%8;y=i//8
  center=6-abs(2*x-7)//2-abs(2*y-7)//2
  bonus=((6-y if p.isupper() else y-1)*9 if t=='p' else center*8 if t in 'nb' else center*3 if t in 'rq' else 0)
  if i in (opp if friendly else own) and i not in (own if friendly else opp):bonus-=V[t]*9//10
  v+=(V[t]+bonus)*(1 if friendly else -1)
 return v
def replies(b,w,ep=-1):
 for i,p in enumerate(b):
  if p=='.' or p.isupper()!=w:continue
  t=p.lower();x=i%8;y=i//8
  if t=='p':
   d=-1 if w else 1
   steps=[(0,d)] if 0<=y+d<8 and b[i+8*d]=='.' else []
   if steps and y==(6 if w else 1) and b[i+16*d]=='.':steps.append((0,2*d))
   steps += [(dx,d) for dx in (-1,1) if 0<=x+dx<8 and 0<=y+d<8 and ((b[i+8*d+dx]!='.' and b[i+8*d+dx].isupper()!=w) or i+8*d+dx==ep)]
  elif t=='n':steps=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
  else:steps=([(1,1),(-1,1),(1,-1),(-1,-1)] if t=='b' else [(1,0),(-1,0),(0,1),(0,-1)] if t=='r' else [(1,1),(-1,1),(1,-1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)])
  for dx,dy in steps:
   xx,yy=x+dx,y+dy
   while 0<=xx<8 and 0<=yy<8:
    j=yy*8+xx;q=b[j]
    if (q=='.' or q.isupper()!=w) and (t!='p' or (dx==0 and q=='.') or (dx!=0 and (q!='.' or j==ep))):
     if q.lower()!='k':
      n=b[:];n[i]='.';n[j]=p
      if t=='p' and j==ep and q=='.':n[j+(8 if w else -8)]='.'
      if t=='p' and yy==(0 if w else 7):n[j]='Q' if w else 'q'
      if n.index('K' if w else 'k') not in attacks(n,not w):yield n
    if q!='.' or t in 'pnk':break
    xx+=dx;yy+=dy
def search(b,w,us,d,lo,hi):
 global nodes
 nodes+=1
 if nodes>3000:raise TimeoutError
 if not d:return score(b,us)
 found=0
 for n in replies(b,w):
  found=1;v=search(n,not w,us,d-1,lo,hi)
  if w==us:lo=max(lo,v)
  else:hi=min(hi,v)
  if lo>=hi:break
 if not found:return 0
 return lo if w==us else hi
def main():
 global nodes
 while 1:
  s=post('/game',{})
  if s.get('status')=='done':return
  while s.get('status')=='your_move':
   legal=s['legal_moves']
   if not legal:break
   b=board(s['fen']);w=s['fen'].split()[1]=='w';m=sorted(legal)[0]
   nodes=0
   for depth in (1,2):
    best=-99999;chosen=m
    try:
     for q in sorted(legal):
      n=move(b,q);e=-1
      if b[sq(q[:2])].lower()=='p' and abs(sq(q[:2])-sq(q[2:4]))==16:e=(sq(q[:2])+sq(q[2:4]))//2
      a=1000000;found=0
      for r in replies(n,not w,e):
       found=1;a=min(a,search(r,w,w,depth-1,best,a))
       if a<=best:break
      if not found:a=100000 if n.index('k' if w else 'K') in attacks(n,w) else 0
      if a>best:best=a;chosen=q
     m=chosen
    except TimeoutError:break
   s=post('/move',{'game':s['game'],'move':m})
if __name__=='__main__':main()