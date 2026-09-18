const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'carrossel.html'));
  await p.waitForTimeout(600);
  const s = await p.$$('.slide');
  for (let i = 0; i < s.length; i++) {
    const n = String(i + 1).padStart(2, '0');
    await s[i].screenshot({ path: path.join(__dirname, `slide-${n}.png`) });
    console.log(`slide-${n}.png`);
  }
  await b.close();
})();
