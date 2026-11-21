// HTML を Chromium で組んで PDF にする。使い方: node render.js in.html out.pdf
// ページ組み (window.__paginate) があれば書体の読み込み後に実行し、結果を <out>.layout.json に書く。
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('pageerror', e => { console.error('JS error:', e.message); process.exitCode = 3; });
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const hasPag = await page.evaluate(() => typeof window.__paginate === 'function');
  let layout = null;
  if (hasPag) {
    layout = await page.evaluate(() => { window.__paginate(); return window.__layout; });
    const fonts = await page.evaluate(() => Array.from(document.fonts).filter(f => f.status !== 'loaded' && f.status !== 'unloaded').map(f => f.family + ':' + f.status));
    if (fonts.length) layout.errors.push('書体の読み込み失敗: ' + fonts.join(','));
    fs.writeFileSync(out.replace(/\.pdf$/, '.layout.json'), JSON.stringify(layout));
  }
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  await browser.close();
})();
