# CLL-SPM Semantic Model (PBIP/TMDL)

Source-controlled Power BI Project for the CLL-SPM executive dashboards.
Open `CLL-SPM.pbip` in Power BI Desktop (task 6.4 builds report pages in the tool).

## What's here

| File | Contents |
|---|---|
| `CLL-SPM.pbip` | PBIP entry — semantic model + report pair |
| `CLL-SPM.SemanticModel/model.tmdl` | Star schema, measures, RLS roles (Executive, Unit) |
| `CLL-SPM.Report/` | Report pages (built in Power BI Desktop, saved back as TMDL) |

## Semantic model design (task 6.1)

```
                          +---------------------+
                          | StrategicPriorities |  (dim)
                          +----------+----------+
                                     | 1..*
              +----------------------+----------------------+
              |                        |                     |
      +-------v-------+       +--------v--------+     +-------v------+
      |   WorkItems   | 1..*  |  StatusUpdates  |     |     KPIs     | 1..*
      |  (dim + fact) +-------+  (fact, D5)     |     +------+-------+
      +---+---+---+---+       +-----------------+            |1..*
          |   |   |                                        +v--------+
          |   |   +--> Units (dim)                        | KpiValues|
          |   |                                           | (fact)   |
          |   +--> ConfidentialCounts (masked fact, D13) +----------+
          +--> Milestones (fact)  [added when F3/F4 write]
```

- **Facts**: StatusUpdates (append-only, D5), KpiValues, Milestones, ConfidentialCounts
- **Dimensions**: WorkItems, StrategicPriorities, Units, KPIs, UnitAccess (security)
- **Measures**: latest RAG, status currency %, KPI progress vs target, masked
  "+N Confidential" (D13), items count incl. confidential
- **RLS roles** (6.3, D7 + D13):
  - **Executive** — all rows
  - **Unit** — `NOT(Confidential) OR LeadUnitId = own unit` on detail tables;
    ConfidentialCounts is permissive (non-identifying by construction)
- Test with "View as" in Power BI Desktop after connecting to the live site.

## Connect to the live site (after OIT task 0.7)

1. Open `CLL-SPM.pbip` in Power BI Desktop.
2. The `SiteUrl` expression at the top of `model.tmdl` holds the site URL —
   update it once, all list queries follow.
3. Transform each table: rename SharePoint internal column names to the
   `internalName`s in `sharepoint/registry-lists.json` if the connector exposes
   titles instead.

## Local development without a site

Swap any table's `query` for the matching seed CSV under `sharepoint/seed/`
(e.g., `Csv.Document(...)`) — the seed_loader validates CSVs against the same
schema so column names line up.

## RLS verification checklist (task 6.3)

- [ ] Executive role: sees a Confidential item in full
- [ ] Unit role (same unit): sees own-unit Confidential item in full
- [ ] Unit role (other unit): item hidden from detail; "+N Confidential" appears in totals
- [ ] Unit role: non-confidential Tier 1 college-wide visible; other units' Tier 2 hidden
- [ ] All roles: ConfidentialCounts contributes counts but no drillable rows
- [ ] USERPRINCIPALNAME() resolves in the Power BI app (not just Desktop "View as")