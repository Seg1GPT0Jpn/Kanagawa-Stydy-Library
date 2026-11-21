"""4冊の組み方。build.py から呼ばれる。"""
import html, json
from build import STAR, CIRC

A4 = dict(pw=210, ph=297, top=22, bottom=25, inner=15, outer=15, mainW=134, gap=6, sideW=40, startPage=1)
A4_1COL = dict(A4, mainW=180, gap=0, sideW=0)
A5 = dict(pw=148, ph=210, top=18, bottom=22, inner=18, outer=19, mainW=111, gap=0, sideW=0, startPage=1)

E = html.escape


def blk(inner, cls='', notes='', **data):
    d = ''.join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in data.items() if v is not None)
    return f'<div class="blk {cls}"{d}>{inner}{notes}</div>'


def note_html(bk, nt, pages):
    k = nt['kind']
    if k == '語注':
        body = '<br>'.join(f'<span class="en">{E(a)}</span><br><span class="gl">{E(b)}</span>' for a, b in nt['items'])
        return f'<div class="sn"><span class="lab">語注</span>{body}</div>'
    if k == '用語':
        return f'<div class="sn"><span class="lab">用語　{E(nt["term"])}</span>{bk.md(nt["text"], pages)}</div>'
    return f'<div class="sn"><span class="lab">{E(k)}</span>{bk.md(nt["text"], pages)}</div>'


def legend_blocks(legend):
    parts = legend.split('<!--split-->')
    out = []
    for i, p in enumerate(parts):
        if i == 0:
            out.append(blk(f'<div class="lg">{p}</div>', 'newpage legend', anchor='legend', chapter='本書の使い方', section='本書の使い方'))
        else:
            out.append(blk(f'<div class="lg">{p}</div>', 'legend'))
    return out


def fullpage(inner, kind='nohead', **data):
    return blk(inner, 'fullpage', pagekind=kind, **data)


# ====================================================================
# 完全解説book
# ====================================================================
KAISETSU_CSS = '''
.page { width: 210mm; height: 297mm; }
@page { size: 210mm 297mm; margin: 0; }
.blk { padding-bottom: 0; }
.maincol p, .blk.p { text-align: justify; }
.blk.p > p { text-indent: 1em; margin-bottom: 1.2mm; }
.blk.h2 { padding: 0 0 1.5mm; border-bottom: 1.2pt solid #000; margin-bottom: 4mm; margin-top: 7mm; display: flex; gap: 3mm; font: 700 14pt/1.4 "Goth"; }
.blk.h2.first { margin-top: 0; }
.blk.h3 { font: 700 11pt/1.5 "Goth"; margin: 4.5mm 0 1.2mm; }
.blk.h3.first { margin-top: 0; }
.blk.chap { margin: 0 0 10mm; padding-top: 6mm; }
.chap .cno { font: 700 11pt/1 "Goth"; letter-spacing: .1em; }
.chap .ct { font: 700 20pt/1.4 "Goth"; margin-top: 3mm; padding-bottom: 3mm; border-bottom: 1.2pt solid #000; }
.chap .lead { font-size: 9.5pt; margin-top: 3mm; }
.blk.ex { display: grid; grid-template-columns: 8mm 1fr; padding: 1.2mm 0; border-bottom: .35pt solid #000; }
.blk.ex.top, .blk.ex.first { border-top: .35pt solid #000; margin-top: 1.5mm; }
.blk.ex.last { margin-bottom: 2mm; }
.ex .n { font: 9pt/1.9 "Goth"; }
.ex .e { font-family: "Ser"; font-size: 10.5pt; line-height: 1.55; }
.ex .j { font: 9pt/1.6 "Min"; }
.blk.steps { margin: .5mm 0 1.5mm; }
.steps div { padding-left: 2.6em; text-indent: -2.6em; }
.steps b { font: 700 9.5pt "Goth"; margin-right: .6em; }
table.t { border-collapse: collapse; width: 100%; margin: 1.5mm 0 3mm; font-size: 9.5pt; line-height: 1.5; }
table.t th, table.t td { border: .5pt solid #000; padding: 1.2mm 2mm; text-align: center; }
table.t thead th { background: var(--net); font: 700 9pt/1.4 "Goth"; }
table.t tbody th { font: 700 9pt/1.4 "Goth"; text-align: left; background: var(--net); white-space: nowrap; }
table.t td { font-family: "Ser", "Min"; font-size: 10pt; }
.blk.check { border: .75pt solid #000; padding: 2mm 3mm; margin: 3mm 0 2mm; }
.check .t { font: 700 9pt/1.6 "Goth"; }
.check .r { display: grid; grid-template-columns: 7mm 1fr 32mm; align-items: baseline; }
.check .q { font-family: "Ser"; }
.check .a { font-family: "Ser", "Min"; text-align: center; border-bottom: .35pt solid #000; }
.check .r.long { grid-template-columns: 7mm 1fr; }
.check .r.long .a { grid-column: 2; text-align: left; padding-left: 2mm; }
.sn { font: 8pt/1.6 "Goth"; padding: 1.2mm 0 3mm; border-top: .35pt solid #000; }
.sn .lab { font-weight: 700; display: block; }
.sn .en { font-family: "Ser"; font-size: 8.5pt; }
.sn .gl { padding-left: 1em; }
/* 前付・後付 */
.page > .blk.fullpage { position: absolute; inset: 0; }
.fm-title { font: 700 16pt/1.4 "Goth"; padding-bottom: 2mm; border-bottom: 1.2pt solid #000; margin-bottom: 5mm; }
.toc .tc { display: flex; font: 700 10.5pt/1.5 "Goth"; margin-top: 4mm; }
.toc .ts { display: flex; font-size: 10pt; line-height: 1.9; padding-left: 2em; }
.toc .dots { flex: 1; border-bottom: .35pt dotted #000; margin: 0 2mm .45em; }
.toc .pg { font-family: "Ser"; min-width: 6mm; text-align: right; }
.idx { column-count: 2; column-gap: 8mm; font-size: 9.5pt; line-height: 1.8; }
.idx .row { display: flex; }
.idx .k { font: 700 9pt/2 "Goth"; margin-top: 2mm; border-bottom: .35pt solid #000; }
.colo { position: absolute; left: 15mm; right: 15mm; bottom: 30mm; font-size: 8.5pt; line-height: 1.7; border-top: .75pt solid #000; padding-top: 4mm; }
.colo .bt { font: 700 12pt/1.5 "Goth"; margin-bottom: 3mm; }
.colo table td { padding: .3mm 4mm .3mm 0; vertical-align: top; }
.colo .warn { border: .75pt solid #000; padding: 2mm 3mm; margin: 0 0 4mm; font-size: 9pt; }
'''


