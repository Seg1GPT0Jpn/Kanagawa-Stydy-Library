// ページ組み（Chromium 内で実行）。
// #flow の中の .blk を順に測り、.page に詰める。側注 (.sn) は参照元ブロックの上端から小口側の欄に置く。
// 完了すると window.__layout に {pages, anchors, errors} を入れる。
window.__paginate = function () {
  const MM = 96 / 25.4;
  const C = window.__cfg; // {pw, ph, top, bottom, inner, outer, mainW, gap, sideW, startPage, hashiraLeft, crossRefs}
  const flow = document.getElementById('flow');
  const out = document.getElementById('pages');
  const errors = [];
  let pageNo = C.startPage - 1;
  let page = null, mainEl = null, sideEl = null, y = 0, sideY = 0;
  const H = (C.ph - C.top - C.bottom) * MM;
  let curChapter = '', curSection = '';
  const pendingNotes = [];  // 側注欄に入りきらず次のページへ送る側注

  function newPage(kind) {
    pageNo++;
    const odd = pageNo % 2 === 1; // 奇数＝右ページ。ノドは左
    page = document.createElement('div');
    page.className = 'page ' + (odd ? 'recto' : 'verso') + (kind ? ' ' + kind : '');
    page.dataset.no = pageNo;
    const left = odd ? C.inner : C.outer;
    const body = document.createElement('div');
    body.className = 'body';
    Object.assign(body.style, { left: left + 'mm', top: C.top + 'mm', width: (C.pw - C.inner - C.outer) + 'mm', height: (C.ph - C.top - C.bottom) + 'mm' });
    mainEl = document.createElement('div'); mainEl.className = 'maincol';
    sideEl = document.createElement('div'); sideEl.className = 'sidecol';
    const mainLeft = (C.sideW && !odd) ? C.sideW + C.gap : 0;
    const sideLeft = odd ? C.mainW + C.gap : 0;
    Object.assign(mainEl.style, { left: mainLeft + 'mm', width: (C.sideW ? C.mainW : (C.pw - C.inner - C.outer)) + 'mm' });
    Object.assign(sideEl.style, { left: sideLeft + 'mm', width: C.sideW + 'mm' });
    body.appendChild(mainEl); if (C.sideW) body.appendChild(sideEl);
    page.appendChild(body);
    out.appendChild(page);
    y = 0; sideY = 0;
    // 前のページから送られた側注を、このページの側注欄の頭に置く
    while (pendingNotes.length && C.sideW) {
      const n = pendingNotes.shift(); const nh1 = measure(n, smeas);
      n.style.position = 'absolute'; n.style.top = (sideY / MM) + 'mm'; n.style.left = 0; n.style.right = 0; sideEl.appendChild(n); sideY += nh1;
    }
    return page;
  }
  function finishPage() {
    if (!page || page.dataset.done) return;
    page.dataset.done = 1;
    if (page.classList.contains('nohead')) return;
    const h = document.createElement('div'); h.className = 'hashira';
    h.innerHTML = (pageNo % 2 === 0 ? (page.dataset.ch || curChapter) : (page.dataset.sec || curSection));
    const n = document.createElement('div'); n.className = 'nombre'; n.textContent = pageNo;
    const odd = pageNo % 2 === 1;
    h.style.top = (C.top - 9) + 'mm'; n.style.bottom = (C.bottom - 11) + 'mm';
    for (const el of [h, n]) { el.style[odd ? 'right' : 'left'] = C.outer + 'mm'; el.style.textAlign = odd ? 'right' : 'left'; page.appendChild(el); }
  }
  function outerH(el) { const cs = getComputedStyle(el); return el.getBoundingClientRect().height + parseFloat(cs.marginTop) + parseFloat(cs.marginBottom); }

  // 測定用の箱
  const meas = document.createElement('div'); meas.className = 'maincol measure';
  meas.style.width = (C.sideW ? C.mainW : (C.pw - C.inner - C.outer)) + 'mm';
  const smeas = document.createElement('div'); smeas.className = 'sidecol measure'; smeas.style.width = C.sideW + 'mm';
  const wmeas = document.createElement('div'); wmeas.className = 'maincol measure'; wmeas.style.width = (C.pw - C.inner - C.outer) + 'mm';
  document.body.appendChild(meas); document.body.appendChild(smeas); document.body.appendChild(wmeas);
  function measure(el, box) { box.appendChild(el); const h = outerH(el); box.removeChild(el); return h; }

  const blocks = Array.from(flow.children);
  if (blocks.length !== C.nblocks) errors.push(`ブロック数の不一致: 生成 ${C.nblocks}、配置対象 ${blocks.length}（HTML の入れ子の誤り）`);
  if (flow.parentElement !== document.body) errors.push('#flow の位置が不正');
  newPage(blocks[0] && blocks[0].dataset.pagekind);
  for (let i = 0; i < blocks.length; i++) {
    const b = blocks[i];
    if (b.dataset.chapter !== undefined) curChapter = b.dataset.chapter;
    if (b.dataset.section !== undefined) curSection = b.dataset.section;
    if (b.classList.contains('fullpage')) {
      // 表紙・白ページ・奥付など：1ページをそのまま使う
      if (y > 0 || page.classList.contains('used')) { finishPage(); newPage(); }
      if (b.dataset.pagekind) page.className += ' ' + b.dataset.pagekind;
      page.appendChild(b); page.classList.add('used');
      finishPage(); y = H + 1; // 次のブロックは新しいページへ
      continue;
    }
    const notes = Array.from(b.querySelectorAll(':scope > .sn'));
    notes.forEach(n => n.remove());
    const forceNew = b.classList.contains('newpage') || b.classList.contains('recto-start');
    if (forceNew && (y > 0 || page.classList.contains('used'))) {
      finishPage(); newPage(b.dataset.pagekind);
      if (b.classList.contains('recto-start') && pageNo % 2 === 0) { page.classList.add('blank', 'nohead'); newPage(b.dataset.pagekind); }
    } else if (forceNew && b.dataset.pagekind) { page.className += ' ' + b.dataset.pagekind; }
    const isWide = b.classList.contains('wide');  // 側注欄まで使う全幅のかたまり（問題など）
    const mbox = b2 => (b2.classList.contains('wide') ? wmeas : meas);
    if (isWide) y = Math.max(y, sideY);  // 側注の下から置く
    let h = measure(b, mbox(b));
    // 見出しは次のブロックと一緒に送る
    let need = h;
    if (b.classList.contains('keepnext')) {
      // 見出し・指示文は、後ろに続く keepnext の列と、その次の本体のかたまりと一緒に送る
      let j = i + 1;
      while (blocks[j]) {
        const c = blocks[j].cloneNode(true); c.querySelectorAll('.sn').forEach(n => n.remove());
        const hj = measure(c, mbox(blocks[j]));
        if (need + hj <= H) need += hj; else break;
        if (!blocks[j].classList.contains('keepnext')) break;
        j++;
      }
    }
    let nh = notes.reduce((s, n) => s + measure(n, smeas), 0);
    const startY = y; // 上端の余白は先頭では詰める
    // 側注が入りきらないときは本文ごと送る。ただし側注がページの6割を超えるほど多いときは送らず、側注を次のページへ続ける
    if (y + need > H + 0.5 || (nh <= H * 0.6 && Math.max(sideY, y) + nh > H + 0.5)) {
      if (y === 0 && !page.classList.contains('used')) { errors.push(`p${pageNo}: ブロックが1ページに収まらない: ${b.textContent.slice(0, 40)}`); }
      else {
        // ページの最後に残る見出し・指示文（keepnext）は、送るかたまりと一緒に次のページへ移す
        const carry = [];
        const placedHere = () => Array.from(page.querySelectorAll('.maincol > .blk, .body > .blk')).sort((a, c) => parseFloat(a.style.top) - parseFloat(c.style.top));
        let lst = placedHere(); let last = lst[lst.length - 1];
        while (last && last.classList.contains('keepnext')) { carry.unshift(last); last.remove(); lst = placedHere(); last = lst[lst.length - 1]; }
        finishPage(); newPage();
        for (const c of carry) {
          if (y === 0) c.classList.add('first'); else c.classList.remove('first');
          c.style.top = (y / MM) + 'mm';
          if (c.classList.contains('wide')) page.querySelector('.body').appendChild(c); else mainEl.appendChild(c);
          y += outerH(c);
          if (!page.dataset.ch) { page.dataset.ch = curChapter; page.dataset.sec = c.dataset.section || curSection; }
        }
        if (carry.length) page.classList.add('used');
      }
    }
    if (y === 0) b.classList.add('first'); else b.classList.remove('first');
    if (isWide) y = Math.max(y, sideY);
    h = measure(b, mbox(b));
    b.style.top = (y / MM) + 'mm';
    if (isWide) {
      const body = page.querySelector('.body');
      body.appendChild(b); b.style.position = 'absolute'; b.style.left = '0'; b.style.width = (C.pw - C.inner - C.outer) + 'mm';
    } else { mainEl.appendChild(b); b.style.position = 'absolute'; b.style.left = '0'; b.style.right = '0'; }
    if (!page.dataset.ch) { page.dataset.ch = curChapter; page.dataset.sec = curSection; }
    page.classList.add('used');
    let sy = Math.max(sideY, y);
    for (const n of notes) {
      const nh1 = measure(n, smeas);
      if (sy + nh1 > H + 0.5 && sy > 0) { pendingNotes.push(n); continue; }   // 下端に届いたら次のページの側注欄へ送る
      n.style.position = 'absolute'; n.style.top = (sy / MM) + 'mm'; n.style.left = 0; n.style.right = 0; sideEl.appendChild(n); sy += nh1;
    }
    sideY = sy;
    if (sy > H + 0.5) errors.push(`p${pageNo}: 側注が下端を越えた ${((sy - H) / MM).toFixed(1)}mm: ${b.textContent.slice(0, 30)}`);
    y += h;
    if (isWide) sideY = Math.max(sideY, y);
    if (y > H + 0.5) errors.push(`p${pageNo}: はみ出し ${(y / MM - H / MM).toFixed(1)}mm: ${b.textContent.slice(0, 40)}`);
  }
  finishPage();
  if (pendingNotes.length) errors.push(`最後のページで置けなかった側注が ${pendingNotes.length} 個ある`);
  meas.remove(); smeas.remove(); wmeas.remove();

  // 参照先のページ
  const anchors = {};
  document.querySelectorAll('#pages .page').forEach(pg => {
    pg.querySelectorAll('[data-anchor]').forEach(a => { for (const k of a.dataset.anchor.split(' ')) if (!(k in anchors)) anchors[k] = +pg.dataset.no; });
  });
  window.__anchorsLocal = anchors;
  // ページの最後に見出し・指示文だけが残っていないか
  document.querySelectorAll('#pages .page').forEach(pg => {
    const bl = Array.from(pg.querySelectorAll('.maincol > .blk, .body > .blk')).sort((a, c) => parseFloat(a.style.top) - parseFloat(c.style.top));
    const last = bl[bl.length - 1];
    if (last && last.classList.contains('keepnext')) errors.push(`p${pg.dataset.no}: ページの最後に見出し・指示文だけが残っている: ${last.textContent.slice(0, 30)}`);
  });
  const placed = document.querySelectorAll('#pages .blk').length;
  if (placed !== C.nblocks) errors.push(`配置されたブロック数 ${placed} が生成数 ${C.nblocks} と違う`);
  window.__layout = { pages: pageNo, anchors, errors };
};
