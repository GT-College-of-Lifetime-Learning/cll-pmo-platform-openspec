// Selector layer for Blueprint data
// D1: Introduce pure functions for all counts
// Every render function MUST call selectors; no inline GOALS.filter in templates

// Known valid areas (teams) for area validation
const AREAS = [
  "Learning Experiences",
  "Library",
  "Admissions",
  "Career Services",
  "Infrastructure",
  "Strategy 2035",
];

// Priority IDs
const PRIORITY_IDS = ["P01", "P02", "P03", "P04", "P05", "P06"];

// Selector functions - pure functions that derive counts from data

// baseGoals: goals matching team and search criteria
export const sel = {
  baseGoals: (state, goals) =>
    goals.filter(
      (g) =>
        (state.team === "" || g.team.includes(state.team)) &&
        (state.search === "" ||
          g.title.toLowerCase().includes(state.search.toLowerCase()) ||
          g.id.toLowerCase().includes(state.search.toLowerCase()) ||
          g.priorities.some((p) => g.initiativeIds.some((iid) => INITIATIVES.find((i) => i.id === iid)?.title.toLowerCase().includes(state.search.toLowerCase()))) ||
          g.initiatives.toLowerCase().includes(state.search.toLowerCase()))
    ),

  goals: (state, goals) => sel.baseGoals(state, goals).filter((g) => g.priorities.some((p) => PRIORITY_IDS.includes(p))),

  review: (goals) => goals.filter((g) => g.targetStatus === "needs_review"),

  source: (goals) => goals.filter((g) => g.targetStatus === "source"),

  deanReview: (priorities) =>
    priorities.filter((p) => p.targetStatus !== "source"),

  matrix: (goals, priorities) =>
    priorities.map((p) =>
      AREAS.map((a) =>
        goals.filter((g) => g.area === a && g.priorities.includes(p.id)).length
      )
    ),
};

// Export for CommonJS
if (typeof module !== "undefined" && module.exports) {
  module.exports = { sel, AREAS, PRIORITY_IDS };
}