---
description: Execute an approved plan with parallel execution for independent steps. Spawns isolated subagents. Consolidates results.
---

# Superpowers Execute Plan (Parallel Mode)

## Overview
This workflow executes an approved plan by identifying independent steps and running them in parallel using isolated subagents.

## When to use parallel mode
- Plan has 2+ steps that don't depend on each other
- Steps operate on different files or independent modules
- You want faster execution (parallel > sequential)

## When NOT to use parallel mode
- Steps have dependencies (Step 2 needs Step 1's output)
- All steps modify the same file
- Plan has < 2 steps
- You want simpler debugging (sequential is easier to debug)

**If unsure, use `/superpowers-execute-plan` (sequential) instead.**

---

## Preconditions (do not skip)

1. The user must have replied **APPROVED** to a written plan
2. The approved plan must exist at: `artifacts/superpowers/plan.md`

If `artifacts/superpowers/plan.md` does not exist:
- Stop immediately
- Tell the user to run `/superpowers-write-plan` first
- Do not continue

---

## Load and analyze the plan

1. Read `artifacts/superpowers/plan.md`
2. Parse all plan steps
3. Identify dependencies between steps:
   - Does Step 2 modify files created/changed by Step 1?
   - Does Step 2 need Step 1's verification to pass first?
   - Do they modify the same files?
4. Group steps into execution batches:
   - **Batch 1**: All independent steps (no dependencies)
   - **Batch 2**: Steps that depend on Batch 1 completing
   - **Batch 3**: Steps that depend on Batch 2 completing
   - etc.

---

## Execution strategy

### For each batch:

1. **Spawn subagents in parallel** for all steps in the batch:

```bash
# Example: Batch 1 has 3 independent steps
python .agent/skills/superpowers-workflow/scripts/spawn_subagent.py \
  --skill tdd \
  --task "Step 1: Add retry logic to sync.py with exponential backoff" &

python .agent/skills/superpowers-workflow/scripts/spawn_subagent.py \
  --skill rest-automation \
  --task "Step 2: Add pagination handling to fetch_items()" &

python .agent/skills/superpowers-workflow/scripts/spawn_subagent.py \
  --skill python-automation \
  --task "Step 3: Update CLI args to support --max-retries flag" &

# Wait for all to complete
wait
```

2. **Collect results** from each subagent:
   - Check log files in `artifacts/superpowers/subagents/`
   - Extract final results from each
   - Check success/failure status

3. **Verify batch completion**:
   - Run verification commands for all steps in the batch
   - If ANY step fails:
     - Stop execution
     - Switch to `/superpowers-debug` for the failed step
     - Do NOT continue to next batch

4. **Append to execution log**:
   - Write batch summary to `artifacts/superpowers/execution.md`:
     ```markdown
     ## Batch N (Parallel Execution)
     - Step X: [SUCCESS/FAILED] - Files: [...] - Duration: Xs
     - Step Y: [SUCCESS/FAILED] - Files: [...] - Duration: Ys

     Verification:
     - Step X: [command] -> [result]
     - Step Y: [command] -> [result]
     ```

5. **Move to next batch** (if all steps passed)

---

## Skill selection for subagents

Choose the appropriate skill for each step:

| Step Type | Skill to Use |
|-----------|-------------|
| Add tests, TDD cycle | `tdd` |
| Fix bugs, investigate failures | `debug` |
| Code review, quality check | `review` |
| REST API work | `rest-automation` |
| Python tooling/scripts | `python-automation` |
| General implementation | `tdd` (default) |

---

## Consolidation phase

After all batches complete:

1. **Integration verification**:
   - Run full test suite (not just individual step tests)
   - Verify all changes work together
   - Check for conflicts between parallel changes

2. **Conflict resolution**:
   - If parallel steps modified related code:
     - Review for integration issues
     - Run combined tests
     - Fix any conflicts

3. **Final artifacts**:
   - Update `artifacts/superpowers/execution.md` with:
     - Total batches executed
     - Total steps completed
     - Total time saved vs sequential
     - All verification results
   - Write `artifacts/superpowers/finish.md` with:
     - Summary of changes
     - Integration test results
     - Follow-up items (if any)

---

## Example: 5-step plan with 2 batches

**Plan:**
1. Add retry logic to sync.py (independent)
2. Add pagination to API client (independent)
3. Update CLI args (independent)
4. Add integration test (depends on 1, 2, 3)
5. Update docs (depends on 4 passing)

**Execution:**

**Batch 1 (parallel):**
- Spawn 3 subagents for steps 1, 2, 3
- Wait for all to complete (~5 min instead of ~15 min sequential)
- Verify each step

**Batch 2 (sequential):**
- Step 4: Add integration test (needs 1+2+3 complete)
- Verify test passes

**Batch 3 (sequential):**
- Step 5: Update docs (needs 4 complete)
- Verify docs are accurate

**Total time: ~10 min vs ~25 min sequential = 60% time savings**

---

## Troubleshooting

### Subagent spawn fails
- Check that `gemini` is in PATH (verify with: `gemini --version`)
- Verify skill exists: `.agent/skills/superpowers-{skill}/SKILL.md`
- Check subagent logs in `artifacts/superpowers/subagents/`

### Steps conflict
- Falls back to sequential execution for conflicting steps
- Mark dependent steps explicitly in plan to avoid conflicts

### Verification fails after parallel execution
- Check integration - parallel steps may work individually but conflict
- Run `/superpowers-debug` to investigate
- Consider re-running in sequential mode: `/superpowers-execute-plan`

---

## Persist (mandatory)

Write execution notes to disk:
- Append batch summaries to: `artifacts/superpowers/execution.md`
- Write final summary to: `artifacts/superpowers/finish.md`

Ensure `artifacts/superpowers/` exists.
Confirm files exist by listing `artifacts/superpowers/` when done.

---

## Finish

After all steps complete:
1. Run `/superpowers-review` (or inline review pass)
2. Generate final summary with time savings metrics
3. List all changed files
4. Provide any manual validation steps

Stop after completing the finish step.
