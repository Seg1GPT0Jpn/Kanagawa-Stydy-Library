#!/usr/bin/env python3
"""データ（本全体または章ごとの部分ファイル）の検査。
使い方: python3 validate.py <yaml> [<yaml> ...]   複数渡すと結合して検査する。
失敗（ERROR）が1つでもあれば終了コード 1。WARN は要確認の候補。
"""
import re, sys, yaml
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
KINDS = {'4択', '正誤', '整序', '補充', '和訳', '英作', '読解'}
SETS = {'節末', '章末', '模試'}
NOTE_KINDS = {'用語', '語注', '注意', '参照'}


def wordlists():
    """04_ai_tells.md の禁止語リスト（コードブロック）を読む。調査ファイルを唯一の情報源にする。"""
    t = (ROOT / 'research' / '04_ai_tells.md').read_text()
    t = t[t.index('## 自動検査用の禁止語リスト'):]
    lists = {}
    for m in re.finditer(r'### (.+?)\n.*?```\n(.*?)```', t, re.S):
        lists[m.group(1).strip()] = [w.strip() for w in m.group(2).splitlines() if w.strip()]
    return lists


def load(paths):
    """本体（eg01.yaml）があれば、ほかのファイルの節を節 ID で差し込んでから返す（組版と同じ結合）。"""
    paths = list(paths)
    mainp = [p for p in paths if Path(p).name == 'eg01.yaml']
    if mainp:
        d = yaml.safe_load(Path(mainp[0]).read_text())
        chapters = d.get('chapters', []) or []; problems = list(d.get('problems', []) or [])
        chs = {c['id']: c for c in chapters}
        for p in paths:
            if p in mainp: continue
            part = yaml.safe_load(Path(p).read_text())
            for pc in part.get('chapters', []) or []:
                ch = chs[pc['id']]
                if pc.get('lead'): ch['lead'] = pc['lead']
                idx = {s['id']: i for i, s in enumerate(ch['sections'])}
                for ps in pc['sections']: ch['sections'][idx[ps['id']]].update(ps)
            problems += part.get('problems', []) or []
        return chapters, problems
    chapters, problems = [], []
    for p in paths:
        d = yaml.safe_load(Path(p).read_text())
        chapters += d.get('chapters', []) or []
        problems += d.get('problems', []) or []
    return chapters, problems


def plain(s):
    s = re.sub(r'<[^>]+>', ' ', str(s))
    return re.sub(r'[{}*_\[\]<>@]', ' ', s)


def main(paths):
    err, warn = [], []
    chapters, problems = load(paths)
    full = yaml.safe_load((ROOT / 'src' / 'eg01.yaml').read_text())
    sec_ids = {s['id'] for c in full['chapters'] for s in c['sections']} | {s['id'] for c in chapters for s in c['sections']}
    ex_ids = Counter(); terms = set()
    en_texts, ja_texts = [], []
    for c in chapters:
        if c.get('lead'): ja_texts.append((c['id'], c['lead']))
        for s in c['sections']:
            for sm in s.get('summary', []) or []: ja_texts.append((s['id'], sm))
            for e in s.get('examples', []) or []:
                ex_ids[e['id']] += 1
                for g in e.get('gloss') or []:
                    if not isinstance(g, list) or len(g) != 2: err.append(f'{e["id"]}: 語注の形が不正（[英語, 意味] の2つ組でない。半角コンマで切れた可能性）: {g}')
                if set(e) - {'id', 'en', 'ja', 'gloss'}: err.append(f'{e["id"]}: 例文に余分な項目: {sorted(set(e) - {"id", "en", "ja", "gloss"})}')
                for k in ('id', 'en', 'ja'):
                    if not e.get(k): err.append(f'{s["id"]}: 例文に {k} がない: {e}')
                en_texts.append((e['id'], e.get('en', '')))
                ja_texts.append((e['id'], e.get('ja', '')))
            used_ex = set()
            for b in s.get('body', []) or []:
                keys = set(b) - {'notes', 'label'}
                if len(keys) != 1 or not keys <= {'h', 'p', 'ex', 'steps', 'table', 'check'}:
                    err.append(f'{s["id"]}: 本文ブロックの形が不正: {list(b)}')
                for n in b.get('notes', []) or []:
                    if n.get('kind') not in NOTE_KINDS: err.append(f'{s["id"]}: 側注の種類が不正: {n}')
                    extra = set(n) - {'kind', 'term', 'yomi', 'text', 'items'}
                    if extra: err.append(f'{s["id"]}: 側注に余分な項目（1行の {{…}} の中の半角コンマで文が切れた可能性）: {sorted(extra)}')
                    if n.get('kind') == '用語':
                        if not n.get('yomi') or not re.fullmatch(r'[ぁ-んー]+', n['yomi']): err.append(f'{s["id"]}: 用語 {n.get("term")} の yomi（ひらがな）がない')
                        if n.get('term') in terms: err.append(f'{s["id"]}: 用語の二重定義: {n.get("term")}')
                        terms.add(n.get('term'))
                if 'ex' in b: used_ex |= set(b['ex'])
                if 'p' in b: ja_texts.append((s['id'], b['p']))
                if 'check' in b:
                    for q in b['check']:
                        if not q.get('q') or not q.get('a'): err.append(f'{s["id"]}: 確認問題に q/a がない')
                        if set(q) - {'q', 'a'}: err.append(f'{s["id"]}: 確認問題に余分な項目（半角コンマで文が切れた可能性）: {sorted(set(q) - {"q", "a"})}')
            for k, w in enumerate(s.get('worked', []) or [], 1):
                wid = f'{s["id"]} 例題{k}'
                for key in ('q', 'steps', 'ans', 'point'):
                    if not w.get(key): err.append(f'{wid}: {key} がない')
                if len(w.get('steps') or []) < 2: err.append(f'{wid}: 解き方の手順が2つ未満')
                if set(w) - {'q', 'choices', 'steps', 'ans', 'point'}: err.append(f'{wid}: 余分な項目 {sorted(set(w) - {"q", "choices", "steps", "ans", "point"})}')
                if w.get('choices') and (len(w['choices']) != 4 or str(w.get('ans')) not in '1234'): err.append(f'{wid}: 選択肢が4つでない、または ans が 1〜4 でない')
                en_texts.append((wid, w.get('q', '')))
                ja_texts.append((wid, ' '.join(map(str, w.get('steps') or [])) + str(w.get('point', ''))))
            defined = {e['id'] for e in s.get('examples', []) or []}
            if defined - used_ex: err.append(f'{s["id"]}: 本文で使っていない例文: {sorted(defined - used_ex)}')
            if used_ex - defined: err.append(f'{s["id"]}: 定義のない例文: {sorted(used_ex - defined)}')
            if s.get('body') and not s.get('summary'): err.append(f'{s["id"]}: summary（要点まとめ）がない')
            for sm in s.get('summary', []) or []:
                if '{{' not in sm: warn.append(f'{s["id"]}: 要点に赤シートの穴 {{{{}}}} がない: {sm[:30]}')
    for k, v in ex_ids.items():
        if v > 1: err.append(f'例文 ID の重複: {k}')
    # 正解の位置の偏り（選択式の4択・読解）：各番号が全体の 15〜35% に入るか。正誤は ④ の少なさを警告
    sel = [str(p.get('ans')) for p in problems if p.get('kind') in ('4択', '読解') and p.get('choices') and str(p.get('ans')) in '1234']
    if len(sel) >= 20:
        cnt = Counter(sel)
        for k in '1234':
            r = cnt[k] / len(sel)
            if not 0.15 <= r <= 0.35: err.append(f'選択式の正解の位置が偏っている：{k} が {cnt[k]}/{len(sel)}（{r:.0%}）。tools/rebalance.py で直す')
    sei = [str(p.get('ans')) for p in problems if p.get('kind') == '正誤']
    if len(sei) >= 20:
        cnt = Counter(sei)
        for k in '1234':
            if cnt[k] / len(sei) < 0.12: warn.append(f'正誤の正解の位置が偏っている：{k} が {cnt[k]}/{len(sei)}')
    # 問題文が完全解説の例文・確認問題とほぼ同じでないか（答えを本で見たことになる）
    import difflib
    def simp(t):
        t = re.sub(r'<[^>]+>|\{\{|\}\}|[*_\[\]＿()（）]|@\w+', ' ', str(t)).lower()
        return ' '.join(re.findall(r"[a-z']+", t))
    refs = [(e['id'], simp(e['en'])) for c in chapters for s in c['sections'] for e in s.get('examples', []) or []]
    refs += [(s['id'] + ' 確認', simp(q['q'])) for c in chapters for s in c['sections'] for b in s.get('body', []) or [] for q in (b.get('check') or [])]
    refs += [(f'{s["id"]} 例題', simp(w['q'])) for c in chapters for s in c['sections'] for w in (s.get('worked') or [])]
    refs = [(i, t) for i, t in refs if len(t.split()) >= 6]
    for p in problems:
        sents = re.split(r'(?<=[.?!])\s+', re.sub(r'<br>.*', '', str(p.get('q', '')))) if p.get('kind') != '読解' else []
        for sent in sents:
            st = simp(sent)
            if len(st.split()) < 6: continue
            for i, t in refs:
                r = difflib.SequenceMatcher(None, st, t).ratio()
                if r >= 0.8:
                    warn.append(f'{p.get("id")}: 問題文が {i} とほぼ同じ（一致度 {r:.0%}）')
                    break
    # YAML の真偽値化け（on/off/yes/no などを引用符なしで書くと true/false になる）
    def walk(x, path):
        if isinstance(x, bool): err.append(f'{path}: 真偽値 {x}（on/off/yes/no を引用符で囲んでいない可能性）')
        elif isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, bool): err.append(f'{path}: キーが真偽値 {k}')
                walk(v, f'{path}.{k}')
        elif isinstance(x, list):
            for i, v in enumerate(x): walk(v, f'{path}[{i}]')
    for c in chapters: walk(c, c.get('id', '?'))
    for p in problems: walk(p, p.get('id', '?'))
    # 参照
    alltext = yaml.safe_dump({'c': chapters, 'p': problems}, allow_unicode=True)
    for m in re.finditer(r'@(s\d+)', alltext):
        if m.group(1) not in sec_ids: err.append(f'存在しない節への参照: @{m.group(1)}')
    full_ex = {e['id'] for c in full['chapters'] for s in c['sections'] for e in s.get('examples', []) or []} | set(ex_ids)
    allq = {p.get('id') for p in problems} | {p.get('id') for p in (full.get('problems') or [])}
    for m in re.finditer(r'@(q\d+)', alltext):
        if m.group(1) not in allq: err.append(f'存在しない問題への参照: @{m.group(1)}')
    for m in re.finditer(r'@(e\d+)', alltext):
        if m.group(1) not in full_ex: err.append(f'存在しない例文への参照: @{m.group(1)}')
    if not any(Path(p).resolve() == (ROOT / 'src' / 'eg01.yaml').resolve() for p in paths):
        base_terms = {n['term'] for c in full['chapters'] for s in c['sections'] for b in s.get('body', []) or [] for n in (b.get('notes') or []) if n.get('kind') == '用語'}
        for t in base_terms & terms: err.append(f'用語の二重定義（本体と部分ファイル）: {t}')
    full_terms = {n['term'] for c in full['chapters'] for s in c['sections'] for b in s.get('body', []) or [] for n in (b.get('notes') or []) if n.get('kind') == '用語'} | terms
    for m in re.finditer(r'<<(.+?)>>', alltext):
        if m.group(1) not in full_terms: err.append(f'用語の定義（側注「用語」）がない: <<{m.group(1)}>>')
    # 問題
    qids = Counter(p.get('id') for p in problems)
    for k, v in qids.items():
        if v > 1: err.append(f'問題 ID の重複: {k}')
    for p in problems:
        pid = p.get('id', '?')
        for k in ('id', 'sec', 'set', 'lv', 'kind', 'min', 'q', 'ans', 'why', 'trap'):
            if p.get(k) in (None, ''): err.append(f'{pid}: {k} がない')
        if p.get('kind') not in KINDS: err.append(f'{pid}: kind が不正: {p.get("kind")}')
        extra = set(p) - {'id', 'sec', 'set', 'lv', 'kind', 'min', 'inst', 'q', 'choices', 'words', 'ans', 'alt', 'why', 'trap', 'ref', 'passage', 'part', 'pts', 'fix'}
        if extra: err.append(f'{pid}: 問題に余分な項目（半角コンマで文が切れた可能性）: {sorted(extra)}')
        if p.get('set') not in SETS: err.append(f'{pid}: set が不正: {p.get("set")}')
        if p.get('lv') not in (1, 2, 3): err.append(f'{pid}: lv が不正')
        if p.get('sec') not in sec_ids: err.append(f'{pid}: sec が存在しない: {p.get("sec")}')
        if p.get('kind') == '4択':
            ch = p.get('choices') or []
            if len(ch) != 4: err.append(f'{pid}: 4択の選択肢が4つでない')
            if str(p.get('ans')) not in ('1', '2', '3', '4'): err.append(f'{pid}: 4択の ans が 1〜4 でない')
            if len(set(ch)) != len(ch): err.append(f'{pid}: 選択肢が重複')
            if '(＿)' not in p.get('q', '') and '＿' not in p.get('q', ''): err.append(f'{pid}: 4択の問題文に空所 ＿ がない')
        if p.get('kind') == '読解' and p.get('choices'):
            if len(p['choices']) != 4: err.append(f'{pid}: 読解の選択肢が4つでない')
            if str(p.get('ans')) not in ('1', '2', '3', '4'): err.append(f'{pid}: 読解の ans が 1〜4 でない')
        if p.get('kind') in ('和訳', '英作', '補充') and not p.get('why'): err.append(f'{pid}: 採点の目安（why）がない')
        if p.get('kind') == '正誤':
            marks = re.findall(r'__.+?__([①-⑳])', p.get('q', ''))
            if len(marks) != 4: err.append(f'{pid}: 正誤の下線部が4つでない（__…__① の形）')
            if str(p.get('ans')) not in ('1', '2', '3', '4'): err.append(f'{pid}: 正誤の ans が 1〜4 でない')
        if p.get('kind') == '整序':
            words = p.get('words') or []
            if not words: err.append(f'{pid}: 整序に words がない')
            ans = str(p.get('ans', ''))
            toks = re.findall(r"[A-Za-z][A-Za-z'’\-]*", ans)
            # 問題文に出ている語（括弧の外）を答えから除き、残りが words と一致するか
            q = re.sub(r'<br>', ' ', p.get('q', ''))
            outside = re.sub(r'\(([^()]*/[^()]*)\)', ' ', q)
            outside_toks = re.findall(r"[A-Za-z][A-Za-z'’\-]*", outside)
            rest = Counter(t.lower() for t in toks)
            for t in outside_toks:
                if rest[t.lower()] > 0: rest[t.lower()] -= 1
            want = Counter(w.lower() for w in words)
            rest = +rest
            if rest != want:
                err.append(f'{pid}: 整序の語が答えと一致しない: 与えた {sorted(want.elements())} / 答えの残り {sorted(rest.elements())}')
            inparen = re.search(r'\(([^()]*/[^()]*)\)', q)
            if inparen:
                shown = Counter(w.strip().lower() for w in inparen.group(1).split('/'))
                if shown != want: err.append(f'{pid}: 問題文の（ / ）内の語と words が一致しない')
        for alt in p.get('alt') or []:
            if not str(alt).strip(): err.append(f'{pid}: 空の別解')
        en_texts.append((pid, p.get('q', '')))
        ja_texts.append((pid, (p.get('why', '') or '') + (p.get('trap', '') or '')))
    mock = [p for p in problems if p.get('set') == '模試']
    if mock:
        for p in mock:
            if p.get('part') not in (1, 2, 3, 4, 5): err.append(f'{p.get("id")}: 模試の part が不正')
            if not p.get('pts'): err.append(f'{p.get("id")}: 模試の pts がない')
        if sum(p.get('pts', 0) or 0 for p in mock) != 100: err.append(f'模試の配点合計が {sum(p.get("pts", 0) or 0 for p in mock)}（100 でない）')
    # 禁止語
    wl = wordlists()
    for key in ('英語・強（単語。活用形を含む）', '英語・強（句）'):
        for w in wl.get(key, []):
            pat = re.compile(r'\b' + re.escape(w) + r'\b', re.I)
            for i, t in en_texts:
                if pat.search(plain(t)): err.append(f'{i}: AI多用語（強）「{w}」')
    for w in wl.get('英語・注意（単語）', []):
        pat = re.compile(r'\b' + re.escape(w) + r'\b', re.I)
        n = [i for i, t in en_texts if pat.search(plain(t))]
        if n: warn.append(f'AI多用語（注意）「{w}」: {n}')
    for w in wl.get('英語・定番名（物語系AIの名前。頻度で判定）', []):
        for i, t in en_texts:
            if re.search(r'\b' + re.escape(w) + r'\b', t): err.append(f'{i}: 定番名「{w}」')
    for w in wl.get('日本語・強', []):
        for i, t in ja_texts:
            if w in str(t): err.append(f'{i}: 日本語の避ける表現「{w}」')
    for w in wl.get('日本語・注意（密度で判定）', []):
        n = [i for i, t in ja_texts if w in str(t)]
        if len(n) >= 3: warn.append(f'日本語の注意表現「{w}」が {len(n)} か所: {n[:6]}')
    for i, t in ja_texts + en_texts:
        if re.search(r'(?<![@\w])s\d{2}\b', str(t)): err.append(f'{i}: 節の内部 ID が本文に残っている: {re.findall(r"(?<![@\w])s\d{2}", str(t))}（@s01 か「第1節」と書く）')
        if re.search(r'(?<![@\w])[qe]\d{3,4}\b', str(t)): err.append(f'{i}: 内部の ID が本文に残っている: {re.findall(r"(?<![@\w])[qe]\d{3,4}", str(t))}')
    for i, t in ja_texts:
        if re.search(r'[！!]', str(t)) and not re.search(r'[A-Za-z]!', str(t)): warn.append(f'{i}: 解説文に「！」')
        if '—' in str(t) or '――' in str(t): err.append(f'{i}: 長いダッシュ')
        if len(re.findall(r'\*\*', str(t))) > 2: warn.append(f'{i}: 太字が1段落に2か所以上')
    # 人名の偏り
    names = Counter()
    for i, t in en_texts:
        for m in re.finditer(r'\b(?:Mr\.|Ms\.|Mrs\.|Dr\.)?\s?([A-Z][a-z]+)\b', plain(t)):
            pass
    for e in warn: print('WARN ', e)
    for e in err: print('ERROR', e)
    print(f'例文 {sum(ex_ids.values())}、問題 {len(problems)}、ERROR {len(err)}、WARN {len(warn)}')
    return 1 if err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
