import { expect, test } from "@playwright/test";

test("home page renders the StaffPilot headline", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: /Staffing operations for teams/ }),
  ).toBeVisible();
  await expect(page.getByText(/payroll preparation/i)).toBeVisible();
});

test("health endpoint returns ok", async ({ request }) => {
  const res = await request.get("/api/health");
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  expect(body.status).toBe("ok");
  expect(body.service).toBe("staffpilot");
});

test("login page explains Supabase is required", async ({ page }) => {
  await page.goto("/login");
  await expect(page.getByRole("heading", { name: /Sign in to StaffPilot/ })).toBeVisible();
  await expect(page.getByText(/Supabase/i).first()).toBeVisible();
});
