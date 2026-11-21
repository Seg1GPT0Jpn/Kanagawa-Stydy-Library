#!/usr/bin/env python3
"""組む → 自動チェック → 合格したときだけ dist/<id>/ に配布用 PDF を書き出す。
書き出すもの：各冊子の A4（要点まとめは A5）PDF、中綴じ用の面付け PDF、ページ順確認用のダミー面付け PDF。
使い方: python3 release.py eg01
"""
import shutil, subprocess, sys
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from impose import impose, dummy, order, fold_and_read

PARTS = [('kaisetsu', '1_完全解説book', 'A4', 'A3'), ('matome', '2_要点まとめbook', 'A5', 'A4'),
         ('mondai', '3_問題集', 'A4', 'A3'), ('kaitou', '4_解答解説', 'A4', 'A3')]


def main(bid):
    tools = ROOT / 'tools'
    subprocess.run([sys.executable, str(tools / 'build.py'), bid], check=True)
    r = subprocess.run([sys.executable, str(tools / 'check.py'), bid])
    if r.returncode:
        raise SystemExit('自動チェックに失敗したので出力しない')
    src = ROOT / 'build' / bid
    dst = ROOT / 'dist' / bid
    if dst.exists(): shutil.rmtree(dst)
    (dst / 'booklet').mkdir(parents=True); (dst / 'dummy').mkdir()
    for key, name, size, sheet in PARTS:
        shutil.copy(src / f'{key}.pdf', dst / f'{bid}_{name}_{size}.pdf')
        n = impose(src / f'{key}.pdf', dst / 'booklet' / f'{bid}_{name}_中綴じ_{sheet}.pdf')
        assert fold_and_read(order(n), n) == list(range(1, n + 1))
        w, h = (210, 297) if size == 'A4' else (148, 210)
        dummy(n, w, h, src / f'dummy_{key}.pdf')
        impose(src / f'dummy_{key}.pdf', dst / 'dummy' / f'{bid}_{name}_ページ順確認_{sheet}.pdf')
        im = PdfReader(dst / 'booklet' / f'{bid}_{name}_中綴じ_{sheet}.pdf')
        print(f'{name}: {n} ページ → 中綴じ {len(im.pages)} 面（{n // 4} 枚を両面印刷・短辺とじ）')
    print('出力先:', dst)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'eg01')
