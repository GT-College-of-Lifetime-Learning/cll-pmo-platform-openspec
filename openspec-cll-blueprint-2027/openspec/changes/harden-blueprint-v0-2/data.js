// Blueprint v0.2 data - hardened with provenance and validation
// Source: v0.1 static bundle, enhanced for consistency, provenance, export parity, deep links

// D2: Dean targets get explicit provenance
// Each priority carries targetStatus (source | needs_review)
// Header reports team review + dean review (27 = 21 team + 6 dean)
export const PRIORITIES = [
  {
    id: "P01",
    title: "Quality at Scale",
    short: "Quality",
    targetStatus: "needs_review",
    color: "#ff6b6b",
  },
  {
    id: "P02",
    title: "Ecosystems",
    short: "Ecosystems",
    targetStatus: "needs_review",
    color: "#ffa502",
  },
  {
    id: "P03",
    title: "Futures",
    short: "Futures",
    targetStatus: "needs_review",
    color: "#ffd93d",
  },
  {
    id: "P04",
    title: "Infra & Ops",
    short: "Infra & Ops",
    targetStatus: "needs_review",
    color: "#43aa8b",
  },
  {
    id: "P05",
    title: "Talent & Org",
    short: "Talent & Org",
    targetStatus: "needs_review",
    color: "#1dd1a1",
  },
  {
    id: "P06",
    title: "Strategy 2035",
    short: "Strategy 2035",
    targetStatus: "source",
    color: "#1a1aef",
  },
];

// D5: Initiative normalization
// Each initiative has stable id and aliases; original text preserved for display
export const INITIATIVES = [
  {
    id: "gti2",
    aliases: ["GTI2.0", "GT Infinity 2.0 Public"],
    title: "GT Infinity 2.0",
  },
  {
    id: "dcl",
    aliases: ["Digital Credentialing"],
    title: "Digital Credentialing",
  },
  {
    id: "lt",
    aliases: ["Learning Technologies"],
    title: "Learning Technologies",
  },
];

// D1: Goals with initiativeIds derived from alias matching
// Original 'initiatives' display text preserved; initiativeIds resolved by alias
export const GOALS = [
  // P01 - Quality at Scale
  {
    id: "1-01",
    title: "Learning Studio Makerspace Model",
    team: "Learning Experiences",
    area: "Learning Experiences",
    priorities: ["P01"],
    initiatives: "GTI2.0",
    initiativeIds: ["gti2"], // resolved from "GTI2.0" alias
    progress: 85,
  },
  {
    id: "1-02",
    title: "Learning Experience Design",
    team: "Learning Experiences",
    area: "Learning Experiences",
    priorities: ["P01", "P03"],
    initiatives: "GTI2.0",
    initiativeIds: ["gti2"], // resolved from "GTI2.0" alias
    progress: 60,
  },
  {
    id: "1-03",
    title: "Library Digitization",
    team: "Library",
    area: "Library",
    priorities: ["P02"],
    initiatives: "Digital Credentialing",
    initiativeIds: ["dcl"], // resolved from "Digital Credentialing" alias
    progress: 40,
  },
  {
    id: "1-04",
    title: "Online Enrollment System",
    team: "Admissions",
    area: "Admissions",
    priorities: ["P02"],
    initiatives: "Digital Credentialing",
    initiativeIds: ["dcl"], // resolved from "Digital Credentialing" alias
    progress: 90,
  },
  {
    id: "1-05",
    title: "Career Services Platform",
    team: "Career Services",
    area: "Career Services",
    priorities: ["P03"],
    initiatives: "Learning Technologies",
    initiativeIds: ["lt"], // resolved from "Learning Technologies" alias
    progress: 55,
  },

  // P02 - Ecosystems
  {
    id: "2-01",
    title: "Shared Identity Framework",
    team: "Learning Experiences",
    area: "Learning Experiences",
    priorities: ["P02"],
    initiatives: "Digital Credentialing",
    initiativeIds: ["dcl"],
    progress: 30,
  },
  {
    id: "2-02",
    title: "Learning Analytics Dashboard",
    team: "Learning Experiences",
    area: "Learning Experiences",
    priorities: ["P02"],
    initiatives: "Learning Technologies",
    initiativeIds: ["lt"],
    progress: 70,
  },
  {
    id: "2-03",
    title: "Portfolio Builder",
    team: "Learning Futures",
    area: "Learning Futures",
    priorities: ["P02"],
    initiatives: "Digital Credentialing",
    initiativeIds: ["dcl"],
    progress: 20,
  },
  {
    id: "2-04",
    title: "Admin & Ops LLM Agent",
    team: "Infrastructure",
    area: "Infrastructure",
    priorities: ["P04"],
    initiatives: "GTI2.0",
    initiativeIds: ["gti2"],
    progress: 65,
  },
  {
    id: "2-05",
    title: "Skill Badging System",
    team: "Infrastructure",
    area: "Infrastructure",
    priorities: ["P04"],
    initiatives: "GTI2.0;Digital Credentialing",
    initiativeIds: ["gti2", "dcl"], // multiple aliases
    progress: 15,
  },

  // P03 - Futures
  {
    id: "3-01",
    title: "Predictive Analytics",
    team: "Learning Futures",
    area: "Learning Futures",
    priorities: ["P03"],
    initiatives: "GTI2.0",
    initiativeIds: ["gti2"],
    progress: 25,
  },
  {
    id: "3-02",
    title: "Pathway Recommendation Engine",
    team: "Learning Futures",
    area: "Learning Futures",
    priorities: ["P03"],
    initiatives: "GTI2.0",
    initiativeIds: ["gti2"],
    progress: 10,
  },

  // P04 - Infra & Ops
  {
    id: "4-01",
    title: "Tool Integration",
    team: "Infrastructure",
    area: "Infrastructure",
    priorities: ["P04"],
    initiatives: "GTI2.0",
    initiativeIds: ["gti2"],
    progress: 50,
  },
  {
    id: "4-02",
    title: "Access Control System",
    team: "Infrastructure",
    area: "Infrastructure",
    priorities: ["P04"],
    initiatives: "Digital Credentialing",
    initiativeIds: ["dcl"],
    progress: 80,
  },

  // P05 - Talent & Org
  {
    id: "5-01",
    title: "SME Hiring",
    team: "Learning Experiences",
    area: "Learning Experiences",
    priorities: ["P05"],
    initiatives: "Learning Technologies",
    initiativeIds: ["lt"],
    progress: 45,
  },
  {
    id: "5-02",
    title: "Mentor Program",
    team: "Learning Futures",
    area: "Learning Futures",
    priorities: ["P05"],
    initiatives: "Learning Technologies",
    initiativeIds: ["lt"],
    progress: 30,
  },

  // P06 - Strategy 2035 (source targets)
  {
    id: "6-01",
    title: "Strategic Initiative A",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 100,
  },
  {
    id: "6-02",
    title: "Strategic Initiative B",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 90,
  },
  {
    id: "6-03",
    title: "Strategic Initiative C",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 80,
  },
  {
    id: "6-04",
    title: "Strategic Initiative D",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 70,
  },
  {
    id: "6-05",
    title: "Strategic Initiative E",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 60,
  },
  {
    id: "6-06",
    title: "Strategic Initiative F",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 50,
  },
  {
    id: "6-07",
    title: "Strategic Initiative G",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 40,
  },
  {
    id: "6-08",
    title: "Strategic Initiative H",
    team: "All",
    area: "Strategy 2035",
    priorities: ["P06"],
    source: true,
    progress: 30,
  },
];
// ]]>

// Validation: unique priority ids, codes, and colors checked by validateBlueprint()