# AgentSpec

**Your AI agent works today. Do you know when it breaks?**

AgentSpec is a cloneable test harness for AI agents. Define expected behavior in YAML. Run eval cases. Catch regressions before your users do. Fail CI automatically.

---

## Clone and run right now

```bash
git clone https://github.com/advik-bhatt/agentspec
cd agentspec
make demo          # zero API key — works immediately
```

With a real Claude agent:

```bash
export ANTHROPIC_API_KEY=sk-...
make demo-live     # live Claude call, contract-tested on the spot
```

---

## What you'll see

```
▶  1 / 3 — fragile agent (expect FAIL)

AgentSpec: FAIL
Agent: refund-support-agent-buggy
Cases: 2 | Passed: 0 | Failed: 2

Failures:
- unsupported_sameday_claim: 7 failed checks
  • contains:insufficient evidence: missing 'insufficient evidence'
  • forbids:guaranteed: contained forbidden phrase 'guaranteed'
  • requires_valid_citation: expected citation id from ['policy_refunds'], got []

▶  2 / 3 — fixed agent (expect PASS)

AgentSpec: PASS
Agent: refund-support-agent-fixed
Cases: 2 | Passed: 2 | Failed: 0
Average score: 100.0/100

▶  3 / 3 — NYTechWeek event scout

AgentSpec: PASS
Agent: nytechweek-event-scout
Cases: 2 | Passed: 2 | Failed: 0
```

---

## The problem it solves

```
You ship an AI agent.
Teammate updates the prompt.
Locally: looks fine.
In prod: wrong answers, hallucinated claims, banned tool calls.
You find out from a user 3 hours later.
```

AgentSpec is the contract test that catches this before merge.

---

## What it checks

- Valid JSON output and required fields
- Required phrases / concepts in the response
- Forbidden claims and phrases (`must_not`)
- Citations that match provided source IDs — no hallucinating sources
- Tool calls restricted to an allowed list
- Required tool calls per case
- Timeouts and latency budgets
- CI exit code (`1` on failure, `0` on pass)

---

## 20 lines of YAML = a behavioral contract

```yaml
agent:
  name: nytechweek-event-scout
  command: "{python} event_scout.py"
  timeout_seconds: 30

contract:
  allowed_tools:
    - rank_events
  must_not:
    - "as an ai"
  output:
    json: true
    required_fields:
      - ranked_events
      - citations
      - tool_calls

cases:
  - id: rank_ai_events_by_interest
    input: "AI agents, developer tools, LLMs in production"
    sources:
      - id: evt_no_forking_way
        text: "No Forking Way: AI Builds — Startup Grind NYC, Jun 4, 6PM, Civic Hall"
    expected:
      requires_citation: true
      allowed_tools_only: true
      must_call_tools:
        - rank_events
```

---

## Plug in your agent

Change one line:

```yaml
agent:
  command: "python your_agent.py"          # any CLI command
  # command: "node your_agent.js"
  # command: "curl -s http://localhost:8080/run"
```

AgentSpec sends a JSON payload to stdin and reads JSON from stdout. Your agent is a black box.

---

## CI — catches regressions on every PR

```bash
agentspec run your-agent.yaml --report reports/report.md
# exits 1 on failure → blocks the PR
```

`.github/workflows/test.yml` is included. Copy it, point it at your spec.

---

## Included examples

| Example | What it shows |
|---|---|
| `examples/support-agent/` | Buggy vs fixed refund agent — citation, tool, and forbidden-phrase checks |
| `examples/event-scout/` | Claude-backed NYTechWeek event ranker — real API call, contract-tested |

---

## Repo structure

```
agentspec/          core harness (config, runner, checks, report, cli)
examples/
  support-agent/    buggy_agent.py · fixed_agent.py · agentspec-*.yaml
  event-scout/      event_scout.py · agentspec.yaml
tests/              pytest — buggy fails, fixed passes
.github/workflows/  CI that runs on every push
Makefile            make demo · make demo-live · make test
```

---

## One-liner

> AgentSpec: define what your AI agent must do, run it, catch regressions, fail CI. Clone it in 30 seconds.

---

## License

MIT
