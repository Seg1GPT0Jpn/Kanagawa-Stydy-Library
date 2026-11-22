#!/usr/bin/env python3
"""組む → 自動チェック → 合格したときだけ dist/<id>/ に配布用 PDF を書き出す。
書き出すもの：各冊子の A4 PDF、印刷用の面付け PDF、ページ順確認用のダミー面付け PDF。
- 64 ページまでの冊子は中綴じ（用紙を全部重ねて二つ折り）。
- それより厚い冊子は 16 ページごとの折丁に分けて面付けする（中綴じでは厚すぎて折れないため）。
- 上巻・下巻のある本（book.volumes）は、本冊を下巻の表紙（anchor 'vol2'）で2つの PDF に分ける。ページ番号は通し。
使い方: python3 release.py eg01
"""
import json, shutil, subprocess, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from impose import impose, impose_signatures, dummy, order, fold_and_read

PARTS = [('honsatsu', '本冊'), ('bessatsu', '別冊_解答解説')]
SADDLE_MAX = 64
SIG = 16


def split(src, a, b, dst):
    r = PdfReader(src); w = PdfWriter()
    for i in range(a - 1, b): w.add_page(r.pages[i])
    with open(dst, 'wb') as f: w.write(f)


def emit(pdf, dst, bid, name, tmp):
    n = len(PdfReader(pdf).pages)
    assert n % 4 == 0, f'{name}: {n} ページが4の倍数でない'
    shutil.copy(pdf, dst / f'{bid}_{name}_A4.pdf')
    dummy(n, 210, 297, tmp / f'dummy_{name}.pdf')
    if n <= SADDLE_MAX:
        impose(pdf, dst / 'booklet' / f'{bid}_{name}_中綴じ_A3.pdf')
        assert fold_and_read(order(n), n) == list(range(1, n + 1))
        impose(tmp / f'dummy_{name}.pdf', dst / 'dummy' / f'{bid}_{name}_ページ順確認_A3.pdf')
        print(f'{name}: {n} ページ → 中綴じ A3 {n // 2} 面（{n // 4} 枚を両面印刷・短辺とじ）')
    else:
        _, groups = impose_signatures(pdf, dst / 'booklet' / f'{bid}_{name}_折丁{SIG}p_A3.pdf', SIG)
        for a, b in groups:
            m = b - a + 1
            assert fold_and_read(order(m), m) == list(range(1, m + 1))
        impose_signatures(tmp / f'dummy_{name}.pdf', dst / 'dummy' / f'{bid}_{name}_ページ順確認_A3.pdf', SIG)
        print(f'{name}: {n} ページ → {SIG} ページの折丁 {len(groups)} 組（A3 {n // 2} 面。折丁ごとに両面印刷・短辺とじで二つ折りし、順に重ねて綴じる）')
    return n


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
    for key, name in PARTS:
        pdf = src / f'{key}.pdf'
        anchors = json.loads((src / f'{key}.layout.json').read_text())['anchors']
        if key == 'honsatsu' and 'vol2' in anchors:
            n = len(PdfReader(pdf).pages); v2 = anchors['vol2']
            split(pdf, 1, v2 - 1, src / f'{key}_上巻.pdf'); split(pdf, v2, n, src / f'{key}_下巻.pdf')
            emit(src / f'{key}_上巻.pdf', dst, bid, f'{name}_上巻_p1-{v2 - 1}', src)
            emit(src / f'{key}_下巻.pdf', dst, bid, f'{name}_下巻_p{v2}-{n}', src)
        else:
            emit(pdf, dst, bid, name, src)
    print('出力先:', dst)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'eg01')
