import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright drives the accessibility smoke (NFR-005, EXD-008) and, from
 * Phase 04, the `e2e` suites registered in registries/test-catalog.md.
 *
 * webServer builds nothing: CI builds first, then Playwright serves web/dist
 * and waits for the port itself.
 */
export default defineConfig({
  testDir: './a11y',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [['list'], ['html', { open: 'never' }]] : 'list',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run preview',
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});
