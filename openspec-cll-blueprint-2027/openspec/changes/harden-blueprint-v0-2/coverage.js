// Coverage metric cards
// Tasks 3.1-3.3: Coverage cards and zero-cell treatment

// Known areas (teams)
const AREAS = [
  "Learning Experiences",
  "Library",
  "Admissions",
  "Career Services",
  "Infrastructure",
  "Strategy 2035",
];

// Compute the four coverage metric card values
// Card 1: {n} — team KPIs in view
export function countTeamKPIsInView(goals, teamFilter) {
  if (teamFilter) {
    return goals.filter((g) => g.team === teamFilter).length;
  }
  return goals.length;
}

// Card 2: {s} — targets stated in source
export function countSourceTargets(goals) {
  return goals.filter((g) => g.targetStatus === "source").length;
}

// Card 3: {r} — targets that need review, with sub-label "{rt} team · {rd} dean"
// Returns {totalCount, teamCount, deanCount}
export function countNeedReview(goals) {
  const teamCount = goals.filter((g) => g.targetStatus === "needs_review").length;
  const deanCount = goals.filter((g) => g.targetStatus === "source" && g.id >= "6-01" && g.id <= "6-08").length; // dean targets are P01-P05 needs_review + P06 source, actually dean = needs_review non-source
  // Actually per design: deanReview = priorities filtered where targetStatus !== "source"
  // But for goals, dean count = goals with targetStatus needs_review that are dean-owned
  // Per the data: 6 dean targets = the 5 P01-P05 needs_review + need to determine which are dean
  // Per proposal: "21 team + 6 dean" = total 27
  // Let's compute: team review = goals where targetStatus === "needs_review" and team is not dean
  // Actually simpler: teamReview = count of goals with targetStatus !== "source" minus dean's
  // Per design D2: dean targets have targetStatus "needs_review", header = teamReview + deanReview
  // teamReview = 21, deanReview = 6
  // For now, compute team count as goals with team assignment, dean as the explicit 6
  // Let's use: team count = goals where targetStatus === "needs_review" and team is not the dean-set
  // Actually per the data structure, we'll just return the counts and let the UI handle the split
  const needsReview = goals.filter((g) => g.targetStatus === "needs_review");
  return {
    total: needsReview.length,
    team: needsReview.filter((g) => g.targetStatus === "needs_review" && g.targetStatus !== "source").length,
    dean: goals.filter((g) => g.targetStatus === "needs_review" && g.id.startsWith("6-")).length,
  };
}

// Card 4: {z} — alignment gaps = zero cells in priority × team matrix for teams in scope
// Returns matrix of counts, highlighting zero cells
export function computePriorityTeamMatrix(goals, areas) {
  // Build matrix: priorities × areas
  const priorities = ["P01", "P02", "P03", "P04", "P05", "P06"];
  const matrix = priorities.map((p) =>
    areas.map((a) =>
      goals.filter((g) => g.area === a && g.priorities.includes(p)).length
    )
  );

  // Identify zero cells
  const zeroCells = [];
  priorities.forEach((p, pi) => {
    areas.forEach((ai, aj) => {
      if (matrix[pi][ai] === 0) {
        zeroCells.push({ priority: p, area: areas[ai] });
      }
    });
  });

  return { matrix, zeroCells };
}

// Export for CommonJS
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    countTeamKPIsInView,
    countSourceTargets,
    countNeedReview,
    computePriorityTeamMatrix,
    AREAS,
  };
}