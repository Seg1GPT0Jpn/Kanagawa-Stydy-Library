import sys; sys.path.insert(0,'.')
from probs import P
STAR={1:"★",2:"★★",3:"★★★"}
head='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>%s</title><link rel="stylesheet" href="base.css"><style>
.body{position:absolute;left:15mm;top:22mm;width:180mm;height:250mm}
.hashira{position:absolute;top:13mm;right:15mm;font:8pt/1 "Goth"}
.nombre{position:absolute;bottom:14mm;right:15mm;font:9pt/1 "Ser"}
.sec{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2pt solid #000;padding-bottom:1.5mm;margin-bottom:3mm}
.sec h2{font:700 14pt/1.4 "Goth"}
.sec .meta{font:8.5pt/1.5 "Goth";text-align:right}
.meta .ref{font-family:"Goth"}
.inst{font:700 9pt/1.6 "Goth";margin:3mm 0 1mm}
.q{padding:2mm 0;border-bottom:.35pt solid #000}
.qh{font:8.5pt/1.4 "Goth";display:flex;gap:3mm;align-items:center}
.qh .no{font:700 10pt "Goth";min-width:9mm}
.box3{display:inline-flex;gap:1mm}.box3 i{width:3.2mm;height:3.2mm;border:.5pt solid #000;display:inline-block}
.en{font-family:"Ser";font-size:10.5pt;line-height:1.7}
.ch{display:flex;gap:6mm;font-family:"Ser";font-size:10.5pt}
.ch span::before{content:attr(data-n);font-family:"Goth";font-size:9pt;margin-right:1.5mm}
u{text-decoration-thickness:.6pt;text-underline-offset:2px} sub{font:7.5pt "Goth";vertical-align:-1pt}
%s
</style></head><body><div class="page"><div class="hashira"><b>第1章</b>　問題</div><div class="body">
<div class="sec"><h2>1　関係代名詞の基本</h2><div class="meta">★〜★★★　5問　目安 8分<br><span class="ref">解説 → 完全解説book p.9〜11</span></div></div>
'''
tail='</div><div class="nombre">4</div></div></body></html>'
def qhtml(p):
    s=f'<div class="qh"><span class="no">問{p["no"]}</span><span>{STAR[p["lv"]]}</span><span class="box3"><i></i><i></i><i></i></span></div>'
    s+=f'<div class="en">{p["q"]}</div>'
    if "ch" in p: s+='<div class="ch">'+''.join(f'<span data-n="{"①②③④"[i]}">{c}</span>' for i,c in enumerate(p["ch"]))+'</div>'
    return s
def ansbox(p,wide):
    k=p["kind"]
    if k in("4択","正誤"): return '<div class="abox s"></div>'
    if k=="整序": return '<div class="aline"></div>'+('' if wide else '')
    return '<div class="aline"></div><div class="aline"></div>'
# 案P1: 答え欄を外側の欄に
css1='''.qr{display:grid;grid-template-columns:130mm 44mm;column-gap:6mm;border-bottom:.35pt solid #000;padding:2mm 0}
.qr .q{border:0;padding:0}.acol{border-left:.35pt solid #000;padding-left:3mm;display:flex;flex-direction:column;justify-content:flex-end;gap:1mm}
.abox.s{width:12mm;height:9mm;border:.75pt solid #000}.aline{height:8mm;border-bottom:.5pt solid #000}
.alab{font:7.5pt "Goth"}'''
b=''
for p in P:
    if p["inst"]: b+=f'<div class="inst">{p["inst"]}</div>'
    b+=f'<div class="qr"><div class="q">{qhtml(p)}</div><div class="acol"><span class="alab">解答</span>{ansbox(p,False)}</div></div>'
open('probP1.html','w').write(head%('試作P1',css1)+b+tail)
# 案P2: 答え欄を問題の下に
css2='''.arow{display:flex;align-items:flex-end;gap:3mm;margin-top:1.5mm}.alab{font:8pt "Goth"}
.abox.s{width:14mm;height:9mm;border:.75pt solid #000}.aline{flex:1;height:8mm;border-bottom:.5pt solid #000}
.q.long .arow{flex-direction:column;align-items:stretch}'''
b=''
for p in P:
    if p["inst"]: b+=f'<div class="inst">{p["inst"]}</div>'
    lg=' long' if p["kind"]=="和訳" else ''
    b+=f'<div class="q{lg}">{qhtml(p)}<div class="arow"><span class="alab">解答</span>{ansbox(p,True)}</div></div>'
open('probP2.html','w').write(head%('試作P2',css2)+b+tail)

# 案P3: 記号解答は外側欄、記述解答は全幅の線（行間10mm）
css3=css1+'''
.wl{grid-column:1/3;margin-top:1mm}.wl .aline{height:10mm;border-bottom:.5pt solid #000}
.wl .alab{display:block;margin-top:1mm}'''
b=''
for p in P:
    if p["inst"]: b+=f'<div class="inst">{p["inst"]}</div>'
    if p["kind"] in ("4択","正誤"):
        b+=f'<div class="qr"><div class="q">{qhtml(p)}</div><div class="acol"><span class="alab">解答</span><div class="abox s"></div></div></div>'
    else:
        n=1 if p["kind"]=="整序" else 2
        b+=f'<div class="qr"><div class="q">{qhtml(p)}</div><div></div><div class="wl"><span class="alab">解答</span>'+'<div class="aline"></div>'*n+'</div></div>'
open('probP3.html','w').write(head%('試作P3',css3)+b+tail)
