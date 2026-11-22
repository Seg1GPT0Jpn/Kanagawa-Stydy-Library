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
        # 執筆途中で組まない節も、参照の文字（第◯章）のために控えておく
        self.all_secs = {s['id']: c for c in self.data['chapters'] for s in c['sections']}
        # 執筆途中の本：中身（本文）のない節と、そうした節しかない章は組まない
        for ch in self.data['chapters']:
            ch['sections'] = [s for s in ch['sections'] if s.get('body')]
        self.data['chapters'] = [c for c in self.data['chapters'] if c['sections']]
        vols = self.data['book'].get('volumes') or []
        ids = {c['id'] for c in self.data['chapters']}
        for v in vols: v['chapters'] = [c for c in v['chapters'] if c in ids]
        self.data['book']['volumes'] = [v for v in vols if v['chapters']]
        self.data['problems'] = [p for p in self.data.get('problems', []) if any(p['sec'] == s['id'] for c in self.data['chapters'] for s in c['sections'])]
        self.out = ROOT / 'build' / bid
        self.out.mkdir(parents=True, exist_ok=True)
        self.ex_no = {}      # e001 -> 1
        self.sec_no = {}     # s01 -> 1
        self.sec_title = {}
        self.ch_of = {}
        self.terms = {}      # term -> yomi
        n_ex = 0; n_sec = 0
        for ci, ch in enumerate(self.data['chapters'], 1):
            unit = re.fullmatch(r'c(\d{2})', ch['id'])   # 英文法編：単元番号（c01 → 1）を章の番号に、節は「単元-節」
            ch['no'] = int(unit.group(1)) if unit else ci
            for s in ch['sections']:
                n_sec += 1
                su = re.fullmatch(r's(\d{2})(\d)', s['id'])
                s['no'] = f'{int(su.group(1))}-{su.group(2)}' if (unit and su) else n_sec
                self.sec_no[s['id']] = s['no']; self.sec_title[s['id']] = s['title']; self.ch_of[s['id']] = ch
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
        # 例題の番号（本冊と同じく、節の順に通しで数える）
        self.wk_nos = {}
        k = 0
        for ch in self.data['chapters']:
            for s in ch['sections']:
                nos = []
                for _ in s.get('worked') or []:
                    k += 1; nos.append(k)
                self.wk_nos[s['id']] = nos
        n = 0
        for p in self.problems:
            if p['set'] not in ('模試', '総合演習'):
                n += 1; p['no'] = n
            elif p['set'] == '総合演習':
                n += 0; p['no'] = 10000 + len([q for q in self.problems[:self.problems.index(p)] if q['set'] == '総合演習'])
        m = 0; k = {}
        for p in self.problems:
            if p['set'] == '模試':
                m += 1; p['no'] = m
                k[p['part']] = k.get(p['part'], 0) + 1
                p['label'] = f'第{p["part"]}問 ({k[p["part"]]})'
            elif p['set'] == '総合演習':
                k[('t', p['part'])] = k.get(('t', p['part']), 0) + 1
                p['label'] = f'総合{p["part"]}-{k[("t", p["part"])]}'
            else:
                p['label'] = f'問{p["no"]}'
        self.pages = {}      # 参照ページ表（完全解説book）: anchor -> page

    def merge_parts(self):
        """src/parts/*.yaml（章ごとの執筆ファイル）を節 ID で本体に差し込む。
        配布する本の唯一の情報源は、結合後に書き出す build/<id>/merged.yaml。"""
        chs = {c['id']: c for c in self.data['chapters']}
        for p in sorted((ROOT / 'src' / 'parts').glob(f'{self.bid}_*.yaml')):  # この本の執筆ファイルだけ
            part = yaml.safe_load(p.read_text())
            for pc in part.get('chapters', []):
                ch = chs[pc['id']]
                for k2, v2 in pc.items():
                    if k2 not in ('id', 'sections'): ch[k2] = v2   # 単元の導入・入口などの項目
                idx = {s['id']: i for i, s in enumerate(ch['sections'])}
                for ps in pc['sections']:
                    # 部分ファイルの節は、書いてある項目だけを本体の節に上書き・追加する（例題だけの追加にも使える）
                    ch['sections'][idx[ps['id']]].update(ps)
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
            starts_with_paren = bool(re.search(r'(^|<br>)\s*\([^()]*/', str(p.get('q', ''))))  # （ ）の語が文頭に来るときだけ
            if p['kind'] == '整序' and starts_with_paren and p['inst_eff'] and '小文字' not in p['inst_eff']:
                p['inst_eff'] = p['inst_eff'].rstrip() + '文頭に来る語も小文字で示してある。'
            if p['kind'] == '正誤':
                p['inst_eff'] = DEFAULT['正誤'] if '直しなさい' not in (p['inst_eff'] or '') else '下線部①〜④のうち、誤りをふくむものを1つ選び、正しい形に直しなさい。語を取り除くときは「削除」と書きなさい。'
        order = {s['id']: i for i, s in enumerate(s for c in self.data['chapters'] for s in c['sections'])}
        # 問題の属する単元（home）：ふつうは sec の章。確認テスト・前提は ID の単元番号（q02001 → c02）で決める
        #（確認テストには前の単元の節を問う問題が入るため）
        chids = [c['id'] for c in self.data['chapters']]
        for p in self.data.get('problems', []):
            home = next(c['id'] for c in self.data['chapters'] if any(s['id'] == p['sec'] for s in c['sections']))
            if p['set'] in ('確認テスト', '前提') and re.fullmatch(r'q\d{5}', str(p['id'])) and f'c{p["id"][1:3]}' in chids:
                home = f'c{p["id"][1:3]}'
            p['home'] = home
        rank = {'前提': 0, '節末': 1, '章末': 2, '確認テスト': 3}
        # 並び：単元ごとに 前提 → 節末（節の順・難易度の順）→ 章末 → 確認テスト。模試・総合演習は最後
        def key(p):
            ci = chids.index(p['home'])
            if p['set'] in ('模試', '総合演習'): return (999, p.get('part', 0), 0, 0)
            if p['set'] == '節末': return (ci, 1, order[p['sec']], p['lv'])
            return (ci, rank[p['set']], 0, 0)
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
            return '<span class="nw">' + f'例文{self.ex_no[a]}' + (f'〜{self.ex_no[b]}' if b else '') + '</span>'  # 例文番号の途中で改行しない
        s = re.sub(r'@(e\d+)(?:〜@(e\d+))?', exref, s)
        def secref(m):
            k = m.group(1)
            if k not in self.sec_no:
                if k in getattr(self, 'all_secs', {}):
                    c = self.all_secs[k]   # まだ組んでいない単元の節：章の番号で示す（執筆途中のときだけ起きる）
                    return f'<span class="pref" data-ref="later">→&nbsp;単元{int(c["id"][1:])}</span>'
                raise SystemExit(f'節 ID がない: {k}')
            # 節への参照は常に完全解説book のページを指す（完全解説book を組むときは自分のページ）
            p = (self.pages or pages or {}).get(k)
            return f'<span class="pref" data-ref="{k}">→&nbsp;p.{p if p else "00"}</span>'
        s = re.sub(r'@(s\d+)', secref, s)
        def qref(m):
            p = next((p for p in self.data.get('problems', []) if p['id'] == m.group(1)), None)
            if not p or 'label' not in p: raise SystemExit(f'問題 ID がない: {m.group(1)}')
            return p['label']
        s = re.sub(r'@(q\d+)', qref, s)
        s = s.replace('[＿]', '[<span class="blank"></span>]').replace('(＿)', '(<span class="blank"></span>)')
        s = s.replace('＿', '<span class="gap"></span>')
        s = s.replace('［ ］', '［&nbsp;］')
        # 下付きの数字（O₁ など）は本文の明朝に字がないので、普通の数字を小さく下げて組む
        s = re.sub('[₀-₉]', lambda m: f'<span class="subn">{ord(m.group(0)) - 0x2080}</span>', s)
        # ハイフンでつながった英単語（thank-you など）はハイフンの位置で改行しない
        s = re.sub(r'(?<![\w-])([A-Za-z]+(?:-[A-Za-z]+)+)(?![\w-])(?![^<]*>)', r'<span class="nw">\1</span>', s)
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
