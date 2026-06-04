# No Forking Way — 10-Minute Demo Script

**Repo:** github.com/advik-bhatt/agentspec  
**One command:** `make demo`

---

## BEFORE YOU GO ON STAGE

Open 3 things:
1. Terminal — already `cd`'d into the repo
2. This file on your phone or second screen
3. `examples/event-scout/agentspec.yaml` open in your editor

Run this once to pre-warm:
```bash
make demo
```

---

## THE TALK (10 min)

### [0:00] Hook — 30 seconds, no typing yet

Say:
> "Everyone in this room has been drowning in NYTechWeek invites this week.
> Too many events, all claiming to be important, scattered across Luma, Partiful, email.
> I built an agent that ranks them for you.
> Then I built the thing that makes sure it doesn't hallucinate event details.
> Here's both, running live."

---

### [0:30] Clone + Run

Type live (or have pre-typed):
```bash
git clone https://github.com/advik-bhatt/agentspec
cd agentspec
make demo
```

Say:
> "That's it. Three commands. No Docker, no config files, no API key needed."

---

### [1:00] FAIL output appears — talk through it

The terminal shows:
```
▶  1 / 3  — fragile agent (expect FAIL)
AgentSpec: FAIL
Cases: 2 | Passed: 0 | Failed: 2
• contains:insufficient evidence: missing 'insufficient evidence'
• forbids:guaranteed: contained forbidden phrase 'guaranteed'
• requires_valid_citation: expected citation id from ['policy_refunds'], got []
```

Say:
> "This agent told a user that same-day refunds are guaranteed.
> That's not in the policy. AgentSpec caught it.
> Missing citation, forbidden claim, hallucinated guarantee — all in one run."

---

### [2:30] PASS output appears

```
▶  2 / 3  — fixed agent (expect PASS)
AgentSpec: PASS
Cases: 2 | Passed: 2 | Failed: 0
Average score: 100.0/100
```

Say:
> "Same contract. Fixed agent. Everything green."

---

### [3:30] Event Scout appears

```
▶  3 / 3  — NYTechWeek event scout
AgentSpec: PASS
Agent: nytechweek-event-scout
Cases: 2 | Passed: 2 | Failed: 0
```

Say:
> "This one's a Claude agent — it ranks real NYTechWeek events by your interests.
> AgentSpec tests that it cites actual sources, uses only approved tools,
> and doesn't invent events that don't exist."

---

### [4:30] Open the YAML — your contract

Switch to editor showing `examples/event-scout/agentspec.yaml`

Point at these lines and read them:
```yaml
must_not:
  - "as an ai"
output:
  required_fields:
    - ranked_events
    - citations
    - tool_calls
cases:
  - id: rank_ai_events_by_interest
    expected:
      requires_citation: true
      must_call_tools:
        - rank_events
```

Say:
> "20 lines of YAML. This is the behavioral contract for your agent.
> Not unit tests. Not vibes. Exact checks that run on every commit."

---

### [6:30] Show CI

Open `.github/workflows/test.yml` or just say:

Say:
> "This is already wired into GitHub Actions.
> Agent regresses on a PR → CI fails → doesn't ship.
> You catch prompt regressions, model swaps, tool schema changes
> before your users do."

---

### [8:00] Plug in your own agent

Say:
> "To use this on your own agent: change one line."

Show:
```yaml
agent:
  command: "python your_agent.py"
  # or: node your_agent.js
  # or: curl -s http://localhost:8080/run
```

Say:
> "AgentSpec sends JSON to stdin, reads JSON from stdout.
> Your agent is a black box. It doesn't care what's inside."

---

### [9:00] Live Claude demo (IF you have your API key)

```bash
export ANTHROPIC_API_KEY=sk-...
make demo-live
```

Say:
> "This is a real Claude call being contract-tested live.
> If it had hallucinated a fake event, that check would fail right here."

---

### [10:00] Close

Say:
> "Clone it. Fork it. Point it at your agent.
> github.com/advik-bhatt/agentspec"

**Leave that URL on the screen.**

---

## IF SOMETHING BREAKS

| Problem | Fix |
|---|---|
| `make: command not found` | `bash demo.sh` instead |
| `agentspec: command not found` | `source .venv/bin/activate` first |
| demo-live fails | skip it, demo mode still shows everything |
| audience can't clone | share the URL, they follow on GitHub |

---

## QUESTIONS YOU'LL GET

**"Can I use GPT-4 / Gemini?"**
> "Yes. AgentSpec doesn't care what's inside your agent. stdin/stdout contract."

**"How is this different from pytest?"**
> "Pytest tests your code. This tests behavior. A prompt change that makes your agent hallucinate won't show up in any unit test."

**"What about streaming?"**
> "Buffer before stdout — same as any CLI pipeline. Or use `--no-fail` while you're iterating."

**"Is this open source?"**
> "MIT. Clone it right now."
