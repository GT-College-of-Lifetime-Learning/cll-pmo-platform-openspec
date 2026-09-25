// Header review count with dean provenance
// Task 2.5: Header review count = team + dean (27) with tooltip
// D2: Header shows teamReview + deanReview (27) with title="21 team + 6 dean"

// Compute team review count (targetStatus !== "source")
// Given a goals array, returns count of goals with targetStatus !== "source"
export function countTeamReview(goals) {
  return goals.filter((g) => g.targetStatus !== "source").length;
}

// Compute dean review count (targetStatus === "needs_review" and not source)
// Given a goals array, returns count of goals needing review (excludes source)
export function countDeanReview(goals) {
  return goals.filter((g) => g.targetStatus === "needs_review").length;
}

// Compute total review count
export function countTotalReview(goals) {
  return countTeamReview(goals) + countDeanReview(goals);
}

// Format the header title: "27 need review"
// Returns the title string and tooltip string
export function formatHeaderReview(goals) {
  const total = countTotalReview(goals);
  const team = countTeamReview(goals);
  const dean = countDeanReview(goals);
  const title = `${total} need review`;
  const tooltip = `${team} team + ${dean} dean`;
  return { title, tooltip };
}

// Export for CommonJS
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    countTeamReview,
    countDeanReview,
    countTotalReview,
    formatHeaderReview,
  };
}