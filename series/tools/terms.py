#!/usr/bin/env python3
"""定義済みの用語の一覧（design/12_terms.md）をデータから作る。使い方: python3 terms.py g1"""
import sys, glob, yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bid = sys.argv[1] if len(sys.argv) > 1 else 'g1'
rows = []
for f in [ROOT / 'src' / f'{bid}.yaml'] + [Path(p) for p in sorted(glob.glob(str(ROOT / 'src' / 'parts' / f'{bid}_*.yaml')))]:
    d = yaml.safe_load(f.read_text())
    for c in d.get('chapters') or []:
        for s in c.get('sections') or []:
            for b in s.get('body') or []:
                for n in b.get('notes') or []:
                    if n.get('kind') == '用語':
                        rows.append((n.get('yomi', ''), n['term'], s['id'], str(n.get('text', ''))[:60]))
rows.sort()
out = ['# 定義済みの用語（自動生成。手で直さない）', '', f'本：{bid}　用語数：{len(rows)}', '', '| 用語 | 読み | 定義した節 | 定義（冒頭） |', '|---|---|---|---|']
out += [f'| {t} | {y} | {sid} | {txt} |' for y, t, sid, txt in rows]
(ROOT / 'design' / '12_terms.md').write_text('\n'.join(out) + '\n')
print(len(rows))
