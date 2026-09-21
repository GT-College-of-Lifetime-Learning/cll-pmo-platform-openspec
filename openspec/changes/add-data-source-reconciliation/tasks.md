# Tasks â€” Data Source Reconciliation

Legend: (code) source-controlled Â· (test) adversarial/planted-defect verification Â· (humans) steward/sponsor action

## 1. Catalog schema and seed
- [x] 1.1 (code) `DataNeeds` table: NeedId, Element, ConsumerView, RequiredFields, Cadence, DefinitionState, SourceState, SourceSystem, SourceFormat, SourceRefresh, Steward, Notes
- [x] 1.2 (code) `SourceDeclarations` table: DeclarationId, Element, System, Format, Refresh, Steward, Notes, MatchedNeedId, RecordedOn
- [x] 1.3 (code) Seed the catalog from the backwards map: 12 KPIs (with definition states incl. UNDEFINED touchpoint/graduates/research-attribution), 6 activity types, capability inventory, hub locations, GT holidays
- [x] 1.4 (code) `DataSource` column on KpiValues, StrategyActivity, Capabilities (default `demo-seed`)

## 2. Coverage view and provenance tags
- [x] 2.1 (code) `/coverage` page: per-need sourced/partial/unsourced, grouped by consumer view with aggregate counts
- [x] 2.2 (code) Wire coverage summary into the feed (`coverage.json` in export_feed)
- [x] 2.3 (code) Provenance display reads DataSource: imported rows name their import source; demo rows state demo origin
- [x] 2.4 (test) Planted defects: a demo row masquerading as real fails the tag check; coverage page disagrees with catalog states fails

## 3. Matrix generator
- [x] 3.1 (code) `demo/generate_matrix.py`: render docs/data-source-matrix.md from the catalog
- [x] 3.2 (code) Drift check: generator compares against the committed file, reports hand edits, rewrites with catalog truth
- [x] 3.3 (test) Drift test: hand-edited matrix is detected and replaced
- [x] 3.4 (code) Commit the generated docs/data-source-matrix.md; reference it from docs/BUILD.md

## 4. Declaration capture
- [x] 4.1 (code) source-declarations.csv template (the steward ask format) in sharepoint/seed/
- [x] 4.2 (code) Declaration loader: match rows to catalog elements, record system/format/refresh/steward, flip SourceState
- [x] 4.3 (code) Unmatched declarations go to a review queue (recorded with MatchedNeedId NULL, surfaced on the coverage page)
- [x] 4.4 (test) Planted defects: declaration naming an unknown element lands in review (no silent row); a MISSING row flips to HAVE only via matched declaration

## 5. First integration increment â€” GT holiday calendar
- [x] 5.1 (code) Loader: confirmed-holidays source file â†’ business-day calendar regeneration, tagged with origin recorded on the catalog row
- [x] 5.2 (code) Replace the REVIEW placeholder in gen_business_days.py with the confirmed-calendar loader path
- [x] 5.3 (test) Import changes business-day math (call-up windows, SLA gates) and coverage flips the holidays row to sourced
- [ ] 5.4 (humans) Strategic Ops obtains the confirmed Institute holiday calendar â€” the one real-world input this increment needs

## 6. Sponsor routing and polish
- [x] 6.1 (code) UNDEFINED rows surface on the coverage page as a needs-attention (sponsor) list; no loader exists for them by construction
- [x] 6.2 (code) README/docs: the P2/P3 workflow (declaration â†’ state flip â†’ loader increment â†’ coverage), steward ask instructions
- [x] 6.3 (test) Full regression battery (routes, flows, visuals, hand-check, trust suite) plus all new planted-defect checks
- [ ] 6.4 (humans) Steward discovery round: send the declaration template to unit data stewards
- [x] 6.5 `openspec validate add-data-source-reconciliation --strict`