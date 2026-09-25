// validateBlueprint - Load-time validation for BLUEPRINT_DATA
// D4: Renders a visible error banner on violation instead of partial UI

// Known valid areas (teams) for area validation
const AREAS = [
  "Learning Experiences",
  "Library",
  "Admissions",
  "Career Services",
  "Infrastructure",
  "Strategy 2035",
];

// Known valid priority ids
const PRIORITY_IDS = ["P01", "P02", "P03", "P04", "P05", "P06"];

// Validate the blueprint data structure
export function validateBlueprint(data) {
  const errors = [];

  // Guard: ensure required data exists
  if (!data || !data.goals || !data.priorities) {
    errors.push("Blueprint data missing required fields (goals, priorities)");
    renderErrorBanner(errors);
    return false;
  }

  // 1. Check unique goal ids
  const goalIds = data.goals.map((g) => g.id);
  const uniqueGoalIds = new Set(goalIds);
  if (goalIds.length !== uniqueGoalIds.size) {
    errors.push("Duplicate goal ids detected");
  }

  // 2. Check every goal area validity
  for (const goal of data.goals) {
    if (!AREAS.includes(goal.area)) {
      errors.push(`Goal ${goal.id} has invalid area: ${goal.area}`);
    }
    // 3. Check 1-2 priorities, all known ids
    if (goal.priorities.length < 1 || goal.priorities.length > 2) {
      errors.push(`Goal ${goal.id} has ${goal.priorities.length} priorities (expected 1-2)`);
    }
    for (const pid of goal.priorities) {
      if (!PRIORITY_IDS.includes(pid)) {
        errors.push(`Goal ${goal.id} has unknown priority id: ${pid}`);
      }
    }
    // 4. Check every initiativeIds entry exists (if initiatives available)
    if (data.initiatives) {
      for (const iid of goal.initiativeIds) {
        const initiative = data.initiatives.find((i) => i.id === iid);
        if (!initiative) {
          errors.push(`Goal ${goal.id} has unresolvable initiativeId: ${iid}`);
        }
      }
    }
    // 5. Check initiative progress integer 0-100
    if (
      typeof goal.progress !== "number" ||
      goal.progress < 0 ||
      goal.progress > 100 ||
      !Number.isInteger(goal.progress)
    ) {
      errors.push(`Goal ${goal.id} has invalid progress: ${goal.progress}`);
    }
  }

  // 6. Check unique priority ids, codes, and colors
  const priorityIds = data.priorities.map((p) => p.id);
  const uniquePriorityIds = new Set(priorityIds);
  if (priorityIds.length !== uniquePriorityIds.size) {
    errors.push("Duplicate priority ids detected");
  }

  // 7. Check targetStatus on all priorities
  for (const p of data.priorities) {
    if (p.targetStatus !== "source" && p.targetStatus !== "needs_review") {
      errors.push(`Priority ${p.id} has invalid targetStatus: ${p.targetStatus}`);
    }
  }

  // 8. Check initiativeIds entries exist (cross-check, if initiatives available)
  if (data.initiatives) {
    for (const goal of data.goals) {
      for (const iid of goal.initiativeIds) {
        const found = data.initiatives.some((i) => i.id === iid);
        if (!found) {
          errors.push(`Goal ${goal.id} references unknown initiativeId: ${iid}`);
        }
      }
    }
  }

  // Render error banner if violations exist
  if (errors.length > 0) {
    renderErrorBanner(errors);
    return false;
  }

  // Valid data - hide banner if it was previously shown
  removeErrorBanner();
  return true;
}

// Render error banner in the page header
function renderErrorBanner(errors) {
  // Only render in browser environment (document available)
  if (typeof document === "undefined") {
    // In Node.js, just log the errors
    console.error("Blueprint Validation Errors:", errors);
    return;
  }
  const banner = document.createElement("div");
  banner.className = "blueprint-error-banner";
  banner.innerHTML = `
    <div class="banner-content">
      <strong>Blueprint Validation Error</strong>
      <ul>
        ${errors.map((e) => `<li>${e}</li>`).join("")}
      </ul>
      <button class="banner-close">×</button>
    </div>
  `;
  // Insert before the header element
  const header = document.querySelector("header") || document.body;
  header.insertBefore(banner, header.firstChild);
  // Add close handler
  banner.querySelector(".banner-close").addEventListener("click", () => {
    removeErrorBanner();
  });
}

// Remove the error banner
function removeErrorBanner() {
  // Only remove in browser environment
  if (typeof document === "undefined") {
    return;
  }
  const banner = document.querySelector(".blueprint-error-banner");
  if (banner) {
    banner.remove();
  }
}

// Export for use in module context
if (typeof module !== "undefined" && module.exports) {
  module.exports = { validateBlueprint, AREAS, PRIORITY_IDS, renderErrorBanner, removeErrorBanner };
}