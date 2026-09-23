namespace CllPmo.Api.Observability;

/// <summary>
/// Structured run record emitted by every ingestion run.
///
/// NFR-004 requires 100% of ingestion runs to emit a structured run record,
/// and AC-NFR-004-2 requires failed or missing runs to alert the on-call
/// owner. This type is the in-process shape of that record; the sink
/// (Azure Monitor / Application Insights, per D8) is wired in T-004.
/// </summary>
/// <param name="RunId">Unique identifier for the run.</param>
/// <param name="SourceId">Source catalog id, e.g. SRC-WD-FIN.</param>
/// <param name="StartedAtUtc">Run start time in UTC.</param>
/// <param name="CompletedAtUtc">Run completion time in UTC, null while running.</param>
/// <param name="Outcome">Terminal outcome of the run.</param>
/// <param name="RecordsRead">Records read from the source.</param>
/// <param name="RecordsQuarantined">Records quarantined by a blocking quality rule (D6).</param>
public sealed record RunRecord(
    Guid RunId,
    string SourceId,
    DateTimeOffset StartedAtUtc,
    DateTimeOffset? CompletedAtUtc,
    RunOutcome Outcome,
    int RecordsRead,
    int RecordsQuarantined)
{
    /// <summary>
    /// A run is complete when it has a completion time and a terminal outcome.
    /// </summary>
    public bool IsComplete =>
        CompletedAtUtc is not null && Outcome is not RunOutcome.Running;

    /// <summary>
    /// Runs that must raise a watchdog alert (AC-NFR-004-2).
    /// </summary>
    public bool RequiresAlert =>
        Outcome is RunOutcome.Failed || (Outcome is RunOutcome.Running && CompletedAtUtc is null && IsOverdue);

    /// <summary>
    /// Placeholder overdue rule. The real threshold comes from the per-source
    /// SLA in contracts/integration-data-contracts.md and is implemented in T-005.
    /// </summary>
    public bool IsOverdue => false;
}

public enum RunOutcome
{
    Running,
    Succeeded,
    SucceededWithQuarantine,
    Failed
}
