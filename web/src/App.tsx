/**
 * Dashboard shell.
 *
 * The eight executive dashboard requirements (EXD-001 - EXD-008) are
 * implemented in Phase 04 (T-044 - T-055) behind GATE-4. This shell exists so
 * the build, typecheck and accessibility jobs in CI have a real target.
 *
 * Accessibility target: WCAG 2.2 AA (NFR-005, EXD-008).
 */
export function App(): JSX.Element {
  return (
    <main>
      <h1>CLL Strategy 2035 PMO Platform</h1>
      <p>
        Dashboard shell. Executive dashboard requirements EXD-001 through
        EXD-008 are delivered in Phase 04.
      </p>
    </main>
  );
}
