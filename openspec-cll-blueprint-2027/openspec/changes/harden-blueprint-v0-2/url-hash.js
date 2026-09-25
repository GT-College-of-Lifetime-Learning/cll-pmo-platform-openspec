// URL Hash state management
// Tasks 4.1-4.4: Search & state (URL hash sync, persistent collapse, deep links)

// Initial hash state values
const defaultHashState = {
  view: "cascade",        // or "matrix", "detail"
  priorityFilter: "",     // e.g., "P01", "quality"
  focus: "",              // focused priority/goal
  team: "",               // team short filter
  search: "",             // search query
  collapsedTeams: [],     // list of collapsed team section IDs
  openGoal: ""            // goal ID to open in dialog
};

// Parse hash state on page load / hashchange
export function parseHashState() {
  const hash = window.location.hash.substring(1); // Remove leading #
  const state = { ...defaultHashState };

  if (!hash) return state;

  const params = new URLSearchParams(hash);
  // URLSearchParams expects the hash after ? but our format uses &
  // Our format: #view=cascade&p=P01&t=Learning&search=quality
  // But location.hash uses & as separator like query string

  const paramKeys = [
    "view", "p", "f", "t", "q", "g", "c"
  ]; // c = collapsed teams

  for (const key of paramKeys) {
    const value = params.get(key);
    if (value) {
      state[key] = value;
    }
  }

  // Parse collapsed teams (comma-separated)
  if (state.collapsedTeams) {
    state.collapsedTeams = state.collapsedTeams.split(",").filter((t) => t.trim());
  }

  return state;
}

// Encode hash state to location.hash
export function encodeHashState(state) {
  const params = [];

  if (state.view && state.view !== "cascade") params.push(`view=${state.view}`);
  if (state.priorityFilter) params.push(`p=${state.priorityFilter}`);
  if (state.focus) params.push(`f=${state.focus}`);
  if (state.team) params.push(`t=${state.team}`);
  if (state.search) params.push(`q=${encodeURIComponent(state.search)}`);
  if (state.openGoal) params.push(`g=${state.openGoal}`);

  // Collapsed teams as comma-separated
  if (state.collapsedTeams && state.collapsedTeams.length > 0) {
    params.push(`c=${state.collapsedTeams.join(",")}`);
  }

  // Only update hash if there are changes from default
  const hashString = params.length > 0 ? "?" + params.join("&") : "";
  window.location.hash = hashString;
}

// Deep link to a specific goal
export function deepLinkToGoal(goalId) {
  const params = new URLSearchParams();
  params.set("g", goalId);
  window.location.hash = params.toString();
}

// Deep link with multiple filters
export function deepLink(filters) {
  const params = new URLSearchParams();
  if (filters.view) params.set("view", filters.view);
  if (filters.priority) params.set("p", filters.priority);
  if (filters.focus) params.set("f", filters.focus);
  if (filters.team) params.set("t", filters.team);
  if (filters.search) params.set("q", filters.search);
  if (filters.openGoal) params.set("g", filters.openGoal);
  if (filters.collapsedTeams && filters.collapsedTeams.length > 0) {
    params.set("c", filters.collapsedTeams.join(","));
  }
  window.location.hash = params.toString();
}

// Export for CommonJS
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    parseHashState,
    encodeHashState,
    deepLink,
    deepLinkToGoal,
    defaultHashState
  };
}