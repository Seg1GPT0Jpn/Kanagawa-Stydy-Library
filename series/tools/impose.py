#!/usr/bin/env python3
"""中綴じ冊子用の面付け（左綴じ・横組み）。
N ページ（4の倍数）の本を、2倍の大きさの用紙の両面に2ページずつ並べる。
A4 の本 → A3 用紙（横）、A5 の本 → A4 用紙（横）。用紙を重ねて二つ折りにし、中央を綴じる。

左綴じでの k 枚目（0 から）の並び：
  表面　左 = N-2k　　右 = 2k+1
  裏面　左 = 2k+2　　右 = N-2k-1
印刷は「両面・短辺とじ」。
"""
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation, PageObject


def order(n, binding='left'):
    assert n % 4 == 0, f'ページ数 {n} が4の倍数でない'
    sides = []
    for k in range(n // 4):
        front = (n - 2 * k, 2 * k + 1)
        back = (2 * k + 2, n - 2 * k - 1)
        if binding == 'right':
            front, back = front[::-1], back[::-1]
        sides += [front, back]
    return sides


def fold_and_read(sides, n):
    """面付けした用紙を重ねて二つ折りにしたとき、読む順に並ぶページ番号を求める（検証用）。
    各用紙の表裏・左右から、冊子の各ページ位置を復元する。"""
    sheets = [(sides[2 * k], sides[2 * k + 1]) for k in range(len(sides) // 2)]
    first_half, second_half = [], []
    for front, back in sheets:           # 外側の用紙から
        first_half += [front[1], back[0]]  # 右半分の表、その裏（左綴じでは右半分が前半）
        second_half = [back[1], front[0]] + second_half
    return first_half + second_half


def impose(src, dst, binding='left'):
    r = PdfReader(src)
    n = len(r.pages)
    w = float(r.pages[0].mediabox.width); h = float(r.pages[0].mediabox.height)
    out = PdfWriter()
    for left, right in order(n, binding):
        sheet = PageObject.create_blank_page(width=2 * w, height=h)
        sheet.merge_transformed_page(r.pages[left - 1], Transformation().translate(0, 0))
        sheet.merge_transformed_page(r.pages[right - 1], Transformation().translate(w, 0))
        out.add_page(sheet)
    with open(dst, 'wb') as f:
        out.write(f)
    return n


def impose_signatures(src, dst, sig=16, binding='left'):
    """厚い本用：sig ページずつの折丁に分けて面付けする。折丁ごとに用紙を重ねて二つ折りにし、
    折丁を順に重ねて綴じる（平綴じ・糸かがり・製本テープなど）。最後の折丁は残りのページ数（4の倍数）。
    返り値：(総ページ数, 各折丁の (最初のページ, 最後のページ))"""
    r = PdfReader(src)
    n = len(r.pages)
    assert n % 4 == 0, f'ページ数 {n} が4の倍数でない'
    w = float(r.pages[0].mediabox.width); h = float(r.pages[0].mediabox.height)
    out = PdfWriter(); groups = []
    for start in range(0, n, sig):
        m = min(sig, n - start)
        groups.append((start + 1, start + m))
        for left, right in order(m, binding):
            sheet = PageObject.create_blank_page(width=2 * w, height=h)
            sheet.merge_transformed_page(r.pages[start + left - 1], Transformation().translate(0, 0))
            sheet.merge_transformed_page(r.pages[start + right - 1], Transformation().translate(w, 0))
            out.add_page(sheet)
    with open(dst, 'wb') as f:
        out.write(f)
    return n, groups


def dummy(n, w_mm, h_mm, path):
    """ページ番号だけのダミー PDF"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    c = canvas.Canvas(str(path), pagesize=(w_mm * mm, h_mm * mm))
    for i in range(1, n + 1):
        c.setFont('Helvetica-Bold', 120)
        c.drawCentredString(w_mm * mm / 2, h_mm * mm / 2 - 40, str(i))
        c.setFont('Helvetica', 14)
        c.drawCentredString(w_mm * mm / 2, 20, 'recto (odd)' if i % 2 else 'verso (even)')
        c.showPage()
    c.save()


if __name__ == '__main__':
    impose(sys.argv[1], sys.argv[2])