def kaisetsu_blocks(bk, pages, cover_html, colophon_html, legend_html):
    d = bk.data
    out = [fullpage(cover_html, 'nohead pk-cover', anchor='cover')]
    out.append(fullpage('', 'nohead pk-blank'))
    out.extend(legend_blocks(legend_html))
    # 目次
    toc = ['<div class="fm-title">目次</div><div class="toc">']
    for ch in d['chapters']:
        toc.append(f'<div class="tc">第{ch["no"]}章　{E(ch["title"])}<span class="dots"></span><span class="pg">{pages.get(ch["id"], "00")}</span></div>')
        for s in ch['sections']:
            toc.append(f'<div class="ts">{s["no"]}　{E(s["title"])}<span class="dots"></span><span class="pg">{pages.get(s["id"], "00")}</span></div>')
    toc.append(f'<div class="tc">索引<span class="dots"></span><span class="pg">{pages.get("index", "00")}</span></div></div>')
    out.append(blk(''.join(toc), 'newpage', anchor='toc', chapter='目次', section='目次'))
    for ch in d['chapters']:
        chap_label = f'第{ch["no"]}章　{ch["title"]}'
        lead = f'<div class="lead">{bk.md(ch["lead"], pages)}</div>' if ch.get('lead') else ''
        out.append(blk(f'<div class="cno">第{ch["no"]}章</div><div class="ct">{E(ch["title"])}</div>{lead}', 'chap newpage keepnext', anchor=ch['id'], chapter=chap_label))
        for s in ch['sections']:
            out.append(blk(f'<span>{s["no"]}</span><span>{E(s["title"])}</span>', 'h2 keepnext', anchor=s['id'], section=f'{s["no"]}　{s["title"]}'))
            exmap = {e['id']: e for e in s.get('examples', [])}
            hno = 0
            for b in s['body']:
                notes = ''.join(note_html(bk, n, pages) for n in (b.get('notes') or []))
                if 'h' in b:
                    hno += 1
                    out.append(blk(f'({hno}) {E(b["h"])}', 'h3 keepnext'))
                elif 'p' in b:
                    out.append(blk(f'<p>{bk.md(b["p"], pages)}</p>', 'p', notes))
                elif 'ex' in b:
                    ids = b['ex']
                    for i, eid in enumerate(ids):
                        e = exmap[eid]
                        gl = ''
                        if e.get('gloss'):
                            gl = note_html(bk, {'kind': '語注', 'items': e['gloss']}, pages)
                        cls = 'ex' + (' top' if i == 0 else '') + (' last' if i == len(ids) - 1 else '')
                        nt = notes if i == 0 else ''
                        out.append(blk(f'<span class="n">{bk.ex_no[eid]}</span><div><div class="e">{bk.md(e["en"], pages)}</div><div class="j">{bk.md(e["ja"], pages)}</div></div>', cls, nt + gl, anchor=eid))
                elif 'steps' in b:
                    rows = ''.join(f'<div><b>問{i}</b>{bk.md(t, pages)}</div>' for i, t in enumerate(b['steps'], 1))
                    out.append(blk(rows, 'steps', notes))
                elif 'table' in b:
                    t = b['table']
                    th = ''.join(f'<th>{bk.md(c, pages)}</th>' for c in t['head'])
                    tr = ''.join('<tr><th>' + bk.md(r[0], pages) + '</th>' + ''.join(f'<td>{bk.md(c, pages)}</td>' for c in r[1:]) + '</tr>' for r in t['rows'])
                    out.append(blk(f'<table class="t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>', 'tbl', notes))
                elif 'check' in b:
                    rows = ''.join(f'<div class="r{" long" if len(str(c["a"])) > 12 else ""}"><span>({i})</span><span class="q">{bk.md(c["q"], pages)}</span><span class="a ans">{bk.md(c["a"], pages)}</span></div>' for i, c in enumerate(b['check'], 1))
                    out.append(blk(f'<div class="t">確認　{E(b.get("inst", "［　］に入る語を答えなさい。答えは赤シートで隠して確かめる。"))}</div>{rows}', 'check', notes))
                else:
                    raise SystemExit(f'未知の本文ブロック: {b}')
    # 索引
    terms = sorted(bk.terms.items(), key=lambda kv: kv[1])
    rows = []; cur = None
    for t, yomi in terms:
        g = gojuon_row(yomi)
        if g != cur:
            rows.append(f'<div class="k">{g}</div>'); cur = g
        rows.append(f'<div class="row">{E(t)}<span class="dots"></span><span class="pg">{pages.get("term:" + t, "00")}</span></div>')
    out.append(blk('<div class="fm-title">索引</div><div class="idx toc">' + ''.join(rows) + '</div>', 'newpage', anchor='index', chapter='索引', section='索引'))
    # 4の倍数にそろえる白ページ（奥付・裏表紙の前）
    pad = 0
    if 'colophon' in pages:
        n_before = (pages['pad'] if 'pad' in pages else pages['colophon']) - 1
        pad = (-(n_before + 2)) % 4
    for i in range(pad):
        out.append(fullpage('', 'nohead pk-blank', **({'anchor': 'pad'} if i == 0 else {})))
    out.append(fullpage(colophon_html, 'nohead', anchor='colophon'))
    out.append(fullpage(back_html(bk, '') if False else _back, 'nohead pk-back', anchor='backcover'))
    return out


GOJUON = [('あ', 'あいうえおぁぃぅぇぉ'), ('か', 'かきくけこがぎぐげご'), ('さ', 'さしすせそざじずぜぞ'), ('た', 'たちつてとだぢづでどっ'),
          ('な', 'なにぬねの'), ('は', 'はひふへほばびぶべぼぱぴぷぺぽ'), ('ま', 'まみむめも'), ('や', 'やゆよゃゅょ'), ('ら', 'らりるれろ'), ('わ', 'わをん')]


def gojuon_row(yomi):
    c = yomi[0]
    for k, chars in GOJUON:
        if c in chars:
            return k
    return '英字・記号'


# ====================================================================
# 表紙・凡例・奥付（仮。表紙は試作で決める）
# ====================================================================
def cover_html(bk, part):
    from cover import relclause_svg, EG01
    b = bk.data['book']
    return f'''<div class="cv"><div class="cv-series"><span>{E(b["series"])}</span><span>{b["vol"]}</span></div>
<div class="cv-title">{E(b["title"])}</div><div class="cv-sub">{E(part)}</div>
<div class="cv-fig">{relclause_svg(**EG01)}</div>
<div class="cv-note">関係詞節は、欠けた語の代わりに先行詞を後ろから説明する。<br>大学入学共通テスト・GMARCH 個別試験の水準まで。</div>
<div class="cv-pub">{E(b["publisher"])}</div></div>'''


def back_html(bk, part):
    b = bk.data['book']
    return f'''<div class="cv"><div class="cv-back">{E(b["series"])} {b["vol"]}　{E(b["title"])}<br>
完全解説book・要点まとめbook・問題集・解答解説（4冊組）<br><br>
本書は無料の教材です。{E(b["license"])} のもとで、出典を表示すれば自由に複製・配布・改変できます。<br>
人間の専門家による確認を受ける前の版です。使う前に奥付の「ご利用の前に」をお読みください。</div>
<div class="cv-pub">{E(b["publisher"])}</div></div>'''


COVER_CSS = '''
.cv { position: absolute; inset: 0; }
.cv-series { position: absolute; left: 20mm; right: 20mm; top: 24mm; border-bottom: .75pt solid #000; padding-bottom: 3mm; display: flex; justify-content: space-between; font: 700 10pt/1 "Goth"; letter-spacing: .2em; }
.cv-title { position: absolute; left: 20mm; top: 48mm; font: 700 38pt/1.25 "Goth"; }
.cv-sub { position: absolute; left: 20mm; top: 72mm; font: 700 15pt/1.4 "Goth"; }
.cv-fig { position: absolute; left: 20mm; right: 20mm; top: 110mm; height: 84mm; background: var(--net); display: flex; align-items: center; justify-content: center; }
.cv-note { position: absolute; left: 20mm; top: 202mm; font: 9.5pt/1.6 "Goth"; }
.cv-pub { position: absolute; left: 20mm; right: 20mm; bottom: 22mm; border-top: .35pt solid #000; padding-top: 3mm; font: 9.5pt/1.6 "Goth"; }
.cv-back { position: absolute; left: 20mm; right: 20mm; top: 200mm; font: 9pt/1.8 "Goth"; }
'''



def legend_html(bk, part):
    return f'''<div class="fm-title">本書の使い方</div>

<p>本書は「{E(bk.data["book"]["title"])}」の4冊組のうちの{E(part)}です。4冊は同じ1つのデータから作っているので、問題番号やページの参照は4冊の間で一致します。</p>
<table class="t lgt"><tbody>
<tr><th>完全解説book</th><td>なぜそうなるかから説明した本体。例文・確認問題つき。</td></tr>
<tr><th>要点まとめbook</th><td>持ち歩き用の A5 判。赤字を赤シートで隠して思い出す。</td></tr>
<tr><th>問題集</th><td>書き込み式。節末問題・章末問題・模擬試験。</td></tr>
<tr><th>解答解説</th><td>全問に正解・根拠・よくある間違い・完全解説book のページ。</td></tr>
</tbody></table>
<!--split--><div class="lgh">記号</div>
<table class="t lgt"><tbody>
<tr><th>［　］</th><td>関係詞節の範囲</td></tr>
<tr><th><span class="rp">who</span></th><td>関係詞（太字と下線）</td></tr>
<tr><th><span class="gap"></span></th><td>関係詞節の中で欠けている位置</td></tr>
<tr><th>→ p.16</th><td>本書の16ページを参照</td></tr>
<tr><th><span class="ans">赤字</span></th><td>赤シートで隠して答える部分。赤はこの用途にだけ使う</td></tr>
<tr><th>★／★★／★★★</th><td>共通テスト水準／GMARCH 標準／入試より難しい発展</td></tr>
<tr><th>□□□</th><td>解いた記録。1回目・1週間後・1か月後に1つずつ印を付ける</td></tr>
</tbody></table>
<!--split--><div class="lgh">進め方</div>
<p>1節ずつ、完全解説book を読む → 節の最後の「確認」を赤シートで隠して答える → 問題集の節末問題を解く → 解答解説で答え合わせ、の順に進めます。間違えた問題は1週間後と1か月後にもう一度解き、□に印を付けます。時間をあけて思い出すほうが、続けて読み返すより長く覚えていられることが、実験で確かめられています。</p>
'''


LEGEND_CSS = '''
.lg p { text-indent: 1em; text-align: justify; margin-bottom: 2mm; }
.lgh { font: 700 11pt/1.5 "Goth"; margin: 5mm 0 1.5mm; }
table.lgt th { width: 34mm; text-align: left; font-weight: 700; }
table.lgt td { text-align: left; font-family: "Min"; font-size: 9.5pt; }
'''


