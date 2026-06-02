#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports

echo "== AgentSpec demo: first run the fragile agent =="
agentspec run examples/support-agent/agentspec-buggy.yaml \
  --report reports/buggy-agent-report.md \
  --json-report reports/buggy-agent-report.json \
  --no-fail

echo ""
echo "== AgentSpec demo: now run the fixed agent =="
agentspec run examples/support-agent/agentspec-fixed.yaml \
  --report reports/fixed-agent-report.md \
  --json-report reports/fixed-agent-report.json

echo ""
echo "Reports written:"
echo "- reports/buggy-agent-report.md"
echo "- reports/fixed-agent-report.md"
