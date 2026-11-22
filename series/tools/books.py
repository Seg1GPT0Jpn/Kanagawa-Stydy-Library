"""4冊の組み方。build.py から呼ばれる。"""
import html, json, re
from build import STAR, CIRC

A4 = dict(pw=210, ph=297, top=22, bottom=25, inner=15, outer=15, mainW=134, gap=6, sideW=40, startPage=1)
A4_1COL = dict(A4, mainW=180, gap=0, sideW=0)
A5 = dict(pw=148, ph=210, top=18, bottom=22, inner=18, outer=19, mainW=111, gap=0, sideW=0, startPage=1)

E = html.escape


CHAPTER_WORD = {'g1': '単元'}   # 英文法編は「単元1」、ほかの本は「第1章」


def CHL(ch):
    """章の呼び方。英文法編（ID が c01 の形）は「単元1」、ほかは「第1章」"""
    return f'単元{ch["no"]}' if re.fullmatch(r'c\d{2}', str(ch.get('id', ''))) else f'第{ch["no"]}章'


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
.blk.h2 { display: flex; align-items: center; gap: 3mm; margin-top: 8mm; padding: 1.6mm 2mm; background: var(--net); border-top: .75pt solid #000; border-bottom: 1.2pt solid #000; font: 700 14pt/1.35 "Goth"; }
.h2 .sno { flex: none; min-width: 9mm; text-align: center; background: #fff; border: .75pt solid #000; font: 700 13pt/1.3 "Goth"; padding: 0 1.5mm; }
.blk.aim { font-size: 9pt; line-height: 1.6; margin: 1.5mm 0 3mm; padding-left: 13mm; text-indent: -13mm; }
.aim .al { display: inline-block; width: 11mm; margin-right: 2mm; text-indent: 0; text-align: center; font: 700 8pt/1.5 "Goth"; border: .5pt solid #000; }
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
.ex .e { font-family: "Ser", "Min"; font-size: 10.5pt; line-height: 1.55; }
.ex .j { font: 9pt/1.6 "Min"; }
.blk.steps { margin: .5mm 0 1.5mm; }
.blk.pt { border: 2.4pt double #000; padding: 2mm 3mm 1mm; margin: 2.5mm 0 3mm; }
.pt .ptl { font: 700 9.5pt/1.6 "Goth"; margin-bottom: 1mm; }
.pt table.t { margin: 0 0 1.5mm; }
.steps div { padding-left: 3.6em; text-indent: -3.6em; }
.steps b { font: 700 9.5pt "Goth"; margin-right: .6em; }
table.t { border-collapse: collapse; width: 100%; margin: 1.5mm 0 3mm; font-size: 9.5pt; line-height: 1.5; }
table.t th, table.t td { border: .5pt solid #000; padding: 1.2mm 2mm; text-align: center; }
table.t thead th { background: var(--net); font: 700 9pt/1.4 "Goth"; }
table.t tbody th { font: 700 9pt/1.4 "Goth"; text-align: left; background: var(--net); }
table.t tbody th.nwc { white-space: nowrap; }
table.t td.nwc, table.t th.nwc { white-space: nowrap; }
table.t td { font-family: "Ser", "Min"; font-size: 10pt; }
.blk.check { border: .75pt solid #000; padding: 2mm 3mm; margin: 3mm 0 2mm; }
.check .t { font: 700 9pt/1.6 "Goth"; }
.check .r { display: grid; grid-template-columns: 7mm 1fr 32mm; align-items: baseline; }
.check .q { font-family: "Ser", "Min"; }
.check .a { font-family: "Ser", "Min"; text-align: center; border-bottom: .35pt solid #000; }
.check .r.long { grid-template-columns: 7mm 1fr; }
.check .r.long .a { grid-column: 2; text-align: left; padding-left: 2mm; }
.sn { font: 8pt/1.6 "Goth"; padding: 1.2mm 0 3mm; border-top: .35pt solid #000; }
.sn .lab { font-weight: 700; display: block; }
.sn .en { font-family: "Ser", "Min"; font-size: 8.5pt; }
.sn .gl { padding-left: 1em; }
/* 前付・後付 */
.page > .blk.fullpage { position: absolute; inset: 0; }
.fm-title { font: 700 16pt/1.4 "Goth"; padding-bottom: 2mm; border-bottom: 1.2pt solid #000; margin-bottom: 5mm; }
.toc .tc { display: flex; font: 700 10.5pt/1.5 "Goth"; margin-top: 4mm; }
.toc .ts { display: flex; font-size: 10pt; line-height: 1.9; padding-left: 2em; }
.toc .dots { flex: 1; border-bottom: .35pt dotted #000; margin: 0 2mm .45em; }
.toc .pg { font-family: "Ser", "Min"; min-width: 6mm; text-align: right; }
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
        toc.append(f'<div class="tc">{CHL(ch)}　{E(ch["title"])}<span class="dots"></span><span class="pg">{pages.get(ch["id"], "00")}</span></div>')
        for s in ch['sections']:
            toc.append(f'<div class="ts">{s["no"]}　{E(s["title"])}<span class="dots"></span><span class="pg">{pages.get(s["id"], "00")}</span></div>')
    toc.append(f'<div class="tc">索引<span class="dots"></span><span class="pg">{pages.get("index", "00")}</span></div></div>')
    out.append(blk(''.join(toc), 'newpage', anchor='toc', chapter='目次', section='目次'))
    for ch in d['chapters']:
        chap_label = f'{CHL(ch)}　{ch["title"]}'
        lead = f'<div class="lead">{bk.md(ch["lead"], pages)}</div>' if ch.get('lead') else ''
        out.append(blk(f'<div class="cno">{CHL(ch)}</div><div class="ct">{E(ch["title"])}</div>{lead}', 'chap newpage keepnext', anchor=ch['id'], chapter=chap_label, section=chap_label))
        for s in ch['sections']:
            out.append(blk(f'<span class="sno">{s["no"]}</span><span class="stt">{E(s["title"])}</span>', 'h2 keepnext', anchor=s['id'], section=f'{s["no"]}　{s["title"]}'))
            aim = s.get('aim') or bk.data.get('aims', {}).get(s['id'])
            if aim:
                out.append(blk(f'<span class="al">ねらい</span>{bk.md(aim, pages)}', 'aim keepnext'))
            exmap = {e['id']: e for e in s.get('examples', [])}
            hno = 0
            for b in s['body']:
                notes = ''.join(note_html(bk, n, pages) for n in (b.get('notes') or []))
                if 'h' in b:
                    hno += 1
                    out.append(blk(f'({hno}) {bk.md(b["h"], pages)}', 'h3 keepnext'))
                elif 'p' in b:
                    out.append(blk(f'<p>{bk.md(b["p"], pages)}</p>', 'p', notes))
                elif 'ex' in b:
                    ids = b['ex']
                    allgl = [g for eid in ids for g in (exmap[eid].get('gloss') or [])]
                    for i, eid in enumerate(ids):
                        e = exmap[eid]
                        # 語注は例文のまとまりごとに1つにまとめ、最初の例文の横に置く
                        gl = note_html(bk, {'kind': '語注', 'items': allgl}, pages) if (i == 0 and allgl) else ''
                        cls = 'ex' + (' top' if i == 0 else '') + (' last' if i == len(ids) - 1 else '')
                        nt = notes if i == 0 else ''
                        out.append(blk(f'<span class="n">{bk.ex_no[eid]}</span><div><div class="e">{bk.md(e["en"], pages)}</div><div class="j">{bk.md(e["ja"], pages)}</div></div>', cls, nt + gl, anchor=eid))
                elif 'steps' in b:
                    lab = b.get('label', '手順')
                    rows = ''.join(f'<div><b>{lab}{i}</b>{bk.md(t, pages)}</div>' for i, t in enumerate(b['steps'], 1))
                    out.append(blk(f'<div class="ptl">● 要点</div>{rows}', 'steps pt', notes))
                elif 'table' in b:
                    t = b['table']
                    th = ''.join(f'<th{" class=nwc" if len(str(c)) <= 8 else ""}>{bk.md(c, pages)}</th>' for c in t['head'])
                    def td(c):
                        if '<br>' in str(c):
                            # 改行位置を指定したマスは、区切った1かたまりごとに改行しない（列の最小幅がそのかたまりの幅になる）
                            segs = str(c).split('<br>')
                            return '<td>' + '<br>'.join(f'<span class="nw">{bk.md(sg, pages)}</span>' for sg in segs) + '</td>'
                        plain = re.sub(r'\{\{|\}\}|<<|>>|\*', '', str(c))
                        ascii_ratio = sum(ch.isascii() for ch in plain) / max(1, len(plain))
                        short = len(plain) <= 12 or (ascii_ratio > 0.8 and len(plain) <= 20)  # 短いマスと英語の句は改行しない
                        return f'<td class="nwc">{bk.md(c, pages)}</td>' if short else f'<td>{bk.md(c, pages)}</td>'
                    tr = ''.join(f'<tr><th{" class=nwc" if len(str(r[0])) <= 10 else ""}>' + bk.md(r[0], pages) + '</th>' + ''.join(td(c) for c in r[1:]) + '</tr>' for r in t['rows'])  # 行の見出しも短いときだけ改行しない
                    cap = f'<div class="ptl">● {E(t["title"])}</div>' if t.get('title') else '<div class="ptl">● 要点</div>'
                    out.append(blk(f'{cap}<table class="t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>', 'tbl pt', notes))
                elif 'check' in b:
                    anylong = any(len(str(c["a"])) > 12 for c in b['check'])  # 囲みの中で答えの位置をそろえる
                    rows = ''.join(f'<div class="r{" long" if anylong else ""}"><span>({i})</span><span class="q">{bk.md(c["q"], pages)}</span><span class="a ans">{bk.md(c["a"], pages)}</span></div>' for i, c in enumerate(b['check'], 1))
                    qs = ' '.join(str(c['q']) for c in b['check'])
                    blank = '（　）' if re.search(r'[(（]\s*＿', qs) and '［' not in qs else '［　］'   # 問いの空所の形に合わせる
                    out.append(blk(f'<div class="t">確認　{E(b.get("inst", blank + "に入る語を答えなさい。答えは赤シートで隠して確かめる。"))}</div>{rows}', 'check', notes))
                else:
                    raise SystemExit(f'未知の本文ブロック: {b}')
    # 索引
    terms = sorted(bk.terms.items(), key=lambda kv: kv[1])
    rows = []; cur = None
    for t, yomi in terms:
        g = gojuon_row(yomi)
        if g != cur:
            rows.append(f'<div class="k">{g}</div>'); cur = g
        rows.append(f'<div class="row">{E(t)}<span class="dots"></span><span class="pg">{pages.get("term:" + t.replace(" ", "\u00a0"), "00")}</span></div>')
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
    from cover import relclause_svg, EG01, pattern_svg, G1
    b = bk.data['book']
    fig = pattern_svg(**G1) if b['id'] == 'g1' else relclause_svg(**EG01)
    note = ('英文は、文の要素 S・V・O・C の並びで意味が決まる。<br>中学の文法から、大学入学共通テスト・GMARCH 個別試験の水準まで。' if b['id'] == 'g1'
            else '関係詞節は、欠けた語の代わりに先行詞を後ろから説明する。<br>大学入学共通テスト・GMARCH 個別試験の水準まで。')
    return f'''<div class="cv"><div class="cv-series"><span>{E(b["series"])}</span><span>{E(b["vol"])}</span></div>
<div class="cv-title"><span class="cv-vol">{E(b["vol"])}</span>【{E(b["title"])}】</div><div class="cv-sub">{E(part)}</div>
<div class="cv-fig">{fig}</div>
<div class="cv-note">{note}</div>
<div class="cv-pub">{E(b["publisher"])}</div></div>'''


def back_html(bk, part):
    b = bk.data['book']
    return f'''<div class="cv"><div class="cv-back">{E(b["series"])}　{E(b["vol"])}【{E(b["title"])}】<br>
{'本冊 上巻・下巻（解説・例題・問題・要点・確認テスト・総合演習）と別冊（解答解説）の3冊組' if b.get('volumes') else '本冊（解説・例題・問題・要点・章末問題・模擬試験）と別冊（解答解説）の2冊組'}<br>{E(part)}<br><br>
本書は無料の教材です。{E(b["license"])} のもとで、出典を表示すれば自由に複製・配布・改変できます。<br>
人間の専門家による確認を受ける前の版です。使う前に奥付の「ご利用の前に」をお読みください。</div>
<div class="cv-pub">{E(b["publisher"])}</div></div>'''


COVER_CSS = '''
.cv { position: absolute; inset: 0; }
.cv-series { position: absolute; left: 20mm; right: 20mm; top: 24mm; border-bottom: .75pt solid #000; padding-bottom: 3mm; display: flex; justify-content: space-between; font: 700 10pt/1 "Goth"; letter-spacing: .2em; }
.cv-title { position: absolute; left: 20mm; top: 46mm; font: 700 36pt/1.25 "Goth"; }
.cv-vol { margin-right: .2em; }
.cv-sub { position: absolute; left: 20mm; top: 72mm; font: 700 15pt/1.4 "Goth"; }
.cv-fig { position: absolute; left: 20mm; right: 20mm; top: 110mm; height: 84mm; background: var(--net); display: flex; align-items: center; justify-content: center; }
.cv-note { position: absolute; left: 20mm; top: 202mm; font: 9.5pt/1.6 "Goth"; }
.cv-pub { position: absolute; left: 20mm; right: 20mm; bottom: 22mm; border-top: .35pt solid #000; padding-top: 3mm; font: 9.5pt/1.6 "Goth"; }
.cv-back { position: absolute; left: 20mm; right: 20mm; top: 200mm; font: 9pt/1.8 "Goth"; }
'''



SYM_EG01 = """<tr><th>［　］</th><td>関係詞節の範囲</td></tr>
<tr><th><span class="rp">who</span></th><td>関係詞（太字と下線）</td></tr>
<tr><th><span class="gap"></span></th><td>関係詞節の中で欠けている位置</td></tr>"""
SYM_G1 = """<tr><th>S V O C M</th><td>文の要素（主語・動詞・目的語・補語・修飾語）。2つの O は O<span class="subn">1</span>（人）・O<span class="subn">2</span>（物）</td></tr>
<tr><th>［　］</th><td>節（S＋V をふくむかたまり）の範囲。名詞節・形容詞節・副詞節のすべてに使う</td></tr>
<tr><th>（　）</th><td>修飾語句 M（前置詞句・副詞）</td></tr>
<tr><th>〈　〉</th><td>準動詞のかたまり（不定詞・動名詞・分詞の句）</td></tr>
<tr><th><span class="gap"></span></th><td>欠けている位置（不完全な文）</td></tr>
<tr><th><span class="rp">that</span></th><td>その単元で注目する語（太字と下線）</td></tr>
<tr><th>do／to do／doing／done</th><td>原形・不定詞・-ing 形・過去分詞。have done は完了形。語法は allow O to do の形で書く</td></tr>"""


def legend_html(bk, part):
    g1 = bk.data['book']['id'] == 'g1'
    return f'''<div class="fm-title">本書の使い方</div>

<p>本書は「{E(bk.data["book"]["series"])}　{E(bk.data["book"]["vol"])}【{E(bk.data["book"]["title"])}】」の{E(part)}です。本冊と別冊は同じ1つのデータから作っているので、問題番号やページの参照は2冊の間で一致します。</p>
<table class="t lgt"><tbody>
<tr><th>本冊</th><td>{'単元の入口で中学の復習と前提チェックをしてから、各節を「解説 → 例題 → 問題 → 要点」の順に学ぶ。単元の終わりに確認テスト（前の単元の問題も混ざる）、本の終わりに単元を混ぜた総合演習。上巻・下巻のページ番号は通し。' if g1 else '各節を「解説 → 例題 → 問題 → 要点」の順に学ぶ。章の終わりに章末問題、本の終わりに模擬試験と解答用紙。'}</td></tr>
<tr><th>別冊　解答解説</th><td>全問に正解・根拠・よくある間違い・本冊の戻り先のページ。</td></tr>
</tbody></table>
<!--split--><div class="lgh">記号</div>
<table class="t lgt"><tbody>
{SYM_G1 if g1 else SYM_EG01}
<tr><th>→ p.16</th><td>本書の16ページを参照</td></tr>
<tr><th><span class="ans">赤字</span></th><td>赤シートで隠して答える部分。赤はこの用途にだけ使う</td></tr>
<tr><th>①②③④（下線）</th><td>正誤問題の下線部の番号。下線部のすぐ後ろに付け、文の前から順に①②③④とする</td></tr>
{'<tr><th>★／★★</th><td>共通テスト水準／GMARCH 標準（入試より難しい発展は、後の講「入試演習編」で扱う）</td></tr>' if g1 else '<tr><th>★／★★／★★★</th><td>共通テスト水準／GMARCH 標準／入試より難しい発展</td></tr>'}
<tr><th>□□□</th><td>解いた記録。1回目・1週間後・1か月後に1つずつ印を付ける</td></tr>
</tbody></table>
<!--split--><div class="lgh">進め方</div>
<p>1節ずつ、次の順に進めます。①解説を読み、例文を声に出して読む。②節の中の「確認」を赤シートで隠して答える。③例題の「解き方」を読み、同じ手順で考えられるようにする。④問題を解き、別冊で答え合わせをする。間違えた問題は、別冊に書いた戻り先のページを読み直す。⑤要点を赤シートで隠して言えるか確かめる。</p>
<p>間違えた問題は1週間後と1か月後にもう一度解き、□に印を付けます。時間をあけて思い出すほうが、続けて読み返すより長く覚えていられることが、実験で確かめられています。{'単元の終わりの確認テストには、前の単元の問題も2問混ぜています。時間をあけて思い出す練習です。間違えた問題は、別冊の診断表で読み直す節を確かめます。' if g1 else '章の終わりの章末問題は、いくつかの節を混ぜて出しています。どの節の考え方を使うかを自分で見分ける練習です。'}</p>
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
<div class="bt">{E(b["series"])}　{E(b["vol"])}【{E(b["title"])}】　{E(part)}</div>
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
.box3 { display: inline-block; vertical-align: -.4mm; }
.qt { font-family: "Ser", "Min"; font-size: 10.5pt; line-height: 1.7; }
.qt .ja { font-family: "Min"; font-size: 10pt; }
.psg { font-family: "Ser", "Min"; font-size: 10pt; line-height: 1.65; text-align: justify; margin: 1mm 0 2mm; padding: 2mm 3mm; border: .5pt solid #000; }
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
.blk.lvh { font: 700 10pt/1.5 "Goth"; margin: 4mm 0 0; padding-bottom: .8mm; border-bottom: .75pt solid #000; }
.lvh .lvs { font-weight: 400; font-size: 9pt; }
.blk.inst { padding-left: 2mm; }
/* 模試 */
.blk.parth { font: 700 11pt/1.5 "Goth"; margin: 5mm 0 0; padding: 1mm 0; border-bottom: .75pt solid #000; }
.parth .pp { font: 400 9pt "Goth"; }
.sheet-h { font: 10pt/2 "Goth"; margin-bottom: 4mm; }
.sheet-h .u { display: inline-block; width: 60mm; border-bottom: .5pt solid #000; }
.sheet-h .u.s { width: 20mm; }
table.sheet { width: 100%; border-collapse: collapse; margin-bottom: 0; }
table.sheet th { background: var(--net); font: 700 9pt/1.6 "Goth"; border: .5pt solid #000; }
table.sheet td { border: .5pt solid #000; padding: 1.5mm 2mm; height: 12mm; }
table.sheet td.sl { width: 24mm; font: 700 9.5pt "Goth"; white-space: nowrap; }
table.sheet td.pt { width: 14mm; text-align: center; font: 9pt "Goth"; }
.sl-box { width: 14mm; height: 8mm; border: .75pt solid #000; }
.sl-line { height: 8mm; border-bottom: .5pt solid #000; }
table.sheet tr.w td { height: 18mm; }
table.sheet tr.ww td { height: 34mm; }
.sl-fix { font: 7.5pt "Goth"; margin-top: 1mm; }
/* 診断表 */
.blk.diag { margin: 5mm 0 3mm; border: 2.4pt double #000; padding: 2.5mm 3mm; }
.dgt { font: 700 11pt/1.5 "Goth"; }
.dgs { font-size: 9pt; line-height: 1.6; margin: 1mm 0 2mm; }
table.dg td { text-align: left; font-size: 9pt; }
table.dg td.cb { width: 10mm; text-align: center; }
.ck { display: inline-block; width: 4mm; height: 4mm; border: .5pt solid #000; vertical-align: middle; }
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


LVNAME = {1: '基本', 2: '標準', 3: '発展'}


def prob_header(bk, title, probs, ref_html=''):
    lvs = sorted({p['lv'] for p in probs})
    star = STAR[lvs[0]] + ('〜' + STAR[lvs[-1]] if len(lvs) > 1 else '')
    mins = sum(p['min'] for p in probs)
    return f'<span class="tt">{title}</span><span class="meta">{star}　{len(probs)}問　目安 {mins}分{"<br>" + ref_html if ref_html else ""}</span>'


def q_body(bk, p, pages):
    pts = f'<span>（{p["pts"]}点）</span>' if p.get('pts') else ''
    s = f'<div class="qh"><span class="no">{p["label"]}</span><span>{STAR[p["lv"]]}</span><svg class="box3" viewBox="0 0 39 11" width="11.7mm" height="3.3mm"><rect x="0.5" y="0.5" width="10" height="10" fill="none" stroke="#000" stroke-width="0.9"/><rect x="14.5" y="0.5" width="10" height="10" fill="none" stroke="#000" stroke-width="0.9"/><rect x="28.5" y="0.5" width="10" height="10" fill="none" stroke="#000" stroke-width="0.9"/></svg>{pts}</div>'
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


def problem_blocks(bk, pages, probs, wide=False):
    """問題を指示文つきで並べる。wide=True なら側注欄まで使う全幅で組む（本体の問題）。"""
    out = []
    W = ' wide' if wide else ''
    last_inst = None
    for p in probs:
        inst = p.get('inst_eff')
        if inst and inst != last_inst:
            out.append(blk(bk.md(inst, pages), 'inst keepnext' + W))
        last_inst = inst
        body = q_body(bk, p, pages)
        if p['kind'] == '正誤' and '直しなさい' in (p.get('inst_eff') or ''):
            out.append(blk(f'<div class="q">{body}</div><div class="acol"><span class="alab">記号</span><div class="abox"></div></div><div class="wl"><span class="alab">正しい形</span><div class="aline"></div><div class="aline"></div></div>', 'qr w' + W, anchor='q' + str(p['no'])))
        elif p['kind'] in ('4択', '正誤') or (p['kind'] == '読解' and p.get('choices')):
            out.append(blk(f'<div class="q">{body}</div><div class="acol"><span class="alab">解答</span><div class="abox"></div></div>', 'qr' + W, anchor='q' + str(p['no'])))
        else:
            n = {'整序': 1, '補充': 1, '和訳': 2, '英作': 2, '読解': 2}[p['kind']]
            if p['kind'] == '補充':
                n = max(1, len(re.findall(r'\(＿\)|\[＿\]', str(p['q']))))  # 空所の数だけ線を引く
            out.append(blk(f'<div class="q">{body}</div><div></div><div class="wl"><span class="alab">解答</span>' + '<div class="aline"></div>' * (n + 1) + '</div>', 'qr w' + W, anchor='q' + str(p['no'])))
    return out


def mondai_blocks(bk, pages, part, cover, colophon, legend):
    kp = bk.pages  # 完全解説book のページ
    out = [fullpage(cover, 'nohead pk-cover', anchor='cover'), fullpage('', 'nohead pk-blank')]
    out.extend(legend_blocks(legend))
    toc = ['<div class="fm-title">目次</div><div class="toc">']
    for ch in bk.data['chapters']:
        toc.append(f'<div class="tc">{CHL(ch)}　{E(ch["title"])}<span class="dots"></span><span class="pg">{pages.get(ch["id"], "00")}</span></div>')
        for s in ch['sections']:
            toc.append(f'<div class="ts">{s["no"]}　{E(s["title"])}<span class="dots"></span><span class="pg">{pages.get("m" + s["id"], "00")}</span></div>')
        toc.append(f'<div class="ts">章末問題<span class="dots"></span><span class="pg">{pages.get("end" + ch["id"], "00")}</span></div>')
    if any(p['set'] == '模試' for p in bk.problems):
        toc.append(f'<div class="tc">模擬試験<span class="dots"></span><span class="pg">{pages.get("mock", "00")}</span></div>')
    toc.append('</div>')
    out.append(blk(''.join(toc), 'newpage', anchor='toc', chapter='目次', section='目次'))

    for ch in bk.data['chapters']:
        chap_label = f'{CHL(ch)}　{ch["title"]}'
        out.append(blk(f'<div class="cno">{CHL(ch)}</div><div class="ct">{E(ch["title"])}</div>', 'chap newpage keepnext', anchor=ch['id'], chapter=chap_label, section=chap_label))
        for s in ch['sections']:
            probs = [p for p in bk.problems if p['sec'] == s['id'] and p['set'] == '節末']
            if not probs: continue
            ref = f'解説 → 完全解説book p.{kp.get(s["id"], "00")}'
            out.append(blk(prob_header(bk, f'{s["no"]}　{E(s["title"])}', probs, ref), 'sech keepnext', anchor='m' + s['id'], section=f'{s["no"]}　{s["title"]}'))
            for lv in (1, 2, 3):
                ps = [p for p in probs if p['lv'] == lv]
                if not ps: continue
                out.append(blk(f'◆ {LVNAME[lv]}　<span class="lvs">{STAR[lv]}</span>', 'lvh keepnext'))
                out.extend(problem_blocks(bk, pages, ps))
        probs = [p for p in bk.problems if p['set'] == '章末' and p['home'] == ch['id']]
        if probs:
            out.append(blk(prob_header(bk, f'{CHL(ch)}　章末問題', probs, '節を混ぜて出題'), 'sech keepnext newpage', anchor='end' + ch['id'], section=f'{CHL(ch)}　章末問題'))
            out.extend(problem_blocks(bk, pages, probs))
    out.extend(mock_blocks(bk, pages))
    pad_and_colophon(out, pages, colophon)
    return out


_back = ''


def mock_blocks(bk, pages, wide=False):
    out = []
    mock = [p for p in bk.problems if p['set'] == '模試']
    if mock:
        tot = sum(p.get('pts', 0) for p in mock)
        out.append(blk(prob_header(bk, '模擬試験', mock, f'解答時間 45分　{tot}点満点'), 'sech keepnext newpage', anchor='mock', chapter='模擬試験', section='模擬試験'))
        parts = sorted({p['part'] for p in mock})
        for pt in parts:
            ps = [p for p in mock if p['part'] == pt]
            out.append(blk(f'第{pt}問　<span class="pp">（配点 {sum(p.get("pts", 0) for p in ps)}点）</span>', 'parth keepnext'))
            out.extend(problem_blocks(bk, pages, ps, wide))
        # 解答用紙
        rows = []
        for pt in parts:
            for p in [p for p in mock if p['part'] == pt]:
                fixq = p['kind'] == '正誤' and '直しなさい' in (p.get('inst_eff') or '')
                wide = fixq or (p['kind'] not in ('4択', '正誤', '読解') or (p['kind'] == '読解' and not p.get('choices')))
                cell = '<div class="sl-box"></div><div class="sl-fix">正しい形</div><div class="sl-line"></div>' if fixq else ('<div class="sl-line"></div>' if wide else '<div class="sl-box"></div>')
                cls = 'ww' if p['kind'] in ('和訳', '英作') else ('w' if wide else '')
                rows.append(f'<tr class="{cls}"><td class="sl">{p["label"]}</td><td>{cell}</td><td class="pt">{p.get("pts", "")}</td></tr>')
        out.append(blk('<div class="fm-title">模擬試験　解答用紙</div><div class="sheet-h">名前 <span class="u"></span>　　得点 <span class="u s"></span> ／ ' + str(tot) + '</div>', 'newpage', anchor='sheet', section='模擬試験　解答用紙'))
        for i in range(0, len(rows), 10):
            out.append(blk('<table class="sheet"><thead><tr><th>番号</th><th>解答</th><th>配点</th></tr></thead><tbody>' + ''.join(rows[i:i + 10]) + '</tbody></table>', 'sheetblk'))
    return out


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


def diagnosis_blocks(bk, ch, kp, st='章末'):
    """章末問題・確認テストの診断表：間違えた問題から、読み直す節と本冊のページが分かる。"""
    ps = [p for p in bk.problems if p['set'] == st and p['home'] == ch['id']]
    rows = ''
    for p in ps:
        refs = p.get('ref') or p['sec']
        refs = refs if isinstance(refs, list) else [refs]
        secs = '<br>'.join(f'{bk.sec_no[r]}　{E(bk.sec_title[r])}' for r in refs)
        pgs = '<br>'.join(f'p.{kp.get(r, "00")}' for r in refs)
        wkc = '<br>'.join(('例題' + '・'.join(map(str, bk.wk_nos.get(r, [])))) if bk.wk_nos.get(r) else '' for r in refs)
        rows += (f'<tr><td class="nwc">{p["label"]}</td><td class="cb"><span class="ck"></span></td><td>{secs}</td>'
                 f'<td class="nwc">{pgs}</td><td class="nwc">{wkc}</td></tr>')
    head = '<tr><th>問題</th><th>×</th><th>読み直す節</th><th>本冊</th><th>例題</th></tr>'
    return [blk(f'<div class="dgt">{CHL(ch)}　{st}の診断表</div><div class="dgs">間違えた問題の「×」の欄に印を付け、その節の解説と例題を読み直してから、本冊の節の問題をもう一度解きます。</div>'
                f'<table class="t dg"><thead>{head}</thead><tbody>{rows}</tbody></table>', 'diag')]


def kaitou_blocks(bk, pages, part, cover, colophon, legend):
    kp = bk.pages
    out = [fullpage(cover, 'nohead pk-cover', anchor='cover'), fullpage('', 'nohead pk-blank')]
    out.extend(legend_blocks(legend))
    cur_ch = None
    for p in bk.problems:
        ch = next(c for c in bk.data['chapters'] if c['id'] == p['home'])
        if p['set'] == '総合演習':
            if cur_ch != ('sougou', p['part']):
                out.append(blk(f'<span class="tt">総合演習　第{p["part"]}回　解答解説</span>', 'sech keepnext newpage', anchor=f'sougou{p["part"]}', chapter='総合演習', section='総合演習'))
                cur_ch = ('sougou', p['part'])
        elif p['set'] == '模試':
            if cur_ch != 'mock':
                out.append(blk('<span class="tt">模擬試験　解答解説</span>', 'sech keepnext newpage', anchor='mock', chapter='模擬試験', section='模擬試験'))
                cur_ch = 'mock'
        elif ch is not cur_ch:
            out.append(blk(f'<span class="tt">{CHL(ch)}　{E(ch["title"])}</span>', 'sech keepnext' + (' newpage' if cur_ch else ''), anchor=ch['id'],
                           chapter=f'{CHL(ch)}　{ch["title"]}', section=f'{CHL(ch)}　{ch["title"]}'))
            cur_ch = ch
        alt = ''
        if p.get('alt'):
            alt = '<dt>別解</dt><dd>' + '／'.join(bk.md(a, pages) for a in p['alt']) + '</dd>'
        refs = p.get('ref') or p['sec']
        refs = refs if isinstance(refs, list) else [refs]   # 2つの節にまたがる問題は戻り先を複数示す
        items = []
        for ref in refs:
            wks = bk.wk_nos.get(ref, [])
            wk = ''
            if wks:
                wk = '<br>例題' + '・'.join(str(n) for n in wks) + f' <span class="pref">→&nbsp;p.{kp.get(f"w{wks[0]}", "00")}</span>'
            items.append(f'本冊 {bk.sec_no[ref]}　{E(bk.sec_title[ref])}<br>解説 <span class="pref">→&nbsp;p.{kp.get(ref, "00")}</span>{wk}')
        side = '<div class="sn"><span class="lab">間違えたら戻る</span>' + '<br>'.join(items) + '</div>'
        label = p['label']
        out.append(blk(f'''<div class="hd"><span class="no">{label}</span><span>{STAR[p["lv"]]}</span><span>{E(p["kind"])}</span></div>
<div><span class="ans-l">正解　</span><span class="ans-v ans">{ans_text(bk, p, pages)}</span></div>
<dl>{alt}<dt>根拠</dt><dd>{bk.md(p["why"], pages)}</dd><dt>よくある間違い</dt><dd>{bk.md(p["trap"], pages)}</dd></dl>''', 'ka', side, anchor='q' + str(p['no'])))
        # 章末問題の最後に診断表
        nxt = bk.problems[bk.problems.index(p) + 1] if bk.problems.index(p) + 1 < len(bk.problems) else None
        for st in ('章末', '確認テスト'):
            if p['set'] == st and (nxt is None or nxt['set'] != st or nxt['home'] != p['home']):
                out.extend(diagnosis_blocks(bk, ch, kp, st))
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
        out.append(blk(f'<div class="cno">{CHL(ch)}</div><div class="ct">{E(ch["title"])}</div>', 'chap newpage keepnext', anchor=ch['id'], chapter=f'{CHL(ch)}　{ch["title"]}', section=f'{CHL(ch)}　{ch["title"]}'))
        for s in ch['sections']:
            if not s.get('summary'): continue
            out.append(blk(f'<span class="tt">{s["no"]}　{E(s["title"])}</span><span class="meta">→ 完全解説book p.{kp.get(s["id"], "00")}</span>', 'sech keepnext', anchor=s['id'], section=f'{s["no"]}　{s["title"]}'))
            for i, t in enumerate(s['summary'], 1):
                out.append(blk(f'<span class="n">{i}</span><div>{bk.md(t, pages)}</div>', 'sm'))
    pad_and_colophon(out, pages, colophon)
    return out


# ====================================================================
# 本体（1冊）：各節＝解説 → 例題 → 問題 → 要点。章末問題、模擬試験、索引
# ====================================================================
WORKED_STYLE = 'band'   # 試作：'box'（囲み）か 'band'（帯の見出し）

WORKED_CSS = '''
.blk.wk { margin: 3mm 0 2mm; }
.wk.box { border: .75pt solid #000; padding: 2mm 3mm 2mm; }
.wk.band { border-top: 1.2pt solid #000; padding: 1.5mm 0 1mm; }
.wk .wh { display: flex; gap: 3mm; align-items: baseline; font: 700 10pt/1.5 "Goth"; }
.wk.band .wh { background: var(--net); padding: .8mm 2mm; margin-bottom: 1mm; }
.wk .wq { font-family: "Ser", "Min"; font-size: 10.5pt; line-height: 1.7; margin: 1mm 0 .5mm; }
.wk .ch { margin-bottom: 1.5mm; }
.wk .how { font-size: 9.5pt; line-height: 1.7; }
.wk .how .hl { font: 700 8.5pt/1.7 "Goth"; display: inline-block; border: .5pt solid #000; padding: 0 1.5mm; margin-bottom: .5mm; }
.wk .how ol { list-style: none; }
.wk .how li { padding-left: 1.6em; text-indent: -1.6em; }
.wk .how li .sn2 { font: 700 9pt "Goth"; margin-right: .4em; }
.wk .wa { margin-top: 1mm; font: 700 9.5pt/1.7 "Goth"; }
.wk .wa .ans { font-family: "Ser", "Min"; font-weight: 600; }
.wk .wp { margin-top: .8mm; font-size: 9pt; line-height: 1.65; border-top: .35pt dotted #000; padding-top: .8mm; }
.wk .wp b { font: 700 8.5pt "Goth"; margin-right: .5em; }
.blk.phase { margin: 6mm 0 1mm; padding: 1.2mm 2mm; font: 700 11pt/1.4 "Goth"; border-top: 1.2pt solid #000; border-bottom: .5pt solid #000; display: flex; justify-content: space-between; align-items: baseline; }
.phase .meta { font: 400 8.5pt "Goth"; }
.blk.intro { margin: 2mm 0 3mm; padding: 2mm 3mm; border: .75pt solid #000; font-size: 9.5pt; line-height: 1.7; }
.intro .ih { font: 700 9.5pt/1.6 "Goth"; margin-bottom: .5mm; }
.blk.sumh { margin: 5mm 0 0; font: 700 10pt/1.5 "Goth"; border: .75pt solid #000; border-bottom: 0; padding: 1mm 2mm; background: var(--net); }
.blk.sm { display: grid; grid-template-columns: 6mm 1fr; padding: 1mm 2mm; border-left: .75pt solid #000; border-right: .75pt solid #000; border-bottom: .35pt solid #000; line-height: 1.75; font-size: 9.5pt; }
.blk.sm.last { border-bottom: .75pt solid #000; margin-bottom: 2mm; }
.sm .n { font: 8pt/1.9 "Goth"; }
'''


def worked_html(bk, s, k, w, pages, style):
    ch = ''
    if w.get('choices'):
        ch = '<div class="ch">' + ''.join(f'<span><span class="cn">{CIRC[i]}</span>{bk.md(c, pages)}</span>' for i, c in enumerate(w['choices'])) + '</div>'
    steps = ''.join(f'<li><span class="sn2">{CIRC[i]}</span>{bk.md(t, pages)}</li>' for i, t in enumerate(w['steps']))
    a = str(w['ans'])
    ans = f'{CIRC[int(a) - 1]}　{bk.md(w["choices"][int(a) - 1], pages)}' if (w.get('choices') and a.isdigit()) else bk.md(a, pages)
    return (f'<div class="wh"><span>例題{k}</span></div><div class="wq">{bk.md(w["q"], pages)}</div>{ch}'
            f'<div class="how"><span class="hl">解き方</span><ol>{steps}</ol></div>'
            f'<div class="wa">答え　<span class="ans">{ans}</span></div>'
            + (f'<div class="wp"><b>ポイント</b>{bk.md(w["point"], pages)}</div>' if w.get('point') else ''))


def sougou_blocks(bk, pages, parts=None):
    """総合演習（単元を混ぜた問題。part ごとに1回分）。parts を指定すると、その回だけ（第1回は上巻の終わりに置く）"""
    out = []
    ps_all = [p for p in bk.problems if p['set'] == '総合演習']
    for pt in sorted({p['part'] for p in ps_all}):
        if parts is not None and pt not in parts: continue
        ps = [p for p in ps_all if p['part'] == pt]
        out.append(blk(prob_header(bk, f'総合演習　第{pt}回', ps, 'いくつもの単元を混ぜて出題　答え → 別冊'), 'sech keepnext newpage wide', anchor=f'sougou{pt}', chapter='総合演習', section=f'総合演習　第{pt}回'))
        out.extend(problem_blocks(bk, pages, ps, wide=True))
    return out


def index_blocks(bk, pages, chapters, anchor):
    """索引。chapters を指定すると、その章で定義した用語だけ（上巻の索引）"""
    terms = sorted(((t, y) for t, y in bk.terms.items() if chapters is None or bk.term_ch.get(t) in chapters), key=lambda kv: kv[1])
    rows = []; cur = None
    for t, yomi in terms:
        g = gojuon_row(yomi)
        if g != cur:
            rows.append(f'<div class="k">{g}</div>'); cur = g
        rows.append(f'<div class="row">{E(t)}<span class="dots"></span><span class="pg">{pages.get("term:" + t.replace(" ", "\u00a0"), "00")}</span></div>')
    # 1ページに入る行数ごとに分ける（各ページは2段組。見出しの行は高いので少なめに数える）
    PER = 64
    chunks, curc, n = [], [], 0
    for r in rows:
        w = 1.6 if r.startswith('<div class="k">') else 1
        if n + w > PER and curc:
            if curc[-1].startswith('<div class="k">'): last = [curc.pop()]   # 五十音の見出しをページ末に残さない
            else: last = []
            chunks.append(curc); curc, n = last, len(last) * 1.6
        curc.append(r); n += w
    if curc: chunks.append(curc)
    title = ('索引（上巻・下巻）' if bk.data['book'].get('volumes') else '索引') if chapters is None else '索引（上巻）'
    out = []
    for k, c in enumerate(chunks):
        head = f'<div class="fm-title">{title}</div>' if k == 0 else ''
        out.append(blk(head + '<div class="idx toc">' + ''.join(c) + '</div>', 'newpage', anchor=anchor if k == 0 else None, chapter=title, section=title))
    return out


def honbun_blocks(bk, pages, part, cover, colophon, legend):
    d = bk.data
    out = [fullpage(cover, 'nohead pk-cover', anchor='cover'), fullpage('', 'nohead pk-blank')]
    out.extend(legend_blocks(legend))
    # 目次は章ごとのかたまりに分ける（ページをまたげるように）
    tocb = []
    vols = bk.data['book'].get('volumes') or []
    vol1_last = vols[0]['chapters'][-1] if len(vols) > 1 else None
    sougou_parts = sorted({p['part'] for p in bk.problems if p['set'] == '総合演習'})
    for k, ch in enumerate(d['chapters']):
        rows = [f'<div class="tc">{CHL(ch)}　{E(ch["title"])}<span class="dots"></span><span class="pg">{pages.get(ch["id"], "00")}</span></div>']
        for s in ch['sections']:
            rows.append(f'<div class="ts">{s["no"]}　{E(s["title"])}<span class="dots"></span><span class="pg">{pages.get(s["id"], "00")}</span></div>')
        if any(p['set'] == '章末' and p['home'] == ch['id'] for p in bk.problems):
            rows.append(f'<div class="ts">章末問題<span class="dots"></span><span class="pg">{pages.get("end" + ch["id"], "00")}</span></div>')
        if any(p['set'] == '確認テスト' and p['home'] == ch['id'] for p in bk.problems):
            rows.append(f'<div class="ts">確認テスト<span class="dots"></span><span class="pg">{pages.get("test" + ch["id"], "00")}</span></div>')
        if ch['id'] == vol1_last:
            for pt in sougou_parts[:1]:
                rows.append(f'<div class="tc">総合演習　第{pt}回<span class="dots"></span><span class="pg">{pages.get(f"sougou{pt}", "00")}</span></div>')
            rows.append(f'<div class="tc">索引（上巻）<span class="dots"></span><span class="pg">{pages.get("index1", "00")}</span></div>')
        tocb.append(''.join(rows))
    tail = []
    for pt in (sougou_parts[1:] if vol1_last else sougou_parts):
        tail.append(f'<div class="tc">総合演習　第{pt}回<span class="dots"></span><span class="pg">{pages.get(f"sougou{pt}", "00")}</span></div>')
    if any(p['set'] == '模試' for p in bk.problems):
        tail.append(f'<div class="tc">模擬試験・解答用紙<span class="dots"></span><span class="pg">{pages.get("mock", "00")}</span></div>')
    tail.append(f'<div class="tc">{"索引（上巻・下巻）" if vol1_last else "索引"}<span class="dots"></span><span class="pg">{pages.get("index", "00")}</span></div>')
    out.append(blk('<div class="fm-title">目次</div><div class="toc">' + tocb[0] + '</div>', 'newpage', anchor='toc', chapter='目次', section='目次'))
    for t in tocb[1:]:
        out.append(blk(f'<div class="toc">{t}</div>', 'tocb'))
    out.append(blk('<div class="toc">' + ''.join(tail) + '</div>', 'tocb'))
    toc_blocks = [b for b in out if 'data-anchor="toc"' in b or ' tocb' in b]
    vols = bk.data['book'].get('volumes') or []
    vol2_first = vols[1]['chapters'][0] if len(vols) > 1 else None
    wk_no = 0
    # 解説部分は完全解説book と同じ組み方を使う（表紙・目次・索引などを除いた本文だけを取り出す）
    body_blocks = kaisetsu_section_blocks(bk, pages)
    for ch in d['chapters']:
        if ch['id'] == vol2_first:
            # 上巻の終わり：上巻の裏表紙までで4の倍数にそろえ、下巻の表紙・目次を置く（ページ番号は通し）
            out.extend(sougou_blocks(bk, pages, sougou_parts[:1]))   # 総合演習 第1回は上巻の終わり
            out.extend(index_blocks(bk, pages, set(vols[0]['chapters']), 'index1'))
            vpad = 0
            if 'vol1back' in pages:
                n_before = (pages['vpad'] if 'vpad' in pages else pages['vol1back']) - 1   # 白ページを入れる前の、上巻の本文の終わり
                vpad = (-(n_before + 1)) % 4
            for i in range(vpad):
                out.append(fullpage('', 'nohead pk-blank', **({'anchor': 'vpad'} if i == 0 else {})))
            out.append(fullpage(back_html(bk, part + '　上巻'), 'nohead pk-back', anchor='vol1back'))
            out.append(fullpage(cover_html(bk, part + '　下巻'), 'nohead pk-cover', anchor='vol2'))
            out.append(fullpage('', 'nohead pk-blank'))
            for i, b in enumerate(toc_blocks):
                out.append(b.replace('data-anchor="toc"', 'data-anchor="toc2"'))
        out.extend(body_blocks[ch['id']])
        # 単元の入口：中学の復習と前提チェック
        if ch.get('intro'):
            out.append(blk(f'<div class="ih">中学の復習</div><div>{bk.md(ch["intro"], pages)}</div>', 'intro'))
        pre = [p for p in bk.problems if p['set'] == '前提' and p['home'] == ch['id']]
        if pre:
            out.append(blk(f'前提チェック　<span class="meta">{len(pre)}問　この単元に入る前に、中学とこれまでの単元の内容を確かめる　答え → 別冊</span>', 'phase keepnext wide', anchor='pre' + ch['id']))
            out.extend(problem_blocks(bk, pages, pre, wide=True))
        for s in ch['sections']:
            out.extend(body_blocks[s['id']])
            # 例題
            if s.get('worked'):
                out.append(blk('例題　<span class="meta">解き方の手順を読んでから、同じ手順で問題を解く</span>', 'phase keepnext'))
                for w in s['worked']:
                    wk_no += 1
                    out.append(blk(worked_html(bk, s, wk_no, w, pages, WORKED_STYLE), 'wk ' + WORKED_STYLE, anchor=f'w{wk_no}'))
            # 問題
            probs = [p for p in bk.problems if p['sec'] == s['id'] and p['set'] == '節末']
            if probs:
                mins = sum(p['min'] for p in probs)
                out.append(blk(f'問題　<span class="meta">{len(probs)}問　目安 {mins}分　答え → 別冊</span>', 'phase keepnext wide', anchor='m' + s['id']))
                for lv in (1, 2, 3):
                    ps = [p for p in probs if p['lv'] == lv]
                    if not ps: continue
                    out.append(blk(f'◆ {LVNAME[lv]}　<span class="lvs">{STAR[lv]}</span>', 'lvh keepnext wide'))
                    out.extend(problem_blocks(bk, pages, ps, wide=True))
            # 要点（赤シート）
            if s.get('summary'):
                out.append(blk('要点　赤字を赤シートで隠して言えるか確かめる', 'sumh keepnext'))
                n = len(s['summary'])
                for i, t in enumerate(s['summary'], 1):
                    out.append(blk(f'<span class="n">{i}</span><div>{bk.md(t, pages)}</div>', 'sm' + (' last' if i == n else '')))
        probs = [p for p in bk.problems if p['set'] == '章末' and p['home'] == ch['id']]
        if probs:
            out.append(blk(prob_header(bk, f'{CHL(ch)}　章末問題', probs, '節を混ぜて出題　答え → 別冊'), 'sech keepnext newpage wide', anchor='end' + ch['id'], section=f'{CHL(ch)}　章末問題'))
            out.extend(problem_blocks(bk, pages, probs, wide=True))
        probs = [p for p in bk.problems if p['set'] == '確認テスト' and p['home'] == ch['id']]
        if probs:
            mixed = any(bk.ch_of[p['sec']]['id'] != ch['id'] for p in probs)
            out.append(blk(prob_header(bk, f'{CHL(ch)}　確認テスト', probs, ('前の単元の問題も混ざる' if mixed else '節を混ぜて出題') + '　答え → 別冊（診断表つき）'), 'sech keepnext newpage wide', anchor='test' + ch['id'], section=f'{CHL(ch)}　確認テスト'))
            out.extend(problem_blocks(bk, pages, probs, wide=True))
    out.extend(mock_blocks(bk, pages, wide=True))
    out.extend(sougou_blocks(bk, pages, sougou_parts[1:] if vol2_first else None))
    # 索引（上下巻のある本は、下巻に上下巻のすべての用語を載せる）
    out.extend(index_blocks(bk, pages, None, 'index'))
    pad_and_colophon(out, pages, colophon)
    return out


def kaisetsu_section_blocks(bk, pages):
    """完全解説book の組み方から、章の見出しと各節の解説のかたまりだけを、章 ID・節 ID ごとに取り出す。"""
    allb = kaisetsu_blocks(bk, pages, '', '', '')
    res = {}
    cur = None
    for b in allb:
        m = re.search(r'data-anchor="(c\d+|s\d+)"', b.split('>', 1)[0])
        if m and ('chap' in b.split('>', 1)[0] or 'h2' in b.split('>', 1)[0]):
            cur = m.group(1); res[cur] = []
        if 'data-anchor="index"' in b.split('>', 1)[0]:
            cur = None
        if cur:
            res[cur].append(b)
    return res


def build_all(bk):
    b = bk.data['book']
    css = KAISETSU_CSS + COVER_CSS + LEGEND_CSS + PROB_CSS + WORKED_CSS
    def go(name, part, cfg, fn):
        global _back
        _back = back_html(bk, part + ('　下巻' if name == 'honsatsu' and bk.data['book'].get('volumes') else ''))
        lay = bk.render(name, f'{b["series"]} {b["vol"]}【{b["title"]}】{part}', css, json.dumps(cfg),
                        lambda pages: fn(bk, pages, part, cover_html(bk, part + ('　上巻' if name == 'honsatsu' and bk.data['book'].get('volumes') else '')), colophon_html(bk, part), legend_html(bk, part)))
        print(f'{part}: {lay["pages"]} ページ')
        return lay
    lay = go('honsatsu', '本冊', A4, honbun_blocks)
    bk.pages = lay['anchors']   # 別冊の参照ページは本冊のページ
    (bk.out / 'pages_honsatsu.json').write_text(json.dumps(lay['anchors'], ensure_ascii=False, indent=1))
    go('bessatsu', '別冊　解答解説', A4, kaitou_blocks)
