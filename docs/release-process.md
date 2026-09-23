# Release Process

**Task:** T-006 (Owner `RELMGR`, Verifier `PLATFORM`)
**Requirements:** REL-002 — acceptance criteria AC-REL-002-1, AC-REL-002-2
**Tests:** TEST-REL-002 · **Evidence:** EV-REL-002 · **Gates:** GATE-0, GATE-8

This document defines how a change reaches an environment, what is recorded
when it does, and how it is reversed.

## Branching

| Branch | Purpose |
|---|---|
| `main` | Always releasable. Protected; no direct commits. |
| `openspec/<change-name>` | One OpenSpec change. Carries both the OpenSpec artifacts and the source code for that change. |

A change is merged to `main` by pull request only. History is never rewritten
and branches are not force-pushed.

## Versioning and commit tagging

Releases use semantic versioning, tagged `v<MAJOR>.<MINOR>.<PATCH>`.

| Increment | When |
|---|---|
| MAJOR | A breaking change to the public API or to a published data contract |
| MINOR | A release gate closes, or new requirements ship |
| PATCH | Defect fixes with no requirement scope change |

Every release tag is annotated and names the release gate it advances, for
example:

```bash
git tag -a v0.1.0 -m "GATE-0: delivery capability established"
git push origin v0.1.0
```

The tag commit SHA is the immutable identifier recorded in the release record.
No artifact is deployed from an untagged commit.

## Release record

One record per release, stored under `docs/releases/<version>.md` and attached
to EV-REL-002. Required fields:

| Field | Description |
|---|---|
| Version | Semantic version, matching the git tag |
| Commit SHA | Full 40-character SHA of the tagged commit |
| Date and time | UTC timestamp of the deployment |
| Environment | dev, test or prod |
| Release gate | Gate advanced by this release, if any |
| Requirements | Requirement ids delivered, e.g. NFR-004, REL-002 |
| Acceptance criteria | Criteria newly satisfied, e.g. AC-NFR-004-1 |
| Evidence | Evidence record ids produced |
| Approvers | Named approvers in the order defined in `registries/approval-sequences.md` |
| Rollback target | Previous version and its commit SHA |
| Known deficiencies | Open defects or active waivers carried into the release |

A release with an open deficiency requires a waiver recorded in the gate
registry format: gate, deficiency, affected requirements and criteria,
compensating control, approver, approval date, expiry date, and the task that
will close it. An expired waiver reopens the gate.

## Promotion path

```
openspec/<change>  ->  PR to main  ->  dev  ->  test  ->  prod
```

1. **dev** — deployed automatically on merge to `main`.
2. **test** — deployed from a release tag. Required for any change touching a
   data contract, the portfolio model or access control.
3. **prod** — deployed from the same tag that passed test, never rebuilt. The
   approval sequence for the advancing gate must be complete before promotion.

Environment parity is a standing requirement (NFR-007, AC-NFR-007-1); any
drift is recorded against EV-NFR-007.

## Rollback

Recovery objectives: **RPO ≤ 4 hours, RTO ≤ 8 hours** (NFR-002).

1. **Declare.** The on-call owner declares a rollback and records the reason.
   No approval is required to roll back; approval is required to roll forward.
2. **Redeploy the previous tag.** Deploy the rollback target named in the
   release record. Do not rebuild from source.
3. **Assess data state.** Application rollback does not reverse data changes.
   - Portfolio model schema migrations are forward-only; each migration ships
     with a tested compensating migration.
   - Landing zone data is immutable and is never rolled back (D1, NFR-006).
   - Snapshots are immutable. A snapshot published in error is superseded by a
     restatement disclosure (BRD-006, KPI-006), never deleted.
4. **Restore if required.** Restore Azure SQL to a point in time within the
   4-hour RPO window.
5. **Verify.** Confirm `/health` and one end-to-end read path per affected
   capability.
6. **Record.** Append a rollback entry to the release record: trigger, start
   and end time, actual RPO and RTO achieved, and follow-up tasks.

Rollback is rehearsed before GATE-8; the rehearsal is evidence for AC-REL-002-2.

## Change freeze

A freeze applies from board package certification (BRD-003) until board
distribution (BRD-007). During a freeze only defect fixes at severity 1 or 2
may merge, and each requires `RELMGR` plus `SPONSOR` approval. The freeze
process is proven before GATE-8.
