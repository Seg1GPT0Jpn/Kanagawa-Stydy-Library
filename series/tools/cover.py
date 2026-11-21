"""表紙の図：本文の例文から作る関係詞節の構造図（SVG）。
語の幅は書体ファイルの字幅から計算するので、線と矢印は語の位置に正確に合う。"""
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
_F = {}


def adv(text, font='Regular', size_pt=10):
    """Source Serif 4 SmText で text を size_pt で組んだときの幅（mm）。CSS の size-adjust 108% を含む。"""
    if font not in _F:
        f = TTFont(ROOT / 'fonts' / 'Source_Serif_4' / f'SourceSerif4SmText-{font}.ttf')
        _F[font] = (f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    cmap, hmtx, upm = _F[font]
    w = sum(hmtx[cmap[ord(c)]][0] for c in text)
    return w / upm * size_pt * 1.08 * 25.4 / 72


def relclause_svg(tokens, gap_after, antecedent, clause, labels, size=24, width=170):
    """tokens: 語の列（'_' は欠けた位置）。antecedent/clause: (開始, 終了) の語番号（両端含む）。
    labels: {'ante': '先行詞', 'clause': '関係詞節', 'gap': '欠けた目的語'}"""
    sp = adv(' ', size_pt=size)
    gapw = size * 0.9 * 25.4 / 72
    xs, ws = [], []
    x = 0
    for t in tokens:
        w = gapw if t == '_' else adv(t, 'Semibold' if t in ('that', 'who', 'which', 'whom', 'whose', 'where', 'when', 'what') else 'Regular', size)
        xs.append(x); ws.append(w); x += w + sp
    total = x - sp
    ox = (width - total) / 2
    base = 34  # ベースライン（mm）
    h = 62
    fs = size * 25.4 / 72  # mm
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}mm" height="{h}mm">']
    for i, t in enumerate(tokens):
        if t == '_':
            parts.append(f'<line x1="{ox + xs[i]:.2f}" y1="{base + .6:.2f}" x2="{ox + xs[i] + ws[i]:.2f}" y2="{base + .6:.2f}" stroke="#000" stroke-width=".5"/>')
            continue
        wt = 600 if t in ('that', 'who', 'which', 'whom', 'whose', 'where', 'when', 'what') else 400
        parts.append(f'<text x="{ox + xs[i]:.2f}" y="{base}" font-family="Ser" font-size="{fs:.2f}" font-weight="{wt}">{t}</text>')
    # 関係詞節の角括弧（下）
    c0, c1 = clause
    bx0, bx1 = ox + xs[c0] - 1, ox + xs[c1] + ws[c1] + 1
    by = base + 4.5
    parts.append(f'<path d="M{bx0:.2f},{by - 2} V{by} H{bx1:.2f} V{by - 2}" fill="none" stroke="#000" stroke-width=".35"/>')
    parts.append(f'<text x="{bx0 + 1:.2f}" y="{by + 5}" font-family="Goth" font-size="3.2">{labels["clause"]}</text>')
    # 先行詞の下線とラベル
    a0, a1 = antecedent
    ax0, ax1 = ox + xs[a0], ox + xs[a1] + ws[a1]
    parts.append(f'<line x1="{ax0:.2f}" y1="{by}" x2="{ax1:.2f}" y2="{by}" stroke="#000" stroke-width="1"/>')
    parts.append(f'<text x="{(ax0 + ax1) / 2:.2f}" y="{by + 5}" font-family="Goth" font-size="3.2" text-anchor="middle">{labels["ante"]}</text>')
    # 欠けた位置 → 先行詞 への弧
    g = tokens.index('_')
    gx = ox + xs[g] + ws[g] / 2
    tx = (ax0 + ax1) / 2
    top = base - fs * 0.75 - 4
    parts.append(f'<path d="M{gx:.2f},{base - fs * 0.15:.2f} C{gx:.2f},{top - 10:.2f} {tx:.2f},{top - 10:.2f} {tx:.2f},{top + 1.5:.2f}" fill="none" stroke="#000" stroke-width=".5"/>')
    parts.append(f'<path d="M{tx - 1.3:.2f},{top - .8:.2f} L{tx:.2f},{top + 1.8:.2f} L{tx + 1.3:.2f},{top - .8:.2f}" fill="none" stroke="#000" stroke-width=".5"/>')
    parts.append(f'<text x="{gx:.2f}" y="{base + 4.5 + 13}" font-family="Goth" font-size="3.2" text-anchor="middle">{labels["gap"]}</text>')
    parts.append(f'<line x1="{gx:.2f}" y1="{base + 2.2}" x2="{gx:.2f}" y2="{base + 4.5 + 9.5}" stroke="#000" stroke-width=".25"/>')
    parts.append('</svg>')
    return '\n'.join(parts)


EG01 = dict(tokens=['the', 'book', '[that', 'I', 'read', '_', 'yesterday]'], gap_after=4, antecedent=(0, 1), clause=(2, 6),
            labels={'ante': '先行詞', 'clause': '関係詞節', 'gap': '欠けた目的語'})
