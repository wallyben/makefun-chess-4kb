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
  if i in (opp if friendly else own) and i not in (own if friendly else opp):bonus-=V[t]//3
  v+=(V[t]+bonus)*(1 if friendly else -1)
 return v
def main():
 while True:
  s=post('/game',{})
  if s.get('status')=='done':return
  while s.get('status')=='your_move':
   legal=s['legal_moves']
   if not legal:break
   b=board(s['fen']);w=s['fen'].split()[1]=='w'
   m=max(sorted(legal),key=lambda m:score(move(b,m),w))
   s=post('/move',{'game':s['game'],'move':m})
if __name__=='__main__':main()
