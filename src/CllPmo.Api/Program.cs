using CllPmo.Api.Observability;

var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

// Liveness probe. Availability is measured against NFR-002
// (99.5% monthly, business hours 07:00-19:00 ET).
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.Run();

// Exposed so the test project can reference the entry point.
public partial class Program;
