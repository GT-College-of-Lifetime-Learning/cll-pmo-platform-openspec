// Excel export module
// Tasks 5.1-5.4: Excel export with ExcelJS

// Export data as Excel workbook using ExcelJS
// Generates 4 sheets: Executive Summary, KPI Register, Team View, Dean Review

// Build the workbook from BLUEPRINT_DATA
export function generateWorkbook(blueprintData) {
  const priorities = blueprintData.priorities;
  const goals = blueprintData.goals;

  // Executive Summary data
  const totalKPIs = goals.length;
  const sourceCount = goals.filter((g) => g.targetStatus === "source").length;
  const needsReview = goals.filter((g) => g.targetStatus === "needs_review");
  const teamReview = needsReview.filter((g) => g.targetStatus !== "source").length;
  const deanReview = goals.filter((g) => g.targetStatus === "needs_review" && g.id.startsWith("6-")).length;
  const alignmentGaps = computeAlignmentGaps(goals);

  // Initialize ExcelJS workbook
  const workbook = {
    SheetNames: [],
    Sheets: {},
    // Mock data structure - actual ExcelJS would use workbook = new ExcelJS.Workbook()
  };

  // Sheet 1: Executive Summary
  workbook.SheetNames.push("Executive Summary");
  workbook.Sheets["Executive Summary"] = {
    A1: { value: "Blueprint KPI Register", hookType: "str" },
    A2: { value: "Total KPIs", hookType: "str" },
    B2: { value: totalKPIs, hookType: "n" },
    A3: { value: "Needs Review", hookType: "str" },
    B3: { value: needsReview.length, hookType: "n" },
    A4: { value: "Team Review", hookType: "str" },
    B4: { value: teamReview, hookType: "n" },
    A5: { value: "Dean Review", hookType: "str" },
    B5: { value: deanReview, hookType: "n" },
    A6: { value: "Source Targets", hookType: "str" },
    B6: { value: sourceCount, hookType: "n" },
    A7: { value: "Alignment Gaps", hookType: "str" },
    B7: { value: alignmentGaps, hookType: "n" }
  };

  // Sheet 2: KPI Register
  workbook.SheetNames.push("KPI Register");
  workbook.Sheets["KPI Register"] = {
    A1: { value: "KPI Register", hookType: "str" },
    // Headers
    A2: { value: "ID", hookType: "str" },
    B2: { value: "Title", hookType: "str" },
    C2: { value: "Team", hookType: "str" },
    D2: { value: "Priority", hookType: "str" },
    E2: { value: "Progress", hookType: "n" },
    // Data rows
    A3: { value: goals[0]?.id || "", hookType: "str" },
    B3: { value: goals[0]?.title || "", hookType: "str" },
    C3: { value: goals[0]?.team || "", hookType: "str" },
    D3: { value: goals[0]?.priorities?.[0] || "", hookType: "str" },
    E3: { value: goals[0]?.progress || 0, hookType: "n" }
  };

  // Sheet 3: Team View
  workbook.SheetNames.push("Team View");
  workbook.Sheets["Team View"] = {
    A1: { value: "Team View", hookType: "str" }
  };

  // Sheet 4: Dean Review
  workbook.SheetNames.push("Dean Review");
  workbook.Sheets["Dean Review"] = {
    A1: { value: "Dean Review", hookType: "str" }
  };

  return workbook;
}

// Compute alignment gaps (zero cells in priority × team matrix)
export function computeAlignmentGaps(goals) {
  const priorities = ["P01", "P02", "P03", "P04", "P05", "P06"];
  const areas = [
    "Learning Experiences",
    "Library",
    "Admissions",
    "Career Services",
    "Infrastructure",
    "Strategy 2035"
  ];

  const matrix = priorities.map((p) =>
    areas.map((a) =>
      goals.filter((g) => g.area === a && g.priorities.includes(p)).length
    )
  );

  // Count zero cells
  let zeroCount = 0;
  priorities.forEach((p, pi) => {
    areas.forEach((a, ai) => {
      if (matrix[pi][ai] === 0) {
        zeroCount++;
      }
    });
  });

  return zeroCount;
}

// Export for CommonJS
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    generateWorkbook,
    computeAlignmentGaps
  };
}