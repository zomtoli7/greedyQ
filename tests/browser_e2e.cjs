const { chromium } = require("playwright");
const fs = require("fs");

const base = process.argv[2];
const executablePath = process.argv[3];
const fail = (condition, message) => { if (!condition) throw new Error(message); };

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath });
  const responsive = [];
  for (const width of [320, 390, 768, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.goto(`${base}/preview.html`, { waitUntil: "domcontentloaded" });
    await page.selectOption("#page", "advanced_controls");
    await page.evaluate(() => { mobile.state.page = "advanced_controls"; mobile.render(); });
    const check = await page.evaluate(() => {
      const root = document.querySelector("#mobile");
      return {
        client: root.clientWidth, scroll: root.scrollWidth,
        nps: root.querySelectorAll(".gq-nps-scale input").length,
        desktopRank: document.querySelectorAll("#desktop [data-rank-item]").length,
      };
    });
    fail(check.scroll <= check.client + 1, `mobile overflow at ${width}px`);
    fail(check.nps === 11, `NPS control incomplete at ${width}px`);
    fail(check.desktopRank === 3, `desktop control missing at ${width}px`);
    responsive.push(check);
    await page.close();
  }

  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(`${base}/preview.html`);
  await page.selectOption("#page", "controls");
  const baseDesktop = page.locator("#desktop");
  await baseDesktop.locator('input[name="conditional_choice"][value="yes"]').check();
  fail(await baseDesktop.locator('[data-q="conditional_text"]').isVisible(), "conditional field did not appear");
  await baseDesktop.locator('input[name="conditional_choice"][value="no"]').check();
  fail(!(await baseDesktop.locator('[data-q="conditional_text"]').isVisible()), "conditional field did not clear");
  await page.selectOption("#page", "advanced_controls");
  const desktop = page.locator("#desktop");
  for (const [index, rank] of ["1", "2", "3"].entries()) await desktop.locator("[data-rank-item]").nth(index).selectOption(rank);
  await desktop.locator('.gq-nps-scale input[value="9"]').check();
  for (const [index, value] of ["30", "30", "40"].entries()) await desktop.locator("[data-constant-item]").nth(index).fill(value);
  for (const radio of await desktop.locator(".gq-side-by-side input[type=radio]").all()) if ((await radio.getAttribute("value")) === "2") await radio.check();
  for (const select of await desktop.locator("[data-pgr-group]").all()) await select.selectOption("essential");
  for (const [index, input] of (await desktop.locator("[data-pgr-rank]").all()).entries()) await input.fill(String(index + 1));
  const drills = await desktop.locator("[data-drill-level]").all();
  await drills[0].selectOption({ label: "Asia" }); await drills[1].selectOption({ label: "Korea" }); await drills[2].selectOption({ label: "Seoul" });
  await desktop.getByRole("button", { name: "Try navigation controls" }).click();
  const answers = await page.evaluate(() => desktop.state.answers);
  for (const id of ["rank_example", "sbs_example", "nps_example", "timing_example", "sum_example", "group_rank_example", "drill_example"]) fail(Object.hasOwn(answers, id), `missing ${id}`);
  const accessibility = await desktop.evaluate(root => ({
    unlabeled: [...root.querySelectorAll("input,select,textarea")].filter(control => !control.getAttribute("aria-label") && !control.closest("label")).length,
    duplicateIds: [...root.querySelectorAll("[id]")].map(node => node.id).filter((id, index, all) => all.indexOf(id) !== index).length,
  }));
  fail(accessibility.unlabeled === 0, "unlabeled form controls found");
  fail(accessibility.duplicateIds === 0, "duplicate element IDs found");
  await page.reload();
  fail(await page.locator("#desktop").getByText("Navigation controls").isVisible(), "preview session session did not resume after refresh");
  await page.selectOption("#page", "complete");
  fail(await page.locator("#desktop .gq-actions button").count() === 0, "terminal page exposes navigation");

  const dashboard = await browser.newPage();
  const payload = { generated_at: new Date().toISOString(), sessions: [{ id: "s1", created_at: new Date().toISOString(), terminal_at: null, lifecycle_state: "active", respondent_source: "direct", is_test: true, current_page: "advanced_controls" }], assignments: [], answers: [
    { session_id: "s1", question_id: "sbs_example", value: { current: { clear: 2 }, proposed: { clear: 3 } } },
    { session_id: "s1", question_id: "rank_example", value: { ease: 1, speed: 2, flexibility: 3 } },
    { session_id: "s1", question_id: "sum_example", value: { design: 30, testing: 30, documentation: 40 } },
    { session_id: "s1", question_id: "drill_example", value: ["Asia", "Korea", "Seoul"] },
  ] };
  await dashboard.route("**/api/results**", route => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(payload) }));
  await dashboard.goto(`${base}/results.html`);
  await dashboard.waitForSelector("#dictionary tr");
  const [download] = await Promise.all([dashboard.waitForEvent("download"), dashboard.click("#download")]);
  const csv = fs.readFileSync(await download.path(), "utf8");
  for (const column of ["sbs_example.current.clear", "rank_example.ease", "sum_example.design", "drill_example.level_3"]) fail(csv.includes(column), `missing CSV column ${column}`);
  const result = { responsive, structuredAnswers: Object.keys(answers).length, dictionaryRows: await dashboard.locator("#dictionary tr").count() };
  console.log(JSON.stringify(result));
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
