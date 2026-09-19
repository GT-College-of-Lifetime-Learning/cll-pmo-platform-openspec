# CLL Digital Transformation Maturity Rubric

Status: Draft — for Dean sign-off (change question Q5). Once signed off, this
document is the published rubric; assessors must use it verbatim.
Source: add-strategy-2035-success-dashboard design D6; Goal 5 (SP-05).

## The five levels

| Level | Name | Meaning | What an assessor should see |
|---|---|---|---|
| 1 | Manual | Paper, email, or hand-passed spreadsheets | Work moves by hand: printed forms, email threads, a spreadsheet someone maintains and emails around |
| 2 | Digitized | Captured in a system of record; online forms | The work is entered in a system (list, form, tool) that is the recognized record; no more parallel spreadsheets |
| 3 | Automated | Rule-based workflow moves the work without manual handoffs | Steps trigger each other: approvals, notifications, data movement happen by rule, not by a person remembering |
| 4 | Data-driven | Instrumented, monitored on dashboards, continuously improved | The work is measured; owners see trends and change the process based on data |
| 5 | AI-enabled | AI agents perform or assist steps with human oversight | AI drafts, classifies, predicts, or executes steps; a named human owns review and correction |

The Dean's mockup labels "Digitized / Automated / AI-enabled" map to levels 2, 3, and 5.

## The index

**Digital Transformation Maturity Index = mean current level of in-scope capabilities**
(unweighted in v1; target level pending Dean decision, Q5).

Computation:
- Every capability in the `Capabilities` list with `InScope = TRUE` contributes its
  current `Level` (1–5).
- A capability is *out of scope* by setting `InScope = FALSE` — the exclusion and its
  reason should be recorded in the capability's notes.
- The index is recomputed at refresh; the as-of date shown is the earliest
  `AssessedOn` among in-scope capabilities (the index is only as fresh as its
  stalest assessment).

## Assessment rules

1. **Evidence required.** A rating without an evidence link is not saved (enforced
   by the list). Evidence: the workflow's system screen, dashboard, automation
   definition, or process doc.
2. **Two-person assessment.** Each rating is assessed by a second person from
   Strategic Operations or the owning unit; the assessor of record is named.
3. **Assess honestly.** A partially automated workflow is level 3 only if the
   *whole chain* moves without manual handoffs; otherwise level 2.
4. **Reassessment:** Strategic Operations runs a full inventory assessment twice a
   year, and project closeouts update the capability they delivered (spec:
   capability updates from Goal 5 work).

## Areas (first-inventory starter set)

Admissions/registration · course scheduling · content development · credentialing
· learner support · financial operations · HR/staffing · facilities/space ·
communications/marketing · data/analytics · compliance/reporting.

Refine the area list during the first inventory (task 1.5); areas feed the heatmap.