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
.sn { font: 8pt/1.6 "Goth"; padding: 1.2mm 0 3mm; border-top: .35pt solid #000; }
.sn .lab { font-weight: 700; display: block; }
.sn .en { font-family: "Ser"; font-size: 8.5pt; }
.sn .gl { padding-left: 1em; }
/* 前付・後付 */
.cover { position: absolute; inset: 0; }
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
    out = [fullpage(cover_html, 'nohead cover', anchor='cover')]
    out.append(fullpage('', 'nohead blank'))
    out.append(blk(legend_html, 'newpage legend', anchor='legend', chapter='本書の使い方', section='本書の使い方'))
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
                    rows = ''.join(f'<div class="r"><span>({i})</span><span class="q">{bk.md(c["q"], pages)}</span><span class="a ans">{bk.md(c["a"], pages)}</span></div>' for i, c in enumerate(b['check'], 1))
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
        out.append(fullpage('', 'nohead blank', **({'anchor': 'pad'} if i == 0 else {})))
    out.append(fullpage(colophon_html, 'nohead', anchor='colophon'))
    out.append(fullpage('<div class="cover back"></div>', 'nohead backcover', anchor='backcover'))
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
def cover_html(bk):
    b = bk.data['book']
    return f'''<div class="cv"><div class="cv-series">{E(b["series"])}　{b["vol"]}</div>
<div class="cv-title">{E(b["title"])}</div><div class="cv-sub">完全解説book</div>
<div class="cv-pub">{E(b["publisher"])}</div></div>'''


COVER_CSS = '''
.cv { position: absolute; inset: 0; padding: 30mm 20mm; }
.cv-series { font: 700 11pt/1 "Goth"; letter-spacing: .15em; border-bottom: .75pt solid #000; padding-bottom: 3mm; }
.cv-title { font: 700 40pt/1.3 "Goth"; margin-top: 30mm; }
.cv-sub { font: 700 14pt/1.4 "Goth"; margin-top: 4mm; }
.cv-pub { position: absolute; bottom: 25mm; left: 20mm; font: 10pt/1 "Goth"; }
'''


def legend_html(bk, part):
    return f'''<div class="fm-title">本書の使い方</div>
<div class="lg">
<p>本書は「{E(bk.data["book"]["title"])}」の4冊組のうちの{E(part)}です。</p>
<table class="t lgt"><tbody>
<tr><th>完全解説book</th><td>なぜそうなるかから説明した本体。例文・確認問題つき。</td></tr>
<tr><th>要点まとめbook</th><td>持ち歩き用の A5 判。赤字を赤シートで隠して思い出す。</td></tr>
<tr><th>問題集</th><td>書き込み式。節末問題・章末問題・模擬試験。</td></tr>
<tr><th>解答解説</th><td>全問に正解・根拠・よくある間違い・完全解説book のページ。</td></tr>
</tbody></table>
<div class="lgh">記号</div>
<table class="t lgt"><tbody>
<tr><th>［　］</th><td>関係詞節の範囲</td></tr>
<tr><th><span class="rp">who</span></th><td>関係詞（太字と下線）</td></tr>
<tr><th><span class="gap"></span></th><td>関係詞節の中で欠けている位置</td></tr>
<tr><th>→ p.16</th><td>本書の16ページを参照</td></tr>
<tr><th><span class="ans">赤字</span></th><td>赤シートで隠して答える部分。赤はこの用途にだけ使う</td></tr>
<tr><th>★／★★／★★★</th><td>共通テスト水準／GMARCH 標準／入試より難しい発展</td></tr>
<tr><th>□□□</th><td>解いた記録。1回目・1週間後・1か月後に1つずつ印を付ける</td></tr>
</tbody></table>
<div class="lgh">進め方</div>
<p>1節ずつ、完全解説book を読む → 節の最後の「確認」を赤シートで隠して答える → 問題集の節末問題を解く → 解答解説で答え合わせ、の順に進めます。間違えた問題は1週間後と1か月後にもう一度解き、□に印を付けます。時間をあけて思い出すほうが、続けて読み返すより長く覚えていられることが、実験で確かめられています。</p>
</div>'''


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


def build_all(bk):
    import subprocess
    part = '完全解説book'
    css = KAISETSU_CSS + COVER_CSS + LEGEND_CSS
    lay = bk.render('kaisetsu', f'{bk.data["book"]["title"]} 完全解説book', css, json.dumps(A4),
                    lambda pages: kaisetsu_blocks(bk, pages, cover_html(bk), colophon_html(bk, part), legend_html(bk, part)))
    bk.pages = lay['anchors']
    (bk.out / 'pages_kaisetsu.json').write_text(json.dumps(lay['anchors'], ensure_ascii=False, indent=1))
    print(f'完全解説book: {lay["pages"]} ページ')
