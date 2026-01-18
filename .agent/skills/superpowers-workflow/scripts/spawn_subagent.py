#!/usr/bin/env python3
"""Spawn an isolated Gemini CLI subagent for focused task execution.

This enables parallel execution by launching independent gemini instances
with isolated context and specific skill instructions.
"""

import argparse
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    """Traverse upwards to find the repository root (containing .agent/)."""
    curr = start.resolve()
    for _ in range(10):
        if (curr / ".agent").exists():
            return curr
        if curr.parent == curr:
            break
        curr = curr.parent
    return Path.cwd()


def load_skill_instructions(skill_path: Path) -> str:
    """Load skill instructions from SKILL.md file."""
    if not skill_path.exists():
        return ""
    return skill_path.read_text(encoding="utf-8")


def spawn_subagent(
    skill: str,
    task: str,
    repo_root: Path,
    yolo: bool = True,
    output_format: str = "text",
) -> dict[str, Any]:
    """
    Spawn a subagent with isolated context.

    Args:
        skill: Skill name (e.g., 'tdd', 'debug', 'review')
        task: Task description for the subagent
        repo_root: Repository root path
        yolo: Auto-approve all actions (default: True for parallel execution)
        output_format: Output format ('text' or 'json')

    Returns:
        dict with keys: success, output, error, log_file, duration_s
    """
    # Generate unique subagent ID
    subagent_id = uuid.uuid4().hex[:8]
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Setup logging directory
    log_dir = repo_root / "artifacts" / "superpowers" / "subagents"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{skill}-{timestamp}-{subagent_id}.log"

    # Load skill instructions
    skill_file = repo_root / f".agent/skills/superpowers-{skill}/SKILL.md"
    skill_instructions = load_skill_instructions(skill_file)

    if not skill_instructions:
        return {
            "success": False,
            "output": "",
            "error": f"Skill not found: {skill_file}",
            "log_file": str(log_file),
            "duration_s": 0,
        }

    # Construct focused prompt
    prompt = f"""You are a specialized subagent focused on: {skill}

IMPORTANT: You have ISOLATED CONTEXT. Do not assume knowledge from other conversations.

Task:
{task}

Skill Instructions:
{skill_instructions}

Requirements:
1. Follow the skill instructions exactly
2. Complete the task fully
3. Output ONLY the final result at the end
4. Do not include meta-commentary or thinking process in final output
5. Write any artifacts to artifacts/superpowers/subagent-{subagent_id}/

When complete, output:
---SUBAGENT-RESULT-START---
[Your final result here]
---SUBAGENT-RESULT-END---
"""

    # Build command
    cmd = ["gemini"]
    if yolo:
        cmd.append("--yolo")

    # Execute subagent
    start_time = time.time()

    try:
        with open(log_file, "w", encoding="utf-8") as log:
            log.write("=== SUBAGENT EXECUTION LOG ===\n")
            log.write(f"Skill: {skill}\n")
            log.write(f"ID: {subagent_id}\n")
            log.write(f"Timestamp: {timestamp}\n")
            log.write(f"Task: {task}\n\n")
            log.write("=== PROMPT ===\n")
            log.write(prompt)
            log.write("\n\n=== EXECUTION ===\n")
            log.flush()

            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                cwd=repo_root,
                timeout=600,  # 10 minute timeout
                shell=True,  # Required on Windows for .ps1/.cmd scripts
            )

            duration_s = time.time() - start_time

            log.write("\n=== STDOUT ===\n")
            log.write(result.stdout)
            log.write("\n=== STDERR ===\n")
            log.write(result.stderr)
            log.write(f"\n=== EXIT CODE: {result.returncode} ===\n")
            log.write(f"=== DURATION: {duration_s:.2f}s ===\n")

        # Extract final result from markers
        output = result.stdout
        if "---SUBAGENT-RESULT-START---" in output:
            parts = output.split("---SUBAGENT-RESULT-START---", 1)
            if len(parts) > 1:
                result_part = parts[1].split("---SUBAGENT-RESULT-END---", 1)
                output = result_part[0].strip()

        return {
            "success": result.returncode == 0,
            "output": output,
            "error": result.stderr if result.returncode != 0 else "",
            "log_file": str(log_file),
            "duration_s": duration_s,
            "subagent_id": subagent_id,
        }

    except subprocess.TimeoutExpired:
        duration_s = time.time() - start_time
        return {
            "success": False,
            "output": "",
            "error": f"Subagent timed out after {duration_s:.0f}s",
            "log_file": str(log_file),
            "duration_s": duration_s,
            "subagent_id": subagent_id,
        }
    except Exception as e:
        duration_s = time.time() - start_time
        return {
            "success": False,
            "output": "",
            "error": f"Subagent execution failed: {e}",
            "log_file": str(log_file),
            "duration_s": duration_s,
            "subagent_id": subagent_id,
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Spawn a Gemini CLI subagent for parallel execution"
    )
    parser.add_argument(
        "--skill",
        required=True,
        help="Skill to use (tdd, debug, review, rest-automation, python-automation)",
    )
    parser.add_argument(
        "--task",
        required=True,
        help="Task description for the subagent",
    )
    parser.add_argument(
        "--no-yolo",
        action="store_true",
        help="Disable auto-approval (interactive mode)",
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())

    if args.output_format == "text":
        print(f"🤖 Spawning subagent: {args.skill}")
        print(f"📋 Task: {args.task[:80]}{'...' if len(args.task) > 80 else ''}")

    result = spawn_subagent(
        skill=args.skill,
        task=args.task,
        repo_root=repo_root,
        yolo=not args.no_yolo,
        output_format=args.output_format,
    )

    if args.output_format == "json":
        print(json.dumps(result, indent=2))
        return 0 if result["success"] else 1

    # Text output
    print(f"\n{'✅' if result['success'] else '❌'} Subagent completed in {result['duration_s']:.1f}s")
    print(f"📝 Full log: {result['log_file']}")

    if result["success"]:
        print(f"\n{'='*60}")
        print("RESULT:")
        print(f"{'='*60}")
        print(result["output"])
        return 0
    else:
        print(f"\n{'='*60}")
        print("ERROR:")
        print(f"{'='*60}")
        print(result["error"])
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
