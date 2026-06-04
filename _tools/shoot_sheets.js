const { chromium } = require('playwright');

const OUT = 'C:/Users/raeda/Downloads/PM_Final_StudyBook/slides/excel/';
const SRC = 'file:///C:/Users/raeda/Downloads/PM_Final_StudyBook/_tools/excel_sheets.html';
const sheets = [
  ['sheet-pricing', 'pricing_games'],
  ['sheet-funnel', 'base_exclusion_funnel'],
  ['sheet-design', 'design_your_own_products'],
  ['sheet-data', 'funnel_data_sample'],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 1.3 });
  await page.goto(SRC, { waitUntil: 'networkidle' });
  await page.waitForTimeout(400); // let webfont settle
  for (const [id, fname] of sheets) {
    const el = page.locator('#' + id);
    await el.screenshot({ path: OUT + fname + '.png' });
    console.log('shot', fname);
  }
  await browser.close();
  console.log('done');
})().catch(e => { console.error('ERR:', e.message); process.exit(1); });
