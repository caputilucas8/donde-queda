import json, collections
topo=json.load(open('ar.topo.json',encoding='utf-8'))
sc=topo['transform']['scale']; tr=topo['transform']['translate']
arcs=[]
for a in topo['arcs']:
    x=y=0; pts=[]
    for dx,dy in a:
        x+=dx; y+=dy; pts.append((x*sc[0]+tr[0], y*sc[1]+tr[1]))
    arcs.append(pts)
def arc(i):
    return arcs[i] if i>=0 else arcs[~i][::-1]
def ring(r):
    out=[]
    for i in r:
        p=arc(i); out.extend(p if not out else p[1:])
    return out
provs={}
for g in topo['objects']['provs']['geometries']:
    polys=g['arcs'] if g['type']=='MultiPolygon' else [g['arcs']]
    provs[g['properties']['prov']]=[[ring(r) for r in poly] for poly in polys]
def inring(x,y,r):
    c=False; n=len(r)
    for i in range(n):
        x1,y1=r[i]; x2,y2=r[i-1]
        if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
def pip(x,y):
    for k,polys in provs.items():
        for poly in polys:
            if inring(x,y,poly[0]) and not any(inring(x,y,h) for h in poly[1:]): return k
    return None
gn2indec={'01':'06','02':'10','03':'22','04':'26','05':'14','06':'18','07':'02','08':'30','09':'34','10':'38','11':'42','12':'46','13':'50','14':'54','15':'58','16':'62','17':'66','18':'70','19':'74','20':'78','21':'82','22':'86','23':'94','24':'90'}
rows=[]; fc=collections.Counter(); mism=[]
for line in open('cities1000.txt',encoding='utf-8'):
    f=line.rstrip('\n').split('\t')
    if f[8]!='AR': continue
    fc[f[7]]+=1
    if f[7] in ('PPLX','PPLH','PPLQ','PPLW','PPLCH'): continue
    name=f[1]; lat=float(f[4]); lon=float(f[5]); pop=int(f[14] or 0)
    a=gn2indec.get(f[10]); p=pip(lon,lat)
    if p and a and p!=a: mism.append((name,a,p,pop))
    prov=p or a
    rows.append(dict(n=name,lat=lat,lon=lon,p=prov,pop=pop,a=a,pp=p))
print(fc); print('rows',len(rows),'mismatch',len(mism)); 
for m in sorted(mism,key=lambda m:-m[3])[:40]: print(m)
print('outside',[(r['n'],r['pop']) for r in rows if not r['pp']][:40])
json.dump(rows,open('rows.json','w',encoding='utf-8'),ensure_ascii=False)

import math
fcode={}
for line in open('cities1000.txt',encoding='utf-8'):
    f=line.split('\t')
    if f[8]=='AR': fcode[(f[1],f[4])]=f[7]
def hav(a,b,c,d):
    a,b,c,d=map(math.radians,(a,b,c,d))
    h=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 2*6371*math.asin(math.sqrt(h))
out=[]
for line in open('cities1000.txt',encoding='utf-8'):
    f=line.rstrip('\n').split('\t')
    if f[8]!='AR' or f[7] in ('PPLX','PPLH','PPLQ','PPLW','PPLCH','PPLC'): continue
    name=f[1]
    if name.startswith('Barrio '): continue
    name={'Gobernador Virasora':'Gobernador Virasoro','El Quebachal':'El Quebrachal','Huanchillas':'Huanchilla'}.get(name,name)
    lat=float(f[4]); lon=float(f[5]); pop=int(f[14] or 0)
    prov=pip(lon,lat) or gn2indec[f[10]]
    amba=1 if prov in ('02','06') and hav(lat,lon,-34.6037,-58.3816)<45 else 0
    cap=1 if f[7]=='PPLA' else 0
    out.append([name,round(lat,4),round(lon,4),prov,pop,cap,amba])
json.dump(out,open('cities.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(len(out),'facil',sum(1 for c in out if c[5] or (c[4]>=100000 and not c[6])),'amba',sum(c[6] for c in out))
print([c[0] for c in out if c[5]])
