# Gemini Superpowers for Antigravity

A "Claude Superpowers"-style workflow for **Google Antigravity**, implemented with Antigravity's native primitives:

- **Rules** (always-on guardrails)
- **Workflows** (slash commands like `/superpowers-write-plan`)
- **Skills** (reusable playbooks: brainstorm, plan, TDD, debug, review, finish, plus REST/Python automation)

This repo also includes a runnable **end-to-end REST automation demo** (sync tool + fake API) with **pytest** tests to prove the workflow produces real working changes.

> **Note:** Claude Superpowers uses `/superpowers:write-plan`.  
> Antigravity workflows are file-based; this repo uses hyphenated names:
> `/superpowers-write-plan` (same idea, different syntax).

---

## What's Included

### Rules (enforcement)

**Location:** `.agent/rules/superpowers.md`

Rules enforce:

- Plan gate for non-trivial work (don't code immediately)
- Approval gate (user must approve plan)
- Execute-plan gate (after approval, implement via `/superpowers-execute-plan`)
- Verification required (tests/commands)
- Review pass required (Blocker/Major/Minor/Nit)
- Artifact persistence: outputs must be written to disk under `artifacts/superpowers/`

### Workflows (commands)

**Location:** `.agent/workflows/`

Commands:

- `/superpowers-brainstorm`
- `/superpowers-write-plan`
- `/superpowers-execute-plan` (sequential execution)
- `/superpowers-execute-plan-parallel` (parallel execution with subagents)
- `/superpowers-review`
- `/superpowers-debug`
- `/superpowers-finish`
- `/superpowers-reload` (force re-reading updated rules/workflows/skills after you edit `.agent/*`)

### Skills (library)

**Location:** `.agent/skills/`

Included skills:

- `superpowers-workflow` (controller + helper scripts)
- `superpowers-brainstorm`
- `superpowers-plan`
- `superpowers-tdd`
- `superpowers-debug`
- `superpowers-review`
- `superpowers-finish`
- `superpowers-rest-automation`
- `superpowers-python-automation`

---

## Repo Layout

```
.agent/
├── rules/
│   └── superpowers.md
├── workflows/
│   ├── superpowers-brainstorm.md
│   ├── superpowers-debug.md
│   ├── superpowers-execute-plan.md
│   ├── superpowers-execute-plan-parallel.md  # NEW: Parallel execution
│   ├── superpowers-finish.md
│   ├── superpowers-review.md
│   ├── superpowers-write-plan.md
│   └── superpowers-reload.md
└── skills/
    └── ... (skills folders)
    └── superpowers-workflow/scripts/
        ├── record_activation.py
        ├── spawn_subagent.py              # NEW: Subagent spawning
        └── write_artifact.py

e2e_demo/
├── api/             # local fake REST API (FastAPI)
├── sync_tool/       # Python sync tool (httpx)
└── tests/           # pytest E2E tests

artifacts/
└── superpowers/     # generated outputs (ignored by git)
    ├── plan.md
    ├── execution.md
    ├── finish.md
    └── subagents/   # parallel execution logs
```

---

## Quick Start (Demo)

### Prerequisites

- Python 3.10+
- Antigravity installed
- **For parallel execution:** Gemini CLI (`npm install -g @google/gemini-cli`, then verify with `gemini --version`)

### Install dependencies

From repo root:

**Windows (PowerShell):**

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install fastapi uvicorn httpx pytest
```

**macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install fastapi uvicorn httpx pytest
```

### Run tests

```bash
pytest -q
```

The E2E test validates:

- Pagination from a source REST endpoint
- Transient failures (500 once) + retries
- Rate limiting (429 + Retry-After) handling
- Idempotency (re-running does not create duplicates)
- Demo sync tool features like `--limit N`

---

## Using Superpowers in Antigravity

### 1. Start Antigravity in the repo root

Antigravity discovers workspace rules/workflows/skills from the current workspace. Launch it from this repo root so it can see:

- `.agent/rules`
- `.agent/workflows`
- `.agent/skills`

### 2. The Superpowers loop

**Brainstorm:**

```
/superpowers-brainstorm <your task>
```

**Write plan (no coding here):**

```
/superpowers-write-plan <your task>
```

**Approve:**

```
APPROVED
```

**Execute plan (implementation happens here):**

```
/superpowers-execute-plan
```

Or for parallel execution (if plan has independent steps):

```
/superpowers-execute-plan-parallel
```

**Optional explicit passes:**

```
/superpowers-review
/superpowers-debug
/superpowers-finish
```

### 3. Parallel execution (optional but powerful)

**When to use parallel mode:**

Parallel execution spawns isolated subagents to execute independent plan steps simultaneously, reducing total execution time.

**Example:**
- **Sequential**: Step 1 (5 min) → Step 2 (5 min) → Step 3 (5 min) = **15 minutes**
- **Parallel**: Steps 1, 2, 3 run simultaneously = **~5 minutes**

**How it works:**

1. The workflow analyzes your plan for dependencies
2. Groups steps into batches (Batch 1: independent steps, Batch 2: depends on Batch 1, etc.)
3. Spawns isolated `gemini` subagents for each step in a batch
4. Each subagent has focused context (only sees its step + skill instructions)
5. Results are consolidated and verified after each batch

**When parallel mode is beneficial:**
- Plan has 3+ independent steps
- Steps modify different files
- Steps don't depend on each other
- You want faster execution

**When to stick with sequential:**
- Steps have dependencies
- All steps modify the same file
- Easier to debug (sequential is simpler)

**Usage:**
```
/superpowers-execute-plan-parallel
```

Or let the regular workflow suggest it:
```
/superpowers-execute-plan
# Agent will detect independent steps and ask if you want parallel mode
```

### 4. Artifact persistence (important)

Workflows persist outputs to disk under:

```
artifacts/superpowers/
```

Examples:

- `brainstorm.md`
- `plan.md`
- `execution.md`
- `review.md`
- `debug.md`
- `finish.md`

Some workflows use `write_artifact.py` to avoid IDE-only documents and ensure files exist on disk.

Parallel execution logs are saved to:
```
artifacts/superpowers/subagents/
```

Each subagent gets a unique log file with full execution details.

---

## When Changes Don't Seem to Take Effect

### `/superpowers-reload`

If you edit anything under `.agent/` (Rules, Workflows, or Skills), Antigravity may continue using the previously loaded instructions in the current session.

Run:

```
/superpowers-reload
```

**What it does:**

- Re-reads the contents of:
  - `.agent/rules/`
  - `.agent/workflows/`
  - `.agent/skills/` (names + descriptions)
- Prints a short summary of what it loaded
- Confirms it will follow the latest versions for the rest of the session

**When to use it:**

- After changing any workflow file (e.g. `superpowers-write-plan.md`)
- After updating any skill instructions (SKILL.md)
- After modifying `superpowers.md` rules
- When behavior seems "stuck" on an older version of your instructions

**Alternative:** Starting a new Antigravity conversation also reloads everything.

---

## Contributing

PRs welcome. Good targets:

- Additional workflows (worktrees / finish-branch parity)
- Tighter execute-plan checkpoints
- Additional language stacks (Node/TS, Go)
- More E2E demos for real integration patterns
- Enhancements to parallel execution (smart dependency detection, progress visualization)

---

## License

See LICENSE.