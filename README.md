# AgentSpec

A cloneable CLI test harness for AI agents.

AgentSpec turns an AI agent prompt/tool setup into something closer to a normal software component: define expected behavior, run eval cases, catch regressions, generate reports, and fail CI when the agent silently breaks.

## Why this exists

Most AI demos are tested manually:

```text
ask a few questions → looks good → ship
```

Then the app breaks when someone changes the prompt, model, tool schema, temperature, retrieval context, or output format.

AgentSpec gives builders a repeatable contract test loop:

```text
agent contract → eval cases → agent command → structured checks → report → CI exit code
```

## What it checks

AgentSpec can verify:

- valid JSON output
- required response fields
- required phrases / concepts
- forbidden claims or phrases
- citations that must match provided source IDs
- tool calls restricted to an allowed list
- required tool calls for a case
- timeouts and latency budgets
- pass/fail behavior for CI

## Demo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
./demo.sh
```

The demo runs two agents:

1. A deliberately fragile support agent that makes unsupported refund claims and invents behavior.
2. A fixed support agent that cites the supplied policy and refuses unsupported same-day refund guarantees.

Example output:

```text
== AgentSpec demo: first run the fragile agent ==
AgentSpec: FAIL
Agent: refund-support-agent-buggy
Cases: 2 | Passed: 0 | Failed: 2

== AgentSpec demo: now run the fixed agent ==
AgentSpec: PASS
Agent: refund-support-agent-fixed
Cases: 2 | Passed: 2 | Failed: 0
```

Reports are written to:

```text
reports/buggy-agent-report.md
reports/fixed-agent-report.md
```

## Example contract

```yaml
agent:
  name: refund-support-agent
  command: "{python} fixed_agent.py"
  timeout_seconds: 10

contract:
  allowed_tools:
    - lookup_policy
    - create_ticket
  must_not:
    - "same-day refunds are guaranteed"
  output:
    json: true
    required_fields:
      - answer
      - citations
      - tool_calls

cases:
  - id: unsupported_sameday_claim
    input: "Does the policy guarantee same-day refunds?"
    sources:
      - id: policy_refunds
        text: "Defective items are eligible for a refund within 30 days."
    expected:
      contains:
        - insufficient evidence
      forbids:
        - guaranteed
      requires_citation: true
      allowed_tools_only: true
      must_call_tools:
        - lookup_policy
```

## CLI

```bash
agentspec run examples/support-agent/agentspec-fixed.yaml \
  --report reports/fixed-agent-report.md \
  --json-report reports/fixed-agent-report.json
```

If the contract fails, AgentSpec exits with code `1`. Use `--no-fail` for demos where you intentionally show a broken agent.

## Why this is an AI build

AgentSpec is not a chatbot wrapper. It is infrastructure for AI systems. The agent can be any local script or model-backed app. AgentSpec handles the repeatable outer loop: execution, source-aware checks, tool-call validation, failure reporting, and CI gating.

That matters because AI agent quality is behavioral. A prompt change that improves one case can break another. AgentSpec makes that visible.

## Event demo framing

**One-liner:** AgentSpec is a cloneable test harness for AI agents: define expected behavior, run eval cases, catch regressions, and generate a CI-ready report.

**10-minute demo:**

1. Show the YAML contract.
2. Run the fragile agent.
3. AgentSpec catches unsupported claims, invalid tool calls, and missing citations.
4. Run the fixed agent.
5. AgentSpec passes and writes a report.
6. Show how this can run in GitHub Actions.

## Repo structure

```text
agentspec/
  agentspec/                  # CLI and eval harness
  examples/support-agent/      # broken + fixed demo agents
  tests/                       # pytest tests
  docs/logic-diagram.md        # shareable asset for the event
  .github/workflows/test.yml   # CI example
```

## Future extensions

- model-as-judge checks
- snapshot comparisons across prompt versions
- cost and latency tracking
- model comparison matrix
- GitHub PR comments
- hosted eval history
- private test suites for teams

## License

MIT
