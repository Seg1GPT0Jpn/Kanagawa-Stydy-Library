#!/usr/bin/env python3
"""4択・読解（選択式）の正解の位置をならす。
正解の選択肢を行き先の位置の選択肢と入れ替え、why・trap・alt・fix・q の中の ①〜④ を同じ対応で書き換える。
行き先は、全体で各番号が同じ数に近づくように、また同じ節・同じ大問で同じ番号が3問続かないように決める。
結果は実行のたびに同じ（乱数を使わない）。正誤は下線の位置が文の順で決まるので対象外。
使い方: python3 rebalance.py        （src/parts/*.yaml と src/eg01.yaml を書き換える）
"""
import glob, re, sys, zlib
from collections import Counter
from pathlib import Path
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
CIRC = '①②③④'


def main(bid='eg01'):
    y = YAML(); y.preserve_quotes = True; y.width = 100000; y.indent(mapping=2, sequence=2, offset=0)
    files = [ROOT / 'src' / f'{bid}.yaml'] + [Path(f) for f in sorted(glob.glob(str(ROOT / 'src' / 'parts' / f'{bid}_*.yaml')))]
    docs = {f: y.load(f.read_text()) for f in files}
    probs = []
    for f in files:
        for p in docs[f].get('problems') or []:
            if p.get('kind') in ('4択', '読解') and p.get('choices') and len(p['choices']) == 4 and str(p.get('ans')) in '1234':
                probs.append(p)
    count = Counter()
    recent = {}
    changed = 0
    for p in probs:
        grp = (p.get('set'), p.get('part') if p.get('set') == '模試' else p.get('sec'))
        hist = recent.setdefault(grp, [])
        # 候補：全体で少ない番号から。同じ番号が直前2問と同じなら避ける。同点は ID から決まる順で選ぶ
        h = zlib.crc32(str(p['id']).encode())
        order = sorted(range(4), key=lambda i: (count[i], (i + h) % 4))
        target = next(i for i in order if not (len(hist) >= 2 and hist[-1] == hist[-2] == i))
        cur = int(str(p['ans'])) - 1
        if target != cur:
            ch = p['choices']
            ch[cur], ch[target] = ch[target], ch[cur]
            m = {CIRC[cur]: CIRC[target], CIRC[target]: CIRC[cur]}
            for k in ('why', 'trap', 'q', 'fix'):
                if isinstance(p.get(k), str):
                    p[k] = type(p[k])(''.join(m.get(c, c) for c in p[k])) if type(p[k]) is not str else ''.join(m.get(c, c) for c in p[k])
            if p.get('alt'):
                p['alt'] = [''.join(m.get(c, c) for c in str(a)) for a in p['alt']]
            # 番号が並ぶとき（③④ など）は小さい順にそろえる
            for k in ('why', 'trap'):
                if isinstance(p.get(k), str):
                    p[k] = re.sub('[①②③④]{2,}', lambda mm: ''.join(sorted(mm.group(0))), p[k])
            p['ans'] = str(target + 1)
            changed += 1
        count[target] += 1
        hist.append(target)
    for f in files:
        with open(f, 'w') as fh:
            y.dump(docs[f], fh)
    print(f'選択式 {len(probs)} 問、並べ替え {changed} 問、正解の位置', {CIRC[i]: count[i] for i in range(4)})


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'eg01')
