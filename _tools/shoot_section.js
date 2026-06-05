const { chromium } = require('playwright');
const SRC = 'file:///C:/Users/raeda/Downloads/PM_Final_StudyBook/index.html';
const OUT = 'C:/Users/raeda/Downloads/PM_Final_StudyBook/_tools/';
const shots = [
  ['excel-walkthroughs', 'sec_intro'],
  ['wt-design', 'sec_design'],
  ['wt-funnel', 'sec_funnel'],
];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1180, height: 920 }, deviceScaleFactor: 1 });
  await page.goto(SRC, { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  for (const [id, name] of shots) {
    await page.evaluate((i) => document.getElementById(i).scrollIntoView({ block: 'start' }), id);
    await page.waitForTimeout(400);
    await page.screenshot({ path: OUT + name + '.png' });
    console.log('shot', name);
  }
  await browser.close();
  console.log('done');
})().catch(e => { console.error('ERR:', e.message); process.exit(1); });
