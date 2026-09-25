// Agent tools for Blueprint
// Tasks 6.1-6.2: read_blueprint_summary, filter_kpi_cascade

// Read blueprint summary data for agent/consumer use
// Task 6.1: read_blueprint_summary adds deanNeedsReview, totalNeedsReview, alignmentGaps
export function readBlueprintSummary(goals) {
  const totalNeedsReview = goals.filter((g) => g.targetStatus === "needs_review").length;
  const deanNeedsReview = goals.filter((g) => g.targetStatus === "needs_review" && g.id.startsWith("6-")).length;
  const alignmentGaps = computeAlignmentGaps(goals);

  return {
    totalNeedsReview,
    deanNeedsReview,
    alignmentGaps,
    teamCount: goals.filter((g) => g.targetStatus !== "source").length,
    sourceCount: goals.filter((g) => g.targetStatus === "source").length
  };
}

// Compute alignment gaps (zero cells in priority × team matrix)
function computeAlignmentGaps(goals) {
  const priorities = ["P01", "P02", "P03", "P04", "P05", "P06"];
  const areas = [
    "Learning Experiences",
    "Library",
    "Admissions",
    "Career Services",
    "Infrastructure",
    "Strategy 2035"
  ];

  let gapCount = 0;
  priorities.forEach((p) => {
    areas.forEach((a) => {
      if (goals.filter((g) => g.area === a && g.priorities.includes(p)).length === 0) {
        gapCount++;
      }
    });
  });

  return gapCount;
}

// Filter KPI cascade to update URL hash like the UI
// Task 6.2: filter_kpi_cascade updates URL hash like the UI
export function filterKPICascade(goals, filterParams) {
  // Apply filters and return cascaded KPIs
  // filterParams can include: view, priority, focus, team, search
  let filtered = [...goals];

  if (filterParams.team) {
    filtered = filtered.filter((g) => g.team === filterParams.team);
  }

  if (filterParams.priority) {
    filtered = filtered.filter((g) => g.priorities.includes(filterParams.priority));
  }

  if (filterParams.search) {
    const searchLower = filterParams.search.toLowerCase();
    filtered = filtered.filter((g) =>
      g.title.toLowerCase().includes(searchLower) ||
      g.id.toLowerCase().includes(searchLower) ||
      g.priorities.some((p) => p.toLowerCase().includes(searchLower))
    );
  }

  if (filterParams.focus) {
    // When focus is set, filter to goals related to that focus priority
    filtered = filtered.filter((g) => g.priorities.includes(filterParams.focus));
  }

  return filtered;
}

// Export for CommonJS
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    readBlueprintSummary,
    filterKPICascade,
    computeAlignmentGaps
  };
}