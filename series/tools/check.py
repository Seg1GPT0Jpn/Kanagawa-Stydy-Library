#!/usr/bin/env python3
"""組み上がった4冊の自動チェック。1つでも失敗したら終了コード 1（出力を配布しない）。
使い方: python3 check.py eg01
"""
import json, re, subprocess, sys, unicodedata
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build import Book

NAMES = {'honsatsu': '本冊', 'bessatsu': '別冊 解答解説'}
FAIL, OK = [], []


def fail(m): FAIL.append(m)
def ok(m): OK.append(m)


def pdftext(pdf, first=None, last=None):
    a = ['pdftotext', '-enc', 'UTF-8']
    if first: a += ['-f', str(first), '-l', str(last or first)]
    return subprocess.run(a + [str(pdf), '-'], capture_output=True, text=True).stdout


BK = None


def norm(s, md=False):
    """比較用：（データなら記法を本と同じに変換し）HTML を外し、空白・記号の差を消す"""
    s = str(s)
    if md and BK is not None:
        import html as _h
        s = _h.unescape(re.sub(r'<[^>]+>', '', BK.md(s, BK.pages)))
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\{\{|\}\}|\*\*|<<|>>|\*|__|[①-⑳]', '', s)
    s = s.replace('＿', '')
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('〜', '~').replace('～', '~')
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'[\s\[\]［］()（）]', '', s)


def coltext(pdf, npages, n, layout=True):
    """本文欄と側注欄を分けて読み取る（側注の文字が本文の行に混ざらないように）"""
    from books import A4, A5
    from books import A4_1COL
    cfg = A4
    pt = 72 / 25.4
    out = []
    for pg in range(1, npages + 1):
        odd = pg % 2 == 1
        left = cfg['inner'] if odd else cfg['outer']
        boxes = []
        if cfg['sideW']:
            mainL = left + (0 if odd else cfg['sideW'] + cfg['gap'])
            sideL = left + (cfg['mainW'] + cfg['gap'] if odd else 0)
            boxes = [(mainL, cfg['mainW'] + 2), (sideL, cfg['sideW'])]
            boxes.append((left, cfg['pw'] - cfg['inner'] - cfg['outer']))  # 全幅（本冊の問題）
            boxes.append((left, 130))  # 問題文の範囲（外側の解答欄を除く）
        else:
            boxes = [(left, cfg['pw'] - cfg['inner'] - cfg['outer'])]
        for x, w in boxes:
            r = subprocess.run(['pdftotext'] + (['-layout'] if layout else []) + ['-enc', 'UTF-8', '-f', str(pg), '-l', str(pg), '-x', str(int(x * pt)), '-y', '0', '-W', str(int(w * pt)), '-H', str(int(cfg['ph'] * pt)), str(pdf), '-'], capture_output=True, text=True)
            out.append(r.stdout)
    return '\n'.join(out)


def main(bid):
    global BK
    bk = Book(bid)
    BK = bk
    bk.pages = json.loads((bk.out / 'honsatsu.layout.json').read_text())['anchors']
    out = bk.out
    lay = {n: json.loads((out / f'{n}.layout.json').read_text()) for n in NAMES}
    kp = lay['honsatsu']['anchors']
    texts = {n: pdftext(out / f'{n}.pdf') for n in NAMES}
    cols = {n: coltext(out / f'{n}.pdf', lay[n]['pages'], n) for n in NAMES}
    cols2 = {n: coltext(out / f'{n}.pdf', lay[n]['pages'], n, layout=False) for n in NAMES}
    # 位置どおりの読み取りと流れ順の読み取りの両方を見る（折り返しの読み取り順の差による誤検出を防ぐ）
    ntexts = {n: norm(t) + '\u0000' + norm(cols2[n]) for n, t in cols.items()}

    # 1. ページ数：PDF と組版結果の一致、4の倍数
    for n, name in NAMES.items():
        pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', str(out / f'{n}.pdf')], capture_output=True, text=True).stdout).group(1))
        if pages != lay[n]['pages']: fail(f'{name}: PDF {pages} ページと組版 {lay[n]["pages"]} ページが違う')
        elif pages % 4: fail(f'{name}: 総ページ {pages} が4の倍数でない')
        else: ok(f'{name}: {pages} ページ（4の倍数）')
        if lay[n]['errors']: fail(f'{name}: 組版エラー {lay[n]["errors"]}')

    # 2. 抜け落ち：データの項目が PDF のテキストにすべて出ているか
    secs = [s for c in bk.data['chapters'] for s in c['sections']]
    miss = []
    pagetexts = {}

    def cell_on_page(c):
        # 表のマスは折り返しで隣のマスと行が混ざるので、語のまとまりがすべて同じページにあるかで見る
        import html as _h
        t = _h.unescape(re.sub(r'<[^>]+>', ' ', bk.md(c, bk.pages)))
        # 表のマスは折り返しで隣のマスと行が混ざる。英語は語ごと、和文は1字ずつ、同じページにすべてあるかを見る（弱い照合。表のマスだけに使う）
        tn = norm(t)
        chunks = [norm(w.strip('-')) for w in re.findall(r"[A-Za-z0-9'\-]+", t) if w.strip('-')] + re.findall(r'[ぁ-んァ-ヶ一-龥]', tn)
        for pg in range(1, lay['honsatsu']['pages'] + 1):
            if pg not in pagetexts: pagetexts[pg] = norm(pdftext(out / 'honsatsu.pdf', pg))
            if all(ch in pagetexts[pg] for ch in chunks): return True
        return False
    for s in secs:
        if norm(s['title'], md=True) not in ntexts['honsatsu']: miss.append(('節題', s['id']))
        for e in s.get('examples', []):
            if norm(e['en'], md=True) not in ntexts['honsatsu']: miss.append(('例文', e['id'], e['en'][:30]))
            if norm(e['ja'], md=True) not in ntexts['honsatsu']: miss.append(('和訳', e['id']))
        for b in s.get('body', []):
            if 'p' in b and norm(b['p'], md=True)[:40] not in ntexts['honsatsu']: miss.append(('段落', s['id'], b['p'][:20]))
            if 'table' in b:
                for r in b['table']['rows']:
                    for c in r:
                        if norm(c, md=True) not in ntexts['honsatsu'] and not cell_on_page(c):
                            miss.append(('表', s['id'], c))
            if 'check' in b:
                for q in b['check']:
                    if norm(q['a'], md=True) not in ntexts['honsatsu']: miss.append(('確認の答え', s['id'], q['a']))
        for sm in s.get('summary', []):
            if norm(sm, md=True) not in ntexts['honsatsu']: miss.append(('要点', s['id'], sm[:20]))
    for p in bk.problems:
        if norm(p['why'], md=True)[:40] not in ntexts['bessatsu']: miss.append(('根拠', p['id']))
        if norm(p['trap'], md=True)[:40] not in ntexts['bessatsu']: miss.append(('よくある間違い', p['id']))
        if norm(p['q'], md=True)[:40] not in ntexts['honsatsu']: miss.append(('問題文', p['id']))
    if miss: fail(f'抜け落ち {len(miss)} 件: {miss[:8]}')
    else: ok(f'抜け落ちなし（節 {len(secs)}、例文 {sum(len(s.get("examples", [])) for s in secs)}、問題 {len(bk.problems)}、要点 {sum(len(s.get("summary", [])) for s in secs)}）')

    # 例文番号が本文の中で 1, 2, 3, … と飛ばずに並ぶか
    seq = [int(m) for m in re.findall(r'<span class="n">(\d+)</span><div><div class="e">', (out / 'honsatsu.html').read_text())]
    if seq != list(range(1, len(seq) + 1)): fail(f'例文番号が連番でない: {[x for i, x in enumerate(seq) if x != i + 1][:5]}')
    else: ok(f'例文番号 1〜{len(seq)} が本文の順に連番')

    # 3. 番号の一致：問題集と解答解説の問題番号が、データの順と完全に一致するか
    want = [p['no'] for p in bk.problems if p['set'] != '模試']
    for n in ('honsatsu', 'bessatsu'):
        # 問題の見出しとして組んだ番号（<span class="no">問N</span>）の並び。診断表の番号は含めない
        h = (out / f'{n}.html').read_text()
        heads = [int(x) for x in re.findall(r'<span class="no">問(\d+)</span>', h)]
        got_txt = {int(x) for x in re.findall(r'問\s?(\d+)', texts[n])}
        if heads != want:
            fail(f'{NAMES[n]}: 問題の見出しの番号の並びがデータと違う（先頭の違い: {[(i + 1, a, b) for i, (a, b) in enumerate(zip(heads, want)) if a != b][:3]}、数 {len(heads)}/{len(want)}）')
        elif set(want) - got_txt:
            fail(f'{NAMES[n]}: PDF に出ていない問題番号 {sorted(set(want) - got_txt)[:10]}')
        else:
            ok(f'{NAMES[n]}: 問題番号 問1〜問{len(want)} がデータの順にそろい、PDF にも出ている')
    mock = [p for p in bk.problems if p['set'] == '模試']
    if mock:
        labels = [p['label'] for p in mock]
        for n, where in (('honsatsu', '本冊'), ('bessatsu', '別冊')):
            t = re.sub(r'\s', '', texts[n])
            lost = [l for l in labels if re.sub(r'\s', '', l) not in t]
            if lost: fail(f'模擬試験の番号が{where}にない: {lost}')
        # 解答用紙：同じ番号が同じ順で並ぶか
        sheet = (out / 'honsatsu.html').read_text()
        got = re.findall(r'<td class="sl">(第\d問 \(\d+\))</td>', sheet)
        if got != labels: fail(f'解答用紙の番号が問題と違う: {got[:5]} / {labels[:5]}')
        else: ok(f'模擬試験 {len(labels)} 問：問題冊子・解答用紙・解答解説の番号が一致')
        tot = sum(p.get('pts', 0) for p in mock)
        if tot != 100: fail(f'模擬試験の配点合計が {tot}')
    a_m = lay['honsatsu']['anchors']; a_k = lay['bessatsu']['anchors']
    if [k for k in a_m if k.startswith('q')] and set(k for k in a_m if re.fullmatch(r'q\d+', k)) != set(k for k in a_k if re.fullmatch(r'q\d+', k)):
        fail('問題集と解答解説で問題の集合が違う')

    # 4. 参照ページ：「→ p.N」がすべて正しいページを指すか
    bad = []
    for n in NAMES:
        h = (out / f'{n}.html').read_text()
        for m in re.finditer(r'<span class="pref" data-ref="(s\d+)">→&nbsp;p\.(\d+)</span>', h):
            if int(m.group(2)) != kp.get(m.group(1)): bad.append((n, m.group(1), m.group(2), kp.get(m.group(1))))
    # 節の見出しが、参照表のページに本当にあるか
    for s in secs:
        pg = kp.get(s['id'])
        if not pg or norm(s['title'], md=True) not in norm(pdftext(out / 'honsatsu.pdf', pg)): bad.append(('honsatsu', s['id'], pg, '見出しがそのページにない'))
    n_ref = sum(len(re.findall(r'data-ref="s\d+"', (out / f'{n}.html').read_text())) for n in NAMES)
    if bad: fail(f'参照ページの誤り {len(bad)} 件: {bad[:6]}')
    else: ok(f'参照ページ {n_ref} か所がすべて正しいページを指す')

    # 目次・索引のページ欄に、ページが見つからなかった「00」が残っていないか
    for n, name in NAMES.items():
        h = (out / f'{n}.html').read_text()
        z = re.findall(r'<span class="pg">00</span>', h)
        if z: fail(f'{name}: 目次・索引でページが見つからない項目が {len(z)} 件（00 のまま）')

    # 5. 混入：組版の残骸・未置換の記法
    pats = ['class=', '">', '</', 'undefined', 'NaN', '[object', 'p.00', '{{', '}}', '<<', '>>', '@s', '@e', '**', 'null', 'None']
    for n, name in NAMES.items():
        hits = [p for p in pats if p in texts[n]]
        if hits: fail(f'{name}: 混入 {hits}')
    if not any(f.startswith(tuple(NAMES.values())) and '混入' in f for f in FAIL): ok('混入なし（class= 〉 </ undefined NaN [object p.00 未置換の記法）')

    # 6. 色：青は0、使ってよいのは黒・灰・赤系だけ。赤は答え（.ans）だけ
    css = (ROOT / 'tools' / 'book.css').read_text() + (ROOT / 'tools' / 'books.py').read_text()
    reds = re.findall(r'([.#\w\- >,]+)\{[^}]*var\(--red\)', css)
    if any(sel.strip() != '.ans' for sel in reds): fail(f'赤を答え以外に指定: {reds}')
    cols = set(c.lower() for c in re.findall(r'#[0-9a-fA-F]{6}\b', css))
    if cols - {'#000000', '#ff4b00', '#e6e6e6', '#ffffff'}: fail(f'許可外の色指定 {cols}')
    for n, name in NAMES.items():
        d = out / 'png'; d.mkdir(exist_ok=True)
        for f in d.glob(f'{n}-*.png'): f.unlink()
        subprocess.run(['pdftoppm', '-r', '50', '-png', str(out / f'{n}.pdf'), str(d / n)], check=True)
        blue = other = redpx = 0
        for f in sorted(d.glob(f'{n}-*.png')):
            a = np.asarray(Image.open(f).convert('RGB')).astype(int)
            r, g, b = a[..., 0], a[..., 1], a[..., 2]
            gray = (a.max(-1) - a.min(-1)) < 16
            redfam = (r >= g - 2) & (g >= b - 8) & (r - b > 6)
            blue += int(((b > r + 30) & (b > g + 30)).sum())
            other += int((~gray & ~redfam).sum())
            redpx += int((~gray & redfam).sum())
            # 赤シート越しの見え方：赤成分だけの画像（赤い所は紙と同じに見える）
            Image.fromarray(r.astype('uint8')).save(f.with_name(f.stem + '-redsheet.png')) if f.stem.endswith(('-05', '-5')) else None
        if blue: fail(f'{name}: 青の画素 {blue}')
        if other > 50: fail(f'{name}: 黒・灰・赤以外の色の画素 {other}')
        else: ok(f'{name}: 青 0、色は黒・灰・赤のみ（赤の画素 {redpx}）')
    # 赤字が赤シートで消えるか（赤成分だけで見たとき、答えの文字が背景と区別できないか）
    # #FF4B00 の赤成分は 255＝白と同じ。画面上の再現としての確認（実際の赤シート・印刷では要確認）
    ok('赤 #FF4B00 の赤成分は 255（白と同じ）：赤成分だけの画像では答えが消える（実物の赤シートでの確認は未実施）')

    # 7. はみ出し・文字切れ：全テキストが版面の中にあるか（pdftotext -bbox）
    for n, name in NAMES.items():
        bb = subprocess.run(['pdftotext', '-bbox', str(out / f'{n}.pdf'), '-'], capture_output=True, text=True).stdout
        outside = []
        for pg in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', bb, re.S):
            W, H = float(pg.group(1)), float(pg.group(2))
            for w in re.finditer(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', pg.group(3)):
                x0, y0, x1, y1 = map(float, w.groups()[:4])
                m = 8 * 72 / 25.4  # 仕上がりから 8mm より外に文字があれば失敗
                if x0 < m or y0 < m or x1 > W - m or y1 > H - m: outside.append(w.group(5))
        if outside: fail(f'{name}: 版面外の文字 {outside[:5]}')
    # 単語の途中での改行（行末のハイフン）
    for n, name in NAMES.items():
        lines = texts[n].splitlines()
        hy = [l for l in lines if re.search(r'[a-z]-$', l)]
        if hy: fail(f'{name}: 行末ハイフン（単語の途中で改行）{hy[:3]}')
    if not any('版面外' in f or '行末ハイフン' in f for f in FAIL): ok('はみ出し・版面外の文字・単語の途中の改行なし')

    # 8. 書体：すべて埋め込み、Type 3 なし
    for n, name in NAMES.items():
        f = subprocess.run(['pdffonts', str(out / f'{n}.pdf')], capture_output=True, text=True).stdout.splitlines()[2:]
        if any('Type 3' in l for l in f): fail(f'{name}: Type 3 書体')
        fams = {re.sub(r'^[A-Z]{6}\+', '', l.split()[0]) for l in f if l.strip()}
        bad = {x for x in fams if not x.startswith(('BIZUDPMincho', 'BIZUDPGothic', 'SourceSerif4'))}
        if bad: fail(f'{name}: ライセンスを確かめていない書体が入っている（代わりの書体で表示された文字がある）: {sorted(bad)}')
        if any(l.split()[-5] != 'yes' for l in f if l.strip()): fail(f'{name}: 埋め込まれていない書体')
    if not any('書体' in x for x in FAIL): ok('書体は BIZ UDP明朝・BIZ UDPゴシック・Source Serif 4 だけ。すべて埋め込み・Type 3 なし')

    # 9. データ検査（形式・参照・整序の語・AI多用語）
    r = subprocess.run([sys.executable, str(ROOT / 'tools' / 'validate.py'), '--strict', str(ROOT / 'src' / f'{bid}.yaml')] + [str(p) for p in sorted((ROOT / 'src' / 'parts').glob(f'{bid}_*.yaml'))], capture_output=True, text=True)
    if r.returncode: fail('データ検査: ' + ' / '.join(l for l in r.stdout.splitlines() if l.startswith('ERROR'))[:800])
    else: ok('データ検査: ' + r.stdout.strip().splitlines()[-1])

    for m in OK: print('OK  ', m)
    for m in FAIL: print('FAIL', m)
    print(f'\n合格 {len(OK)}、失敗 {len(FAIL)}')
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'eg01'))
