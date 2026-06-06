# AgentSpec — Agent Instructions

## Repo role

This repo is a monorepo containing two systems:

1. **AgentSpec CLI** (`breathe/` Python package) — the primary product. A local-first behavioral contract testing harness for AI agents. CLI commands: `breathe run`, `breathe rank` (entry points: `breathe`, `agentspec`).
2. **Event discovery web app** (`web/`) — a paired Next.js 15 system with calendar import, Clerk auth, Neon DB, and iCal feed. Currently unpublished and undeployed.

Always read before coding:
- `docs/shared-product-context.md`
- `docs/cross-repo-contract.md`
- `docs/current-architecture.md`
- `docs/build-and-test.md`

---

## Product definition: AgentSpec

AgentSpec is a local-first CLI for testing AI agents like software.

You write a YAML contract that defines what your agent must do — required output fields, required phrases, forbidden claims, citation requirements, allowed tool calls, latency budgets. AgentSpec runs your agent as a subprocess, captures stdout/stderr/exit code/latency, checks the output against the contract, and produces a Markdown/JSON report. It exits 1 on failure, 0 on pass. CI blocks on failure.

The agent is a black box. AgentSpec does not instrument the model. It runs the same cases repeatedly and checks output against explicit expectations.

**What it is not:** a model benchmark, a dashboard, a prompt playground, or an evals SaaS. It is a contract test harness.

**Name note:** The public CLI command is `breathe` (e.g. `breathe run spec.yaml`). The product is called AgentSpec. The `agentspec` entry point is an alias. The README currently says "Breathe." Do not treat this as an error — the naming is in transition. Do not rename the Python package or break the `breathe` entry point without explicit instruction.

---

## Positioning

- "Test your AI agent like software."
- Behavioral contracts in YAML.
- Black-box subprocess execution — language and framework agnostic.
- Works with any agent that reads JSON from stdin and writes JSON to stdout.
- CI-ready. Zero model bias. Deterministic checks.
- Open source, local-first, no accounts required.

---

## Demo flow

The canonical demo runs three cases in sequence (`make demo`):

1. **Fragile agent (expect FAIL)** — buggy refund agent fails citation, forbidden-phrase, and tool checks. Shows what a caught regression looks like.
2. **Fixed agent (expect PASS)** — same spec, correct implementation. Clean contract result.
3. **Event scout (PASS)** — Claude-backed event ranker tested against a contract requiring citations, allowed tool calls, and structured JSON output.

Works without an API key (demo mode, keyword scoring). With `ANTHROPIC_API_KEY` or `OPENROUTER_API_KEY` set, the event scout uses live Claude.

---

## Architecture loop

```
breathe.yaml / agentspec.yaml
  → load_spec()  (breathe/config.py)
  → for each case: spawn agent subprocess, inject JSON via stdin  (breathe/runner.py)
  → capture stdout JSON, stderr, exit code, latency  (breathe/run.py)
  → 11 behavioral checks:
       valid JSON · required fields · contains · forbids · requires_citation
       allowed_tools_only · must_call_tools · latency budget  (breathe/checks.py)
  → case scores + failure details
  → write Markdown + JSON report  (breathe/report.py)
  → exit 0 (PASS) or 1 (FAIL)
```

---

## Commands

### CLI (primary system)

| Command | What it does |
|---|---|
| `make install` | Create `.venv` and install package + dev deps |
| `make demo` | Run 3-case demo (FAIL → PASS → PASS) |
| `make test` | Run pytest (`tests/test_breathe.py`) |
| `make clean` | Remove `.venv` and report caches |
| `.venv/bin/breathe run <spec.yaml>` | Run a contract spec |
| `.venv/bin/breathe run <spec.yaml> --no-fail` | Run without blocking CI |
| `.venv/bin/breathe run <spec.yaml> --report <path.md>` | Custom Markdown report path |
| `.venv/bin/breathe run <spec.yaml> --json-report <path.json>` | JSON report output |
| `.venv/bin/breathe rank "<interests>"` | Rank NYC Tech Week events for interests (opens browser) |
| `.venv/bin/breathe rank --repo <github-url>` | Rank events for a codebase (auto-detects git remote) |
| `.venv/bin/agentspec run <spec.yaml>` | Alias for `breathe run` |

### Web (`web/` — paired system, currently unpublished)

| Command | What it does |
|---|---|
| `cd web && npm install` | Install deps |
| `cd web && npm run dev` | Start dev server at localhost:3000 |
| `cd web && npm run build` | Type-check + build (must pass before marking any change done) |
| `cd web && npm run lint` | ESLint |

---

## Rules for future agents

1. **Before touching any file**, identify which system owns the change: CLI (`breathe/`, `examples/`, `tests/`, `Makefile`, `pyproject.toml`) or web (`web/`). State this explicitly.
2. **Before modifying shared contracts** (DB schema, API shape, env vars, event data type, auth), update `docs/cross-repo-contract.md` and note the paired system's impact.
3. **Do not add a CLI feature without a test case** in `tests/test_breathe.py` or a matching YAML spec in `examples/`.
4. **Do not invent users, metrics, or performance numbers.** The demo is the proof.
5. **AgentSpec is not a benchmark.** Do not frame any output as model quality scoring or LLM evaluation. It tests agent behavior against explicit contracts.
6. **The web system (`web/`) is currently unpublished.** Do not write code that assumes live DB, live Clerk, or live Firecrawl unless env vars are confirmed present.
7. **Run `make test` before reporting any CLI change done.** If touching the web system, also run `cd web && npm run build`.
8. **Do not commit API keys, secrets, or `.env` files.**
9. **Do not mention Rolemate** in any public file, README, or generated copy.
10. **The `web/` directory is architecturally separate from the standalone Breathe product repo.** Do not conflate them. Treat `web/` as internal/staged infrastructure until explicitly directed otherwise.