def colophon_html(bk, part):
    b = bk.data['book']
    return f'''<div class="colo">
<div class="warn"><b>ご利用の前に</b>　本書の本文・例文・問題・解説は AI（Claude）が作成し、自動検査と AI による点検を行ったものです。人間の専門家（英語の教員など）による確認はまだ受けていません。授業や配布に使う前に、必ず専門家の確認を受けてください。誤りを見つけた場合は配布ページでお知らせください。</div>
<div class="bt">{E(b["series"])} {b["vol"]}　{E(b["title"])}　{E(part)}</div>
<table><tbody>
<tr><td>版</td><td>{E(b["edition"])}（{E(b["date"])}）</td></tr>
<tr><td>発行</td><td>{E(b["publisher"])}</td></tr>
<tr><td>ライセンス</td><td>{E(b["license"])}（クリエイティブ・コモンズ 表示 4.0 国際）。出典を表示すれば、複製・改変・再配布・商用利用ができます。https://creativecommons.org/licenses/by/4.0/deed.ja</td></tr>
<tr><td>書体</td><td>BIZ UDP明朝・BIZ UDPゴシック（Copyright 2022 The BIZ UDMincho / BIZ UDGothic Project Authors）、Source Serif 4（Copyright 2014–2023 Adobe, with Reserved Font Name ‘Source’）。いずれも SIL Open Font License 1.1。</td></tr>
<tr><td>問題について</td><td>問題・例文・長文はすべて本書のための書き下ろしです。実際の入試問題は出題形式の分析にだけ使い、文章は使っていません。</td></tr>
</tbody></table></div>'''


# ====================================================================
# 問題集・解答解説
# ====================================================================
PROB_CSS = '''
.blk.sech { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1.2pt solid #000; padding-bottom: 1.5mm; margin: 7mm 0 2mm; }
.blk.sech.first { margin-top: 0; }
.sech .tt { font: 700 13pt/1.4 "Goth"; }
.sech .meta { font: 8.5pt/1.5 "Goth"; text-align: right; white-space: nowrap; padding-left: 4mm; }
.blk.inst { font: 700 9pt/1.6 "Goth"; margin: 3mm 0 .5mm; }
.blk.inst.first { margin-top: 0; }
.blk.qr { display: grid; grid-template-columns: 130mm 44mm; column-gap: 6mm; border-bottom: .35pt solid #000; padding: 2mm 0; }
.qh { font: 8.5pt/1.4 "Goth"; display: flex; gap: 3mm; align-items: center; margin-bottom: .5mm; }
.qh .no { font: 700 10pt "Goth"; min-width: 10mm; }
.box3 { display: inline-flex; gap: 1mm; } .box3 i { width: 3.2mm; height: 3.2mm; border: .5pt solid #000; display: inline-block; }
.qt { font-family: "Ser", "Min"; font-size: 10.5pt; line-height: 1.7; }
.qt .ja { font-family: "Min"; font-size: 10pt; }
.psg { font-family: "Ser"; font-size: 10pt; line-height: 1.65; text-align: justify; margin: 1mm 0 2mm; padding: 2mm 3mm; border: .5pt solid #000; }
.ch { display: flex; flex-wrap: wrap; column-gap: 6mm; font-family: "Ser", "Min"; font-size: 10.5pt; line-height: 1.7; }
.ch.col { flex-direction: column; }
.ch span .cn { font-family: "Goth"; font-size: 9pt; margin-right: 1.5mm; }
.acol { border-left: .35pt solid #000; padding-left: 3mm; display: flex; flex-direction: column; justify-content: flex-end; gap: 1mm; }
.abox { width: 12mm; height: 9mm; border: .75pt solid #000; }
.alab { font: 7.5pt "Goth"; }
.wl { grid-column: 1 / 3; margin-top: 1mm; }
.wl .aline { height: 10mm; border-bottom: .5pt solid #000; }
.wl .aline:last-child { border-bottom: 0; }
.blk.qr.w { border-bottom: .5pt solid #000; }
/* 解答解説 */
.blk.ka { border-bottom: .35pt solid #000; padding: 2mm 0 2.2mm; }
.ka .hd { display: flex; gap: 3mm; align-items: baseline; font: 8.5pt/1.5 "Goth"; }
.ka .hd .no { font: 700 10pt "Goth"; min-width: 10mm; }
.ka .ans-l { font: 700 10pt/1.6 "Goth"; }
.ka .ans-v { font-family: "Ser", "Min"; font-size: 10.5pt; }
.ka dl { display: grid; grid-template-columns: 22mm 1fr; font-size: 9.5pt; line-height: 1.7; margin-top: .5mm; }
.ka dt { font: 700 8.5pt/2 "Goth"; }
.ka dd { text-align: justify; }
'''


