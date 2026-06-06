# Breathe Labs — Shared Context

This file provides context for Claude sessions working across the Breathe Labs product suite.
It lives in both repos because there is no shared workspace. Keep both copies in sync when updated.

---

## Identity

Breathe Labs builds focused, high-craft tools for founders, operators, and builders.

Products ship as standalone tools with clear product identities. They are not bundled, platform-ized, or merged unless that is explicitly the next step.

---

## Products

### AgentSpec

**Repo:** `advik-bhatt/agentspec`
**Type:** Local-first CLI, open source
**Stack:** Python, PyYAML, subprocess, standard library (+ optional `anthropic` SDK for live mode)

Behavioral contract testing for AI agents. Define what your agent must do in YAML. Run it. Check the output. Fail CI on regression. No accounts, no servers, no model opinions.

The primary CLI command is `breathe` (e.g. `breathe run spec.yaml`). The `agentspec` entry point is an alias. The README currently says "Breathe CLI." This naming tension is known — the CLI was originally named Breathe before the product separation. Do not treat it as an error. Do not rename the package or break the `breathe` entry point without explicit instruction.

The `agentspec` repo also contains a full event-discovery web app under `web/` (Next.js 15, Clerk, Neon DB). That system is unpublished and undeployed. It is internal/staged infrastructure, not the Breathe landing page product.

**Positioning:** "Test your AI agent like software."
**Not:** a model benchmark, prompt playground, dashboard, or evals SaaS.

---

### Breathe

**Repo:** `advik-bhatt/breathe`
**Type:** Private alpha web product
**Stack:** Next.js 14, React 18, Three.js, Tailwind CSS, Resend, Go signal engine (stub), AMPL optimization model (stub)

Private event intelligence. Turns Luma drops, LinkedIn signals, newsletters, and opt-in calendar context into a ranked map of high-signal rooms. For founders, operators, investors, and builders whose calendar is part of their edge.

Access is invite-only. The product is in private alpha. No public launch. Access requests are collected via the landing page and reviewed manually.

**Positioning:** "Private event intelligence for finding the rooms worth being in."
**Not:** a meditation app, generic calendar, event aggregator, social network, or SaaS dashboard.

---

## Public positioning rules

1. **Do not describe either product as part of a platform, suite, or ecosystem** in public copy, README files, landing pages, demo scripts, or investor materials. Each product stands alone.
2. **Do not invent users, metrics, revenue, partners, sponsors, or traction.** The demo is the proof for AgentSpec. Controlled FOMO through scarcity and quality — not fake numbers — for Breathe.
3. **Do not mention Rolemate** in any public file or generated copy in either repo.
4. **Breathe is not a wellness product.** The name is a spatial/attention metaphor. Do not use wellness, mindfulness, or meditation language.
5. **AgentSpec is not a model benchmark or evals SaaS.** It tests agent behavior against explicit contracts. Do not frame it as model quality scoring.

---

## Private integration notes

*For internal context only. Do not include this framing in public README files, landing pages, demo scripts, or investor materials.*

- These products may later integrate into a larger ecosystem. That is private architecture context.
- The AgentSpec CLI's `breathe rank` command and the Breathe event intelligence product share a conceptual thread (event signal → ranking → calendar action), but they are architecturally separate today.
- The `agentspec` repo's `web/` directory is a more advanced event-discovery system (calendar import, Clerk auth, Neon DB, iCal feed) than the standalone Breathe landing page. Its relationship to the Breathe product repo is not yet resolved. Treat it as internal/undeployed infrastructure.
- Future integration decisions are out of scope for individual coding sessions unless explicitly specified.

---

## Repo relationship

| | AgentSpec (`agentspec/`) | Breathe (`breathe/`) |
|---|---|---|
| Primary language | Python | TypeScript / Next.js |
| Public state | Open source CLI, demo-able | Private alpha, invite-only |
| Auth | None (CLI tool) | Cookie-based owner gate + Resend email |
| Database | None (stateless CLI) | None currently (landing page only) |
| Shared code | None | None |
| Cross-repo contract | None currently | None currently |

These repos do not share code, types, or infrastructure today. They are developed independently. Do not introduce a shared dependency between them without explicit instruction.

---

## Current priorities (as of June 2026)

### AgentSpec
- CLI is fully functional and demo-able
- Used at Startup Grind NYC
- `web/` directory inside the repo needs Neon DB, Firecrawl key, and Vercel deploy before it is usable
- No active web deployment

### Breathe
- Cinematic landing page is built and functional
- Request-access form is wired to Resend
- Private beta — access reviewed manually
- Go signal engine (`services/engine/`) and AMPL model (`optimization/`) are stubs, not wired to production
- No Clerk, no DB — landing-page-only today

---

## How to work across both repos

- **Always treat them as separate products** in outputs, copy, and framing — even when underlying context overlaps.
- **Do not copy-paste product copy between repos** without checking that the framing fits each product's identity.
- **If a cross-repo contract or integration is needed**, document it explicitly and note the impact on both repos in your summary.
- **Changes to AgentSpec CLI event-ranking** may have future relevance to Breathe, but that is not a reason to couple them today.
