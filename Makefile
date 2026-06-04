VENV      = .venv
PIP       = $(VENV)/bin/pip
SPEC      = $(VENV)/bin/agentspec
PYTEST    = $(VENV)/bin/pytest

.PHONY: demo demo-live install test clean

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install -e ".[dev]" -q

install: $(VENV)/bin/activate

# ─── Zero API key — works for everyone in the room ─────────────────────────
demo: install
	@mkdir -p reports
	@echo ""
	@echo "══════════════════════════════════════════════════"
	@echo "  AgentSpec · contract testing for AI agents"
	@echo "══════════════════════════════════════════════════"
	@echo ""
	@echo "▶  1 / 3  — fragile agent (expect FAIL)"
	@echo ""
	@$(SPEC) run examples/support-agent/agentspec-buggy.yaml \
		--report reports/buggy-report.md \
		--json-report reports/buggy-report.json \
		--no-fail
	@echo ""
	@echo "▶  2 / 3  — fixed agent (expect PASS)"
	@echo ""
	@$(SPEC) run examples/support-agent/agentspec-fixed.yaml \
		--report reports/fixed-report.md \
		--json-report reports/fixed-report.json
	@echo ""
	@echo "▶  3 / 3  — NYTechWeek event scout — demo mode (no API key)"
	@echo ""
	@cd examples/event-scout && ../../$(SPEC) run agentspec.yaml \
		--report ../../reports/event-scout-report.md \
		--json-report ../../reports/event-scout-report.json

# ─── Live mode — real Claude call, set ANTHROPIC_API_KEY first ─────────────
demo-live: install
	@mkdir -p reports
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "Set ANTHROPIC_API_KEY first:  export ANTHROPIC_API_KEY=sk-..."; exit 1; fi
	@$(PIP) install anthropic -q
	@echo ""
	@echo "══════════════════════════════════════════════════"
	@echo "  AgentSpec · live Claude agent demo"
	@echo "══════════════════════════════════════════════════"
	@echo ""
	@echo "▶  NYTechWeek event scout — real Claude call"
	@echo ""
	@cd examples/event-scout && ANTHROPIC_API_KEY=$$ANTHROPIC_API_KEY \
		../../$(SPEC) run agentspec.yaml \
		--report ../../reports/event-scout-live-report.md \
		--json-report ../../reports/event-scout-live-report.json

test: install
	$(PYTEST) -q

clean:
	rm -rf $(VENV) reports/__pycache__