def prob_header(bk, title, probs, ref_html=''):
    lvs = sorted({p['lv'] for p in probs})
    star = STAR[lvs[0]] + ('〜' + STAR[lvs[-1]] if len(lvs) > 1 else '')
    mins = sum(p['min'] for p in probs)
    return f'<span class="tt">{title}</span><span class="meta">{star}　{len(probs)}問　目安 {mins}分{"<br>" + ref_html if ref_html else ""}</span>'


def q_body(bk, p, pages):
    s = f'<div class="qh"><span class="no">問{p["no"]}</span><span>{STAR[p["lv"]]}</span><span class="box3"><i></i><i></i><i></i></span></div>'
    q = p['q']
    if p['kind'] == '読解' and p.get('passage'):
        s += f'<div class="psg">{bk.md(p["passage"], pages)}</div>'
    s += f'<div class="qt">{bk.md(q, pages)}</div>'
    if p.get('choices'):
        if p['kind'] == '正誤':
            pass
        else:
            longc = any(len(str(c)) > 18 for c in p['choices'])
            s += f'<div class="ch{" col" if longc else ""}">' + ''.join(f'<span><span class="cn">{CIRC[i]}</span>{bk.md(c, pages)}</span>' for i, c in enumerate(p['choices'])) + '</div>'
    return s


def mondai_blocks(bk, pages, part, cover, colophon, legend):
    kp = bk.pages  # 完全解説book のページ
    out = [fullpage(cover, 'nohead pk-cover', anchor='cover'), fullpage('', 'nohead pk-blank')]
    out.extend(legend_blocks(legend))
    toc = ['<div class="fm-title">目次</div><div class="toc">']
    for ch in bk.data['chapters']:
        toc.append(f'<div class="tc">第{ch["no"]}章　{E(ch["title"])}<span class="dots"></span><span class="pg">{pages.get(ch["id"], "00")}</span></div>')
        for s in ch['sections']:
            toc.append(f'<div class="ts">{s["no"]}　{E(s["title"])}<span class="dots"></span><span class="pg">{pages.get("m" + s["id"], "00")}</span></div>')
        toc.append(f'<div class="ts">章末問題<span class="dots"></span><span class="pg">{pages.get("end" + ch["id"], "00")}</span></div>')
    if any(p['set'] == '模試' for p in bk.problems):
        toc.append(f'<div class="tc">模擬試験<span class="dots"></span><span class="pg">{pages.get("mock", "00")}</span></div>')
    toc.append('</div>')
    out.append(blk(''.join(toc), 'newpage', anchor='toc', chapter='目次', section='目次'))

    def emit(probs):
        last_inst = None
        for p in probs:
            inst = p.get('inst') or last_inst
            if p.get('inst') and p['inst'] != last_inst:
                out.append(blk(bk.md(p['inst'], pages), 'inst keepnext'))
            last_inst = inst
            body = q_body(bk, p, pages)
            if p['kind'] in ('4択', '正誤') or (p['kind'] == '読解' and p.get('choices')):
                out.append(blk(f'<div class="q">{body}</div><div class="acol"><span class="alab">解答</span><div class="abox"></div></div>', 'qr', anchor='q' + str(p['no'])))
            else:
                n = {'整序': 1, '補充': 1, '和訳': 2, '英作': 2, '読解': 2}[p['kind']]
                out.append(blk(f'<div class="q">{body}</div><div></div><div class="wl"><span class="alab">解答</span>' + '<div class="aline"></div>' * (n + 1) + '</div>', 'qr w', anchor='q' + str(p['no'])))

    for ch in bk.data['chapters']:
        chap_label = f'第{ch["no"]}章　{ch["title"]}'
        out.append(blk(f'<div class="cno">第{ch["no"]}章</div><div class="ct">{E(ch["title"])}</div>', 'chap newpage keepnext', anchor=ch['id'], chapter=chap_label))
        for s in ch['sections']:
            probs = [p for p in bk.problems if p['sec'] == s['id'] and p['set'] == '節末']
            if not probs: continue
            ref = f'解説 → 完全解説book p.{kp.get(s["id"], "00")}'
            out.append(blk(prob_header(bk, f'{s["no"]}　{E(s["title"])}', probs, ref), 'sech keepnext', anchor='m' + s['id'], section=f'{s["no"]}　{s["title"]}'))
            emit(probs)
        probs = [p for p in bk.problems if p['set'] == '章末' and bk.ch_of[p['sec']] is ch]
        if probs:
            out.append(blk(prob_header(bk, f'第{ch["no"]}章　章末問題', probs, '節を混ぜて出題'), 'sech keepnext newpage', anchor='end' + ch['id'], section=f'第{ch["no"]}章　章末問題'))
            emit(probs)
    mock = [p for p in bk.problems if p['set'] == '模試']
    if mock:
        out.append(blk(prob_header(bk, '模擬試験', mock, '解答時間 45分'), 'sech keepnext newpage', anchor='mock', chapter='模擬試験', section='模擬試験'))
        emit(mock)
    pad_and_colophon(out, pages, colophon)
    return out


