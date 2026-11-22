#!/usr/bin/env python3
"""模擬生徒の答え（review/<版>/S*_answers.json）を正答と突き合わせる。
4択・正誤・読解（選択式）は番号、整序は英文（大文字小文字・句読点の差は無視）を比べる。
和訳・英作・補充は自動では判定せず、並べて書き出す（目で確かめる）。
使い方: python3 compare_students.py review/v1
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import Book


def canon(s):
    s = re.sub(r'<[^>]+>', ' ', str(s)).lower().replace('’', "'")
    return ' '.join(re.findall(r"[a-z0-9']+", s))


def main(d):
    d = Path(d)
    bk = Book(sys.argv[2] if len(sys.argv) > 2 else 'eg01')
    by_label = {p['label']: p for p in bk.problems}
    out = ['# 模擬生徒の答えと正答の突き合わせ', '', '| 番号 | 形式 | ★ | 生徒の答え | 正答（別解） | 判定 |', '|---|---|---|---|---|---|']
    n = ok = 0; wrong = []
    for f in sorted(d.glob('S*_answers.json')):
        ans = json.loads(f.read_text())
        for label, a in ans.items():
            p = by_label.get(label)
            if not p: out.append(f'| {label} | ? | | {a} | 番号が問題にない | 要確認 |'); continue
            k = p['kind']; correct = [str(p['ans'])] + [str(x) for x in p.get('alt') or []]
            if k in ('4択', '正誤') or (k == '読解' and p.get('choices')):
                m = re.search(r'\d', str(a)); a1 = m.group(0) if m else str(a)
                res = '一致' if a1 == str(p['ans']) else '不一致'
            elif k == '整序':
                res = '一致' if canon(a) in [canon(c) for c in correct] else '不一致'
            else:
                res = '目視'
            n += 1; ok += res == '一致'
            if res == '不一致': wrong.append(label)
            out.append(f'| {label} | {k} | {"★" * p["lv"]} | {str(a)[:60]} | {" ／ ".join(c[:60] for c in correct)} | {res} |')
    out.insert(2, f'突き合わせ {n} 問、一致 {ok}、不一致 {len(wrong)}：{", ".join(wrong)}\n')
    (d / 'student_compare.md').write_text('\n'.join(out))
    print(f'{n} 問、一致 {ok}、不一致 {len(wrong)}: {wrong}')


if __name__ == '__main__':
    main(sys.argv[1])
