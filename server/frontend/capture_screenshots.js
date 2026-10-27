const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const OUTPUT_DIR = path.resolve(__dirname, "../../submission_evidence/screenshots");

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function run() {
  console.log("Launching Chrome at:", CHROME_PATH);
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: "new",
    defaultViewport: { width: 1280, height: 800 },
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // 1. admin_login.png
  console.log("Capturing admin_login.png...");
  await page.goto('http://127.0.0.1:8000/admin/', { waitUntil: 'networkidle2' });
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'admin_login.png') });

  // 2. admin_logout.png
  console.log("Capturing admin_logout.png...");
  await page.goto('http://127.0.0.1:8000/admin/logout/', { waitUntil: 'networkidle2' });
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'admin_logout.png') });

  // 3. get_dealers.png (logged out)
  console.log("Capturing get_dealers.png...");
  await page.goto('http://127.0.0.1:8000/dealers', { waitUntil: 'networkidle2' });
  await page.waitForSelector('table tbody tr', { timeout: 10000 });
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'get_dealers.png') });

  // 4. dealersbystate.png (Kansas filtered)
  console.log("Capturing dealersbystate.png...");
  await page.select('#state', 'Kansas');
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'dealersbystate.png') });

  // 5. Login as demouser
  console.log("Logging in as demouser...");
  await page.goto('http://127.0.0.1:8000/login', { waitUntil: 'networkidle2' });
  await page.waitForSelector('input[name="username"]');
  await page.type('input[name="username"]', 'demouser');
  await page.type('input[name="psw"]', 'Demopass123!');
  await page.click('input[type="submit"]');
  await new Promise(r => setTimeout(r, 1500));

  // 6. get_dealers_loggedin.png (shows username in header and Review Dealer column)
  console.log("Capturing get_dealers_loggedin.png...");
  await page.goto('http://127.0.0.1:8000/dealers', { waitUntil: 'networkidle2' });
  await page.waitForSelector('table tbody tr', { timeout: 10000 });
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'get_dealers_loggedin.png') });

  // 7. dealer_id_reviews.png (Dealer 8 with sentiment and reviews)
  console.log("Capturing dealer_id_reviews.png...");
  await page.goto('http://127.0.0.1:8000/dealer/8', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'dealer_id_reviews.png') });

  // 8. dealership_review_submission.png (Review submission form)
  console.log("Capturing dealership_review_submission.png...");
  await page.goto('http://127.0.0.1:8000/postreview/8', { waitUntil: 'networkidle2' });
  await page.waitForSelector('textarea#review', { timeout: 10000 });
  await page.type('textarea#review', 'Exceptional service and friendly staff in Topeka! Highly recommended.');
  await page.type('input[type="date"]', '2023-11-20');
  await page.select('#cars', 'Toyota Camry');
  await page.type('input[type="number"]', '2022');
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'dealership_review_submission.png') });

  // 9. added_review.png (Submit review and view updated reviews page)
  console.log("Submitting review and capturing added_review.png...");
  page.on('dialog', async dialog => {
    await dialog.accept();
  });
  await page.click('button.btn-primary');
  await new Promise(r => setTimeout(r, 3000));
  await page.goto('http://127.0.0.1:8000/dealer/8', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'added_review.png') });

  await browser.close();
  console.log("All screenshots captured successfully in:", OUTPUT_DIR);
}

run().catch(err => {
  console.error("Screenshot error:", err);
  process.exit(1);
});