_back = ''


def pad_and_colophon(out, pages, colophon):
    pad = 0
    if 'colophon' in pages:
        n_before = (pages['pad'] if 'pad' in pages else pages['colophon']) - 1
        pad = (-(n_before + 2)) % 4
    for i in range(pad):
        out.append(fullpage('', 'nohead pk-blank', **({'anchor': 'pad'} if i == 0 else {})))
    out.append(fullpage(colophon, 'nohead', anchor='colophon'))
    out.append(fullpage(back_html(bk, '') if False else _back, 'nohead pk-back', anchor='backcover'))


def ans_text(bk, p, pages):
    a = str(p['ans'])
    if p['kind'] in ('4択', '読解') and p.get('choices') and a.isdigit():
        return f'{CIRC[int(a) - 1]}　{bk.md(p["choices"][int(a) - 1], pages)}'
    if p['kind'] == '正誤' and a.isdigit():
        fix = f'　（正しくは {bk.md(p["fix"], pages)}）' if p.get('fix') else ''
        return f'{CIRC[int(a) - 1]}{fix}'
    return bk.md(a, pages)


def kaitou_blocks(bk, pages, part, cover, colophon, legend):
    kp = bk.pages
    out = [fullpage(cover, 'nohead pk-cover', anchor='cover'), fullpage('', 'nohead pk-blank')]
    out.extend(legend_blocks(legend))
    cur_ch = None
    for p in bk.problems:
        ch = bk.ch_of[p['sec']]
        if p['set'] == '模試':
            if cur_ch != 'mock':
                out.append(blk('<span class="tt">模擬試験　解答解説</span>', 'sech keepnext newpage', anchor='mock', chapter='模擬試験', section='模擬試験'))
                cur_ch = 'mock'
        elif ch is not cur_ch:
            out.append(blk(f'<span class="tt">第{ch["no"]}章　{E(ch["title"])}</span>', 'sech keepnext' + (' newpage' if cur_ch else ''), anchor=ch['id'],
                           chapter=f'第{ch["no"]}章　{ch["title"]}', section=f'第{ch["no"]}章　{ch["title"]}'))
            cur_ch = ch
        alt = ''
        if p.get('alt'):
            alt = '<dt>別解</dt><dd>' + '／'.join(bk.md(a, pages) for a in p['alt']) + '</dd>'
        ref = p.get('ref') or p['sec']
        side = f'<div class="sn"><span class="lab">参照</span>完全解説book<br>{bk.sec_no[ref]}　{E(bk.sec_title[ref])}<br><span class="pref">→&nbsp;p.{kp.get(ref, "00")}</span></div>'
        label = f'問{p["no"]}' if p['set'] != '模試' else f'第{p["no"]}問'
        out.append(blk(f'''<div class="hd"><span class="no">{label}</span><span>{STAR[p["lv"]]}</span><span>{E(p["kind"])}</span></div>
<div><span class="ans-l">正解　</span><span class="ans-v ans">{ans_text(bk, p, pages)}</span></div>
<dl>{alt}<dt>根拠</dt><dd>{bk.md(p["why"], pages)}</dd><dt>よくある間違い</dt><dd>{bk.md(p["trap"], pages)}</dd></dl>''', 'ka', side, anchor='q' + str(p['no'])))
    pad_and_colophon(out, pages, colophon)
    return out


