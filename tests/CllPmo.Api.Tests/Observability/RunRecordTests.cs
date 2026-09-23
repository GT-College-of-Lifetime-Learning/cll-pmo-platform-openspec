using CllPmo.Api.Observability;
using Xunit;

namespace CllPmo.Api.Tests.Observability;

/// <summary>
/// Seed cases for TEST-NFR-004. The full suite is registered in
/// registries/test-catalog.md and completed under T-004 and T-005.
/// </summary>
public class RunRecordTests
{
    private static RunRecord Record(RunOutcome outcome, DateTimeOffset? completed) =>
        new(
            RunId: Guid.NewGuid(),
            SourceId: "SRC-WD-FIN",
            StartedAtUtc: DateTimeOffset.UnixEpoch,
            CompletedAtUtc: completed,
            Outcome: outcome,
            RecordsRead: 100,
            RecordsQuarantined: 0);

    [Fact]
    public void RunningRun_IsNotComplete()
    {
        var run = Record(RunOutcome.Running, completed: null);

        Assert.False(run.IsComplete);
    }

    [Fact]
    public void SucceededRunWithCompletionTime_IsComplete()
    {
        var run = Record(RunOutcome.Succeeded, completed: DateTimeOffset.UnixEpoch.AddMinutes(5));

        Assert.True(run.IsComplete);
    }

    [Fact]
    public void FailedRun_RequiresAlert()
    {
        var run = Record(RunOutcome.Failed, completed: DateTimeOffset.UnixEpoch.AddMinutes(5));

        Assert.True(run.RequiresAlert);
    }

    [Fact]
    public void SucceededRun_DoesNotRequireAlert()
    {
        var run = Record(RunOutcome.Succeeded, completed: DateTimeOffset.UnixEpoch.AddMinutes(5));

        Assert.False(run.RequiresAlert);
    }

    [Fact]
    public void QuarantinedRecordsAreCountedSeparatelyFromReads()
    {
        var run = new RunRecord(
            RunId: Guid.NewGuid(),
            SourceId: "SRC-WD-FIN",
            StartedAtUtc: DateTimeOffset.UnixEpoch,
            CompletedAtUtc: DateTimeOffset.UnixEpoch.AddMinutes(5),
            Outcome: RunOutcome.SucceededWithQuarantine,
            RecordsRead: 100,
            RecordsQuarantined: 7);

        Assert.Equal(100, run.RecordsRead);
        Assert.Equal(7, run.RecordsQuarantined);
        Assert.True(run.IsComplete);
    }
}
