// HTML を Chromium で PDF にする。使い方: node render.js in.html out.pdf
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  // ページ内のはみ出しを検出（.page の中で .overflow-check が下端を越えたら失敗）
  const over = await page.evaluate(() => {
    const bad = [];
    document.querySelectorAll('.page').forEach((pg, i) => {
      const body = pg.querySelector('.body') || pg;
      const lim = body.getBoundingClientRect().bottom + 0.5;
      body.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.height > 0 && r.bottom > lim) bad.push(`p${i + 1}: <${el.tagName.toLowerCase()} class="${el.className}"> ${(el.textContent || '').slice(0, 30)}`);
      });
    });
    return bad;
  });
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  await browser.close();
  if (over.length) { console.error('OVERFLOW\n' + over.slice(0, 20).join('\n')); process.exit(2); }
})();