# ====================================================================
# 要点まとめbook（A5）
# ====================================================================
MATOME_CSS = '''
.page { width: 148mm; height: 210mm; }
@page { size: 148mm 210mm; margin: 0; }
body { font-size: 9pt; }
.hashira { font-size: 7.5pt; } .nombre { font-size: 8.5pt; }
.blk.sech { border-bottom: 1pt solid #000; padding-bottom: 1mm; margin: 5mm 0 1.5mm; display: flex; justify-content: space-between; align-items: flex-end; }
.blk.sech.first { margin-top: 0; }
.sech .tt { font: 700 11pt/1.4 "Goth"; }
.sech .meta { font: 7.5pt/1.4 "Goth"; white-space: nowrap; padding-left: 3mm; }
.blk.sm { display: grid; grid-template-columns: 6mm 1fr; padding: 1mm 0; border-bottom: .35pt solid #000; line-height: 1.75; }
.sm .n { font: 8pt/1.9 "Goth"; }
.blk.chap { margin: 0 0 6mm; padding-top: 3mm; }
.chap .cno { font: 700 9pt/1 "Goth"; letter-spacing: .1em; }
.chap .ct { font: 700 15pt/1.4 "Goth"; margin-top: 2mm; padding-bottom: 2mm; border-bottom: 1pt solid #000; }
.fm-title { font-size: 13pt; }
.cv-series { left: 14mm; right: 14mm; top: 16mm; font-size: 8pt; }
.cv-title { left: 14mm; top: 32mm; font-size: 26pt; }
.cv-sub { left: 14mm; top: 49mm; font-size: 11pt; }
.cv-fig { left: 14mm; right: 14mm; top: 72mm; height: 62mm; }
.cv-fig svg { width: 118mm; height: auto; }
.cv-note { left: 14mm; top: 140mm; font-size: 7.5pt; }
.cv-pub { left: 14mm; right: 14mm; bottom: 15mm; font-size: 8pt; }
.cv-back { left: 14mm; right: 14mm; top: 135mm; font-size: 7.5pt; }
.colo { left: 12mm; right: 12mm; bottom: 20mm; font-size: 7.5pt; }
'''


def matome_blocks(bk, pages, part, cover, colophon, legend):
    kp = bk.pages
    out = [fullpage(cover, 'nohead pk-cover', anchor='cover'), fullpage('', 'nohead pk-blank')]
    out.extend(legend_blocks(legend))
    for ch in bk.data['chapters']:
        out.append(blk(f'<div class="cno">第{ch["no"]}章</div><div class="ct">{E(ch["title"])}</div>', 'chap newpage keepnext', anchor=ch['id'], chapter=f'第{ch["no"]}章　{ch["title"]}'))
        for s in ch['sections']:
            if not s.get('summary'): continue
            out.append(blk(f'<span class="tt">{s["no"]}　{E(s["title"])}</span><span class="meta">→ 完全解説book p.{kp.get(s["id"], "00")}</span>', 'sech keepnext', anchor=s['id'], section=f'{s["no"]}　{s["title"]}'))
            for i, t in enumerate(s['summary'], 1):
                out.append(blk(f'<span class="n">{i}</span><div>{bk.md(t, pages)}</div>', 'sm'))
    pad_and_colophon(out, pages, colophon)
    return out


def build_all(bk):
    b = bk.data['book']
    css_common = KAISETSU_CSS + COVER_CSS + LEGEND_CSS
    def go(name, part, cfg, fn, css):
        global _back
        _back = back_html(bk, part)
        lay = bk.render(name, f'{b["title"]} {part}', css, json.dumps(cfg),
                        lambda pages: fn(bk, pages, part, cover_html(bk, part), colophon_html(bk, part), legend_html(bk, part)))
        print(f'{part}: {lay["pages"]} ページ')
        return lay
    lay = go('kaisetsu', '完全解説book', A4, lambda bk, pages, part, c, col, lg: kaisetsu_blocks(bk, pages, c, col, lg), css_common)
    bk.pages = lay['anchors']
    (bk.out / 'pages_kaisetsu.json').write_text(json.dumps(lay['anchors'], ensure_ascii=False, indent=1))
    go('matome', '要点まとめbook', A5, matome_blocks, css_common + MATOME_CSS)
    go('mondai', '問題集', A4_1COL, mondai_blocks, css_common + PROB_CSS)
    go('kaitou', '解答解説', A4, kaitou_blocks, css_common + PROB_CSS)
