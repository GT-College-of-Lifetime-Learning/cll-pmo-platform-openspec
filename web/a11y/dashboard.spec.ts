import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

/**
 * Seed cases for TEST-NFR-005 and TEST-EXD-008.
 *
 * NFR-005 and EXD-008 require WCAG 2.2 AA conformance. Automated scanning
 * cannot establish full conformance on its own, so the registered `a11y`
 * tests pair this scan with the manual audit evidenced at GATE-4 (T-055).
 */
const wcag22aa = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

test('dashboard shell has no detectable WCAG 2.2 AA violations', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).withTags(wcag22aa).analyze();

  expect(results.violations).toEqual([]);
});

test('dashboard shell exposes a single top-level heading', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { level: 1 })).toHaveCount(1);
});
