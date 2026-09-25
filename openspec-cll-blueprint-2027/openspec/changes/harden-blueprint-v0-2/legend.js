// Legend rendering - data-driven, filter-aware
// Task 2.4: Replace hard-coded Blueprint legend with data-driven, filter-aware values
// D4: Legend SHALL be rendered from data and reflect the current team and search filters: "{s} source targets · {r} need review"

// Compute legend string from filtered goal set
// Returns "{sourceCount} source targets · {reviewCount} need review"
export function computeLegend(goals) {
  const sourceCount = goals.filter((g) => g.targetStatus === "source").length;
  const reviewCount = goals.filter((g) => g.targetStatus === "needs_review").length;
  return `${sourceCount} source targets · ${reviewCount} need review`;
}

// Compute legend with team filter context
// Returns "{sourceCount} source targets · {reviewCount} need review ({teamCount} team)"
export function computeLegendWithTeam(goals, teamFilter) {
  const filtered = teamFilter
    ? goals.filter((g) => g.team === teamFilter)
    : goals;
  const sourceCount = filtered.filter((g) => g.targetStatus === "source").length;
  const reviewCount = filtered.filter((g) => g.targetStatus === "needs_review").length;
  return `${sourceCount} source targets · ${reviewCount} need review`;
}

// Export for CommonJS
if (typeof module !== "undefined" && module.exports) {
  module.exports = { computeLegend, computeLegendWithTeam };
}