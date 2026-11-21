#!/usr/bin/env python3
"""単一データファイル (series/src/<id>.yaml) から4冊の PDF を作る。

使い方: python3 series/tools/build.py eg01
手順: 完全解説book を組む → 参照ページ表を作る → 要点まとめ・問題集・解答解説を組む → 自動チェック。
各冊子は2回組み、1回目のページ割りで目次・索引・参照ページを埋めて2回目を組む。
"""
import html, json, re, subprocess, sys, os
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
STAR = {1: '★', 2: '★★', 3: '★★★'}
CIRC = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'


class Book:
    def __init__(self, bid):
        self.bid = bid
        self.data = yaml.safe_load((ROOT / 'src' / f'{bid}.yaml').read_text())
        self.merge_parts()
        self.out = ROOT / 'build' / bid
        self.out.mkdir(parents=True, exist_ok=True)
        self.ex_no = {}      # e001 -> 1
        self.sec_no = {}     # s01 -> 1
        self.sec_title = {}
        self.ch_of = {}
        self.terms = {}      # term -> yomi
        n_ex = 0; n_sec = 0
        for ci, ch in enumerate(self.data['chapters'], 1):
            ch['no'] = ci
            for s in ch['sections']:
                n_sec += 1; s['no'] = n_sec
                self.sec_no[s['id']] = n_sec; self.sec_title[s['id']] = s['title']; self.ch_of[s['id']] = ch
                # 例文番号は本文に出る順に振る（データの並びではなく）
                for blkd in s.get('body', []):
                    for eid in blkd.get('ex', []) or []:
                        if eid not in self.ex_no:
                            n_ex += 1; self.ex_no[eid] = n_ex
                for b in s.get('body', []):
                    for nt in b.get('notes', []) or []:
                        if nt['kind'] == '用語':
                            self.terms[nt['term']] = nt.get('yomi', nt['term'])
        self.problems = self.data.get('problems', [])
        n = 0
        for p in self.problems:
            if p['set'] != '模試':
                n += 1; p['no'] = n
        m = 0; k = {}
        for p in self.problems:
            if p['set'] == '模試':
                m += 1; p['no'] = m
                k[p['part']] = k.get(p['part'], 0) + 1
                p['label'] = f'第{p["part"]}問 ({k[p["part"]]})'
            else:
                p['label'] = f'問{p["no"]}'
        self.pages = {}      # 参照ページ表（完全解説book）: anchor -> page

    def merge_parts(self):
        """src/parts/*.yaml（章ごとの執筆ファイル）を節 ID で本体に差し込む。
        配布する本の唯一の情報源は、結合後に書き出す build/<id>/merged.yaml。"""
        chs = {c['id']: c for c in self.data['chapters']}
        for p in sorted((ROOT / 'src' / 'parts').glob('*.yaml')):
            part = yaml.safe_load(p.read_text())
            for pc in part.get('chapters', []):
                ch = chs[pc['id']]
                if pc.get('lead'): ch['lead'] = pc['lead']
                idx = {s['id']: i for i, s in enumerate(ch['sections'])}
                for ps in pc['sections']:
                    ch['sections'][idx[ps['id']]] = ps
            self.data.setdefault('problems', []).extend(part.get('problems', []) or [])
        # 指示文：同じ形式の直前の問題から引き継ぐ（節末は節ごと、章末は章ごと、模試は大問ごと）。
        # 引き継ぐものがなければ形式ごとの標準の指示を使う。正誤は全冊で1つの言い回しにそろえる。
        DEFAULT = {'4択': '（　）に入る最も適切なものを1つ選びなさい。',
                   '正誤': '下線部①〜④のうち、誤りをふくむものを1つ選びなさい。',
                   '整序': '日本語の意味になるように（　）内の語を並べかえなさい。',
                   '和訳': '下線部を日本語に訳しなさい。',
                   '読解': '次の英文を読み、問いの答えとして最も適切なものを1つ選びなさい。'}
        last = {}
        for p in self.data.get('problems', []):
            chid = next(c['id'] for c in self.data['chapters'] if any(s['id'] == p['sec'] for s in c['sections']))
            unit = ('模試', p.get('part')) if p['set'] == '模試' else ((p['sec'] if p['set'] == '節末' else chid), p['set'])
            k = unit + (p['kind'],)
            if p.get('inst'): last[k] = p['inst']
            p['inst_eff'] = p.get('inst') or last.get(k) or DEFAULT.get(p['kind'])
            if p['kind'] == '正誤':
                p['inst_eff'] = DEFAULT['正誤'] if '直しなさい' not in (p['inst_eff'] or '') else '下線部①〜④のうち、誤りをふくむものを1つ選び、正しい形に直しなさい。'
        order = {s['id']: i for i, s in enumerate(s for c in self.data['chapters'] for s in c['sections'])}
        setord = {'節末': 0, '章末': 1, '模試': 2}
        # 並び：模試は最後。章末は章の最後。節末は節の順
        def key(p):
            ch = next(c for c in self.data['chapters'] if any(s['id'] == p['sec'] for s in c['sections']))
            ci = self.data['chapters'].index(ch)
            if p['set'] == '模試': return (99, 0, 0, 0)
            if p['set'] == '章末': return (ci, 1, 0, 0)
            return (ci, 0, order[p['sec']], p['lv'])  # 節末は難易度の順（◆基本→標準→発展）
        self.data['problems'] = sorted(self.data.get('problems', []), key=key)  # 安定ソート

    # ---------- 文中記法 ----------
    def md(self, s, pages=None):
        s = html.escape(str(s), quote=False)
        s = s.replace('&lt;br&gt;', '<br>')
        def term(m):
            t = m.group(1)
            if t not in self.terms:
                raise SystemExit(f'用語の定義（側注「用語」）がない: {t}')
            return f'<b class="term" data-anchor="term:{html.escape(t)}">{t}</b>'
        s = re.sub(r'&lt;&lt;(.+?)&gt;&gt;', term, s)
        s = re.sub(r'\{\{(.+?)\}\}', r'<span class="ans">\1</span>', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        s = re.sub(r'(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])', r'<span class="rp">\1</span>', s)
        s = re.sub(r'__(.+?)__([①-⑳])?', lambda m: f'<u>{m.group(1)}</u>' + (f'<sub>{m.group(2)}</sub>' if m.group(2) else ''), s)
        def exref(m):
            a, b = m.group(1), m.group(2)
            for k in (a, b):
                if k and k not in self.ex_no: raise SystemExit(f'例文 ID がない: {k}')
            return f'例文{self.ex_no[a]}' + (f'〜{self.ex_no[b]}' if b else '')
        s = re.sub(r'@(e\d+)(?:〜@(e\d+))?', exref, s)
        def secref(m):
            k = m.group(1)
            if k not in self.sec_no: raise SystemExit(f'節 ID がない: {k}')
            # 節への参照は常に完全解説book のページを指す（完全解説book を組むときは自分のページ）
            p = (self.pages or pages or {}).get(k)
            return f'<span class="pref" data-ref="{k}">→&nbsp;p.{p if p else "00"}</span>'
        s = re.sub(r'@(s\d+)', secref, s)
        s = s.replace('[＿]', '[<span class="blank"></span>]').replace('(＿)', '(<span class="blank"></span>)')
        s = s.replace('＿', '<span class="gap"></span>')
        s = s.replace('［ ］', '［&nbsp;］')
        return s

    # ---------- 共通 ----------
    def html_doc(self, title, css, cfg, blocks):
        base = (ROOT / 'tools' / 'book.css').read_text()
        js = (TOOLS / 'paginate.js').read_text()
        return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{base}\n{css}</style></head><body>
<div id="flow">{''.join(blocks)}</div><div id="pages"></div>
<script>window.__cfg = {cfg}; window.__cfg.nblocks = {len(blocks)};</script><script>{js}</script></body></html>'''

    def render(self, name, title, css, cfg, blocks_fn):
        """2回組み。blocks_fn(pages_self) がブロック列を返す。"""
        prev = None; lay = None
        for it in range(4):
            doc = self.html_doc(title, css, cfg, blocks_fn(prev or {}))
            hp = self.out / f'{name}.html'; hp.write_text(doc)
            pdf = self.out / f'{name}.pdf'
            r = subprocess.run(['node', str(TOOLS / 'render.js'), str(hp), str(pdf)], capture_output=True, text=True)
            if r.returncode not in (0,):
                print(r.stdout, r.stderr); raise SystemExit(f'{name}: 組版失敗')
            lay = json.loads((self.out / f'{name}.layout.json').read_text())
            if lay['errors']:
                print('\n'.join(lay['errors'])); raise SystemExit(f'{name}: ページ組みエラー')
            if prev is not None and lay['anchors'] == prev:
                return lay
            prev = lay['anchors']
        raise SystemExit(f'{name}: ページ割りが安定しない')


def main():
    bid = sys.argv[1] if len(sys.argv) > 1 else 'eg01'
    bk = Book(bid)
    from books import build_all
    build_all(bk)


if __name__ == '__main__':
    sys.path.insert(0, str(TOOLS))
    main()
