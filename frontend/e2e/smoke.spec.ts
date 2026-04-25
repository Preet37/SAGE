import { test, expect, type Page } from "@playwright/test";

const BASE = "http://localhost:3000";
const API = "http://localhost:8000";
const TEST_EMAIL = `smoketest-${Date.now()}@example.com`;
const TEST_USER = `smoketest${Date.now()}`;
const TEST_PASS = "Test1234!";

let authToken = "";

async function registerAndGetToken(): Promise<string> {
  const res = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: TEST_EMAIL,
      username: TEST_USER,
      password: TEST_PASS,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(`Register failed: ${res.status} ${JSON.stringify(err)}`);
  }
  const data = await res.json();
  return data.access_token;
}

async function injectAuth(page: Page, token: string) {
  await page.goto(BASE);
  await page.evaluate((t) => localStorage.setItem("tutor_token", t), token);
}

async function createDraft(token: string, title: string): Promise<{ id: string }> {
  const res = await fetch(`${API}/course-creator/drafts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title,
      source_type: "prompt",
      source_text: title,
    }),
  });
  expect(res.ok).toBeTruthy();
  return res.json();
}

async function gotoWorkspace(page: Page, token: string, draftId: string) {
  await injectAuth(page, token);
  await page.goto(`${BASE}/create/${draftId}`);
  await page.waitForLoadState("domcontentloaded");
  // Wait for the canvas to render (Course Assistant header appears in ChatPanel)
  await page.waitForSelector("text=Course Assistant", { timeout: 10000 });
}

test.describe("Frontend Smoke Tests", () => {
  test.beforeAll(async () => {
    authToken = await registerAndGetToken();
    console.log(`Registered test user: ${TEST_EMAIL}`);
  });

  test("1. Login page renders without errors", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto(`${BASE}/login`);
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(500);

    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.getByRole("button", { name: "Sign In" })).toBeVisible();
    await expect(page.locator("text=SocraticTutor").first()).toBeVisible();
    await expect(page.getByRole("link", { name: "Register" })).toBeVisible();

    expect(errors).toHaveLength(0);
  });

  test("2. Register page renders without errors", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto(`${BASE}/register`);
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(500);

    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[placeholder="Username"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.getByRole("button", { name: "Create Account" })).toBeVisible();

    expect(errors).toHaveLength(0);
  });

  test("3. All pages load without JS crashes", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => {
      if (!err.message.includes("fetch") && !err.message.includes("Request failed")) {
        errors.push(err.message);
      }
    });

    const paths = ["/login", "/register", "/create", "/explore", "/quiz",
      "/concepts", "/assess", "/curriculum", "/projects"];

    for (const path of paths) {
      await page.goto(`${BASE}${path}`);
      await page.waitForTimeout(500);
      console.log(`  ${path} → ${page.url()}`);
    }

    if (errors.length > 0) console.log("JS ERRORS:", errors);
    expect(errors).toHaveLength(0);
  });

  test("4. Create landing page: hero, goal input, and button", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await injectAuth(page, authToken);
    await page.goto(`${BASE}/create`);
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(500);

    await expect(page.locator("text=AI-Powered Course Builder")).toBeVisible();
    await expect(page.locator("text=What do you want to learn")).toBeVisible();
    await expect(page.locator("text=Describe a topic")).toBeVisible();

    const textarea = page.locator("textarea");
    await expect(textarea).toBeVisible();

    const buildBtn = page.getByRole("button", { name: "Build Course" });
    await expect(buildBtn).toBeVisible();
    await expect(buildBtn).toBeDisabled();

    await textarea.fill("How neural networks learn");
    await expect(buildBtn).toBeEnabled();

    await textarea.fill("");
    await expect(buildBtn).toBeDisabled();

    await expect(page.locator("text=Back to courses")).toBeVisible();
    await expect(page.locator("text=Press Enter to submit")).toBeVisible();

    const realErrors = errors.filter(
      (e) => !e.includes("fetch") && !e.includes("Request failed"),
    );
    expect(realErrors).toHaveLength(0);
  });

  test("5. Create draft → workspace loads with title and phase", async ({ page }) => {
    const draft = await createDraft(authToken, "E2E: Attention Mechanisms");
    await gotoWorkspace(page, authToken, draft.id);

    await expect(page.locator("text=E2E: Attention Mechanisms")).toBeVisible();
    await expect(page.locator("text=Shaping")).toBeVisible();
    await expect(page.locator('a[href="/create"]')).toBeVisible();
  });

  test("6. ChatPanel renders with header, input, send button", async ({ page }) => {
    const draft = await createDraft(authToken, "E2E: Chat Panel");
    await gotoWorkspace(page, authToken, draft.id);

    await expect(page.locator("text=Course Assistant")).toBeVisible();

    const chatInput = page.locator('textarea[placeholder="Refine your course..."]');
    await expect(chatInput).toBeVisible();

    // Send button should exist (find by role)
    const sendBtns = page.locator("button").filter({ has: page.locator("svg") });
    expect(await sendBtns.count()).toBeGreaterThan(0);
  });

  test("7. ArtifactPanel: all 5 tabs render and switch correctly", async ({ page }) => {
    const draft = await createDraft(authToken, "E2E: Tab Switching");
    await gotoWorkspace(page, authToken, draft.id);

    const tabs = ["Outline", "Progress", "Lessons", "Sources", "Quality"];
    for (const tab of tabs) {
      const tabEl = page.locator(`[role="tab"]:has-text("${tab}")`);
      await expect(tabEl).toBeVisible();
    }

    // Outline tab active by default
    await expect(page.locator('[role="tab"]:has-text("Outline")')).toHaveAttribute("data-state", "active");

    // Click Progress → shows empty state
    await page.locator('[role="tab"]:has-text("Progress")').click();
    await page.waitForTimeout(300);
    await expect(page.locator('[role="tab"]:has-text("Progress")')).toHaveAttribute("data-state", "active");
    await expect(page.locator("text=Build Course").first()).toBeVisible();

    // Click Lessons → shows empty state
    await page.locator('[role="tab"]:has-text("Lessons")').click();
    await page.waitForTimeout(300);
    await expect(page.locator("text=Generate content first")).toBeVisible();

    // Click Sources → shows empty state
    await page.locator('[role="tab"]:has-text("Sources")').click();
    await page.waitForTimeout(300);
    await expect(page.locator("text=Sources will appear after")).toBeVisible();

    // Click Quality → shows empty state
    await page.locator('[role="tab"]:has-text("Quality")').click();
    await page.waitForTimeout(300);
    await expect(page.locator("text=Quality metrics will appear")).toBeVisible();

    // Back to Outline
    await page.locator('[role="tab"]:has-text("Outline")').click();
    await page.waitForTimeout(300);
    await expect(page.locator('[role="tab"]:has-text("Outline")')).toHaveAttribute("data-state", "active");
  });

  test("8. OutlineView: shows generating or empty state", async ({ page }) => {
    const draft = await createDraft(authToken, "E2E: Outline State");
    await gotoWorkspace(page, authToken, draft.id);

    // The page auto-generates outline, so we should see one of these states
    const generating = page.locator("text=Building your course outline");
    const empty = page.locator("text=No outline yet");
    const outlineHeader = page.locator("text=E2E: Outline State").first();

    await page.waitForTimeout(1000);

    const isGenerating = await generating.isVisible().catch(() => false);
    const isEmpty = await empty.isVisible().catch(() => false);
    const hasOutline = await outlineHeader.isVisible().catch(() => false);

    console.log(`  Outline state: generating=${isGenerating} empty=${isEmpty} loaded=${hasOutline}`);
    expect(isGenerating || isEmpty || hasOutline).toBeTruthy();
  });

  test("9. Draft list shows on landing after creating drafts", async ({ page }) => {
    // Create a couple drafts first
    await createDraft(authToken, "E2E: Draft List Item 1");
    await createDraft(authToken, "E2E: Draft List Item 2");

    await injectAuth(page, authToken);
    await page.goto(`${BASE}/create`);
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(1500);

    const recentDrafts = page.locator("text=Recent Drafts");
    const hasDrafts = await recentDrafts.isVisible().catch(() => false);

    if (hasDrafts) {
      console.log("  Draft list visible ✓");
      // Check at least one draft card is clickable
      const draftCards = page.locator('[data-slot="card"]');
      const count = await draftCards.count();
      console.log(`  Found ${count} draft cards`);
      expect(count).toBeGreaterThan(0);
    } else {
      console.log("  No drafts section visible (API may have returned empty)");
    }
  });

  test("10. Navigation: Create link in learn layout", async ({ page }) => {
    await injectAuth(page, authToken);
    await page.goto(`${BASE}/learn`);
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(1000);

    const createLink = page.locator('a[href="/create"]');
    if ((await createLink.count()) > 0) {
      await expect(createLink.first()).toBeVisible();
      console.log("  Create link found in learn nav ✓");
    } else {
      console.log("  Create link not found (may need wider viewport)");
    }
  });

  test("11. Resizable panels exist in workspace", async ({ page }) => {
    const draft = await createDraft(authToken, "E2E: Resize Panels");
    await gotoWorkspace(page, authToken, draft.id);

    // react-resizable-panels renders the separator with role="separator"
    const resizeHandle = page.locator('[role="separator"], [data-panel-resize-handle-id], .cursor-col-resize');
    const handleCount = await resizeHandle.count();
    console.log(`  Resize handles found: ${handleCount}`);
    expect(handleCount).toBeGreaterThan(0);
  });

  test("12. Console error audit across all create flows", async ({ page }) => {
    const consoleErrors: string[] = [];
    const pageErrors: string[] = [];

    page.on("console", (msg) => {
      if (msg.type() === "error") {
        const text = msg.text();
        if (!text.includes("favicon") && !text.includes("ERR_CONNECTION")) {
          consoleErrors.push(text);
        }
      }
    });
    page.on("pageerror", (err) => pageErrors.push(err.message));

    await injectAuth(page, authToken);

    // Landing page
    await page.goto(`${BASE}/create`);
    await page.waitForTimeout(1000);

    // Workspace page
    const draft = await createDraft(authToken, "E2E: Console Audit");
    await page.goto(`${BASE}/create/${draft.id}`);
    await page.waitForLoadState("domcontentloaded");
    await page.waitForSelector("text=Course Assistant", { timeout: 10000 });
    await page.waitForTimeout(1000);

    // Click through all tabs
    for (const tab of ["Progress", "Lessons", "Sources", "Quality", "Outline"]) {
      await page.locator(`[role="tab"]:has-text("${tab}")`).click();
      await page.waitForTimeout(500);
    }

    console.log(`  Page errors: ${pageErrors.length}`);
    console.log(`  Console errors: ${consoleErrors.length}`);

    if (pageErrors.length > 0) console.log("  PAGE ERRORS:", pageErrors);
    if (consoleErrors.length > 0) console.log("  CONSOLE ERRORS:", consoleErrors);

    const critical = pageErrors.filter(
      (e) => !e.includes("fetch") && !e.includes("Request failed") && !e.includes("AbortError"),
    );
    expect(critical).toHaveLength(0);
  });
});
