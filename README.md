# Gemini Superpowers for Antigravity

A systematic workflow framework for **Google Antigravity** that helps you build better code through structured planning, test-driven development, and optional parallel execution.

Think of it as "guardrails for AI coding" - it prevents you from diving straight into code and instead guides you through brainstorming → planning → building → reviewing.

> **Inspired by:** [Claude Superpowers](https://github.com/obra/superpowers)
> **Adapted for:** Google Antigravity with native workflows and skills

---

## 🎯 What This Does

Instead of this chaotic workflow:
```
You: "Build me a CLI tool"
AI: *immediately starts writing code*
You: *realizes halfway through it's not what you wanted*
```

You get this structured approach:
```
You: "Build me a CLI tool"
→ Brainstorm: AI asks clarifying questions
→ Plan: AI writes a step-by-step plan with verification
→ You approve the plan
→ Execute: AI builds it step-by-step with tests
→ Review: AI checks for issues
→ Finish: Everything documented and working
```

**Bonus:** If your plan has independent steps (like "add 3 separate features"), the AI can work on them **in parallel** to save time!

---

## ✨ What's Included

### Workflows (Slash Commands)
These are commands you type in Antigravity:

- `/superpowers-brainstorm` - Explore ideas and ask questions before planning
- `/superpowers-write-plan` - Create a detailed plan (no code yet!)
- `/superpowers-execute-plan` - Build the code step-by-step
- `/superpowers-execute-plan-parallel` - Build independent steps in parallel (faster!)
- `/superpowers-review` - Check code quality
- `/superpowers-debug` - Systematic debugging
- `/superpowers-finish` - Final summary and documentation

### Skills (Building Blocks)
These teach the AI how to work:

- **TDD** - Test-driven development (write tests first)
- **Debug** - Systematic problem solving
- **Review** - Code quality checks
- **REST/Python Automation** - Best practices for specific tasks

### Rules (Guardrails)
Automatic enforcement of good practices:

- ✅ Must write a plan before coding
- ✅ Must get approval before implementing
- ✅ Must verify each step works
- ✅ Must save outputs to disk (not just chat)

---

## 🚀 Getting Started (Step-by-Step)

### Step 1: Check What You Have Installed

Before starting, make sure you have these tools:

#### ✅ Required (You must have these):

**Google Antigravity**
- How to check: Open Antigravity (if it opens, you have it!)
- Don't have it? [Install Antigravity](https://antigravity.google)

**Python 3.10 or newer**
- How to check:
  ```bash
  python --version
  ```
- Should show: `Python 3.10.x` or higher
- Don't have it? [Download Python](https://www.python.org/downloads/)

#### 🎨 Optional (Only needed for parallel execution):

**Gemini CLI** (makes things faster but not required)
- How to check:
  ```bash
  gemini --version
  ```
- If it says "command not found", you don't have it
- To install:
  ```bash
  npm install -g @google/gemini-cli
  ```

  **Windows users:** After installing, verify it works:
  ```powershell
  gemini --version
  ```
  If you see a version number, you're good! If not, see [Troubleshooting](#troubleshooting) below.

---

### Step 2: Set Up This Framework in Your Project

You have two options:

#### Option A: Start a New Project (Recommended for First-Time Users)

1. **Create a new folder for your project:**

   **Windows (PowerShell):**
   ```powershell
   mkdir my-awesome-project
   cd my-awesome-project
   ```

   **Mac/Linux:**
   ```bash
   mkdir my-awesome-project
   cd my-awesome-project
   ```

2. **Copy the `.agent` folder from this repo into your project:**

   **Windows (PowerShell):**
   ```powershell
   # Replace the path with where you downloaded this repo
   Copy-Item -Recurse C:\path\to\gemini-superpowers-antigravity\.agent .
   ```

   **Mac/Linux:**
   ```bash
   # Replace the path with where you cloned this repo
   cp -r /path/to/gemini-superpowers-antigravity/.agent .
   ```

3. **Initialize git (required for the framework to work):**
   ```bash
   git init
   git add .agent
   git commit -m "Add Superpowers framework"
   ```

4. **Open Antigravity in this folder:**

   **From your terminal:**
   ```bash
   # Make sure you're in my-awesome-project folder
   # Then open Antigravity (however you normally do it)
   ```

   **Or:** Open Antigravity → File → Open Folder → Select `my-awesome-project`

#### Option B: Use This Repo Directly (For Testing the Demo)

1. **Clone this repo:**
   ```bash
   git clone <your-repo-url>
   cd gemini-superpowers-antigravity
   ```

2. **Install Python dependencies (for the demo only):**

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -U pip
   pip install fastapi uvicorn httpx pytest
   ```

   **Mac/Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install fastapi uvicorn httpx pytest
   ```

3. **Run the demo tests (optional but cool to see it work):**
   ```bash
   pytest -q
   ```

   You should see: `6 passed` ✅

4. **Open Antigravity in this folder**

---

### Step 3: Verify It's Working

1. **In Antigravity, type:**
   ```
   /superpowers-reload
   ```

2. **You should see output like:**
   ```
   I've reloaded the Superpowers framework:

   Rules: superpowers.md
   Workflows: 8 loaded (brainstorm, debug, execute-plan, execute-plan-parallel, finish, reload, review, write-plan)
   Skills: 9 loaded (brainstorm, debug, finish, plan, python-automation, rest-automation, review, tdd, workflow)

   I will follow these instructions for the rest of this session.
   ```

3. **If you see this, you're ready!** 🎉

4. **If you see "command not found":**
   - Make sure Antigravity is opened in the folder that contains `.agent/`
   - Try closing and reopening Antigravity in the correct folder

---

## 📖 How to Use It (Your First Task)

Let's build something simple to see how it works.

### Example: Build a Simple Calculator CLI

#### Step 1: Brainstorm (Optional but Helpful)

In Antigravity, type:
```
/superpowers-brainstorm

I want to build a simple calculator CLI tool in Python that can add, subtract, multiply, and divide two numbers.
```

**What happens:**
- The AI will ask clarifying questions like:
  - "Should it support decimal numbers?"
  - "Command-line arguments or interactive mode?"
  - "Need error handling for division by zero?"
- Answer them to refine your idea
- The AI writes a brainstorm summary to `artifacts/superpowers/brainstorm.md`

**What you do:** Answer the questions to help the AI understand what you want.

---

#### Step 2: Write a Plan

In Antigravity, type:
```
/superpowers-write-plan

Build a Python calculator CLI with add, subtract, multiply, divide functions. Use argparse for command-line args. Include tests for each function.
```

**What happens:**
- The AI reads your project (if any files exist)
- Creates a step-by-step plan with:
  - Small steps (2-10 minutes each)
  - Files it will create/modify
  - How to verify each step works
- Writes the plan to `artifacts/superpowers/plan.md`
- Asks: **"Approve this plan? Reply APPROVED if it looks good."**

**What you do:**
1. Read the plan in `artifacts/superpowers/plan.md` (or in the chat)
2. Check if it makes sense
3. If you like it, type: `APPROVED`
4. If not, ask for changes

**Example plan you might see:**
```
## Plan

Step 1: Create calculator module
Files: calculator.py
Change: Add functions for add, subtract, multiply, divide
Verify: python -c "from calculator import add; print(add(2, 3))"

Step 2: Add tests
Files: test_calculator.py
Change: Add pytest tests for all functions
Verify: pytest test_calculator.py

Step 3: Create CLI
Files: cli.py
Change: Use argparse to create command-line interface
Verify: python cli.py add 2 3
```

---

#### Step 3: Execute the Plan

After you approve, the AI will say:
```
Plan approved. Run `/superpowers-execute-plan` to begin implementation.
```

Now type:
```
/superpowers-execute-plan
```

**What happens:**
- The AI reads the plan from `artifacts/superpowers/plan.md`
- Implements **one step at a time**
- After each step:
  - Runs the verification command
  - Writes what it did to `artifacts/superpowers/execution.md`
  - Shows you the results
- If verification fails, it stops and debugs
- At the end, writes a summary to `artifacts/superpowers/finish.md`

**What you see:**
```
Implementing Step 1: Create calculator module
[AI writes calculator.py]
Running verification: python -c "from calculator import add; print(add(2, 3))"
✅ Output: 5
Step 1 complete!

Implementing Step 2: Add tests
[AI writes test_calculator.py]
Running verification: pytest test_calculator.py
✅ 4 passed
Step 2 complete!

... (continues for each step)

All steps complete! 🎉
```

**What you do:** Just watch! The AI does the work. If it asks questions, answer them.

---

#### Step 4: Check the Results

1. **Look at the code:**
   ```bash
   ls
   ```
   You should see new files: `calculator.py`, `test_calculator.py`, `cli.py`

2. **Try running it:**
   ```bash
   python cli.py add 5 3
   ```
   Should show: `8`

3. **Check the artifacts:**
   ```bash
   # Windows
   ls artifacts\superpowers\

   # Mac/Linux
   ls artifacts/superpowers/
   ```

   You should see:
   - `plan.md` - The plan you approved
   - `execution.md` - Step-by-step log of what happened
   - `finish.md` - Final summary

---

## ⚡ Using Parallel Execution (Optional - Makes Things Faster!)

If your plan has **independent steps** (steps that don't depend on each other), you can run them in parallel to save time!

### When to Use Parallel Mode

**Good for parallel:**
- ✅ Adding 3 separate features to different files
- ✅ Creating 3 independent modules
- ✅ Writing tests for 3 different functions

**Not good for parallel:**
- ❌ Steps that build on each other (Step 2 needs Step 1's output)
- ❌ All steps modify the same file
- ❌ Only 1-2 steps total (not worth the overhead)

### How to Use It

**Option 1: Let the AI suggest it**

When you run `/superpowers-execute-plan`, if the AI detects independent steps, it will ask:
```
I notice steps 1, 2, 3 are independent and could run in parallel.
Would you like to use `/superpowers-execute-plan-parallel` for faster execution?
Or continue with sequential execution? (Reply: PARALLEL or SEQUENTIAL)
```

Reply: `PARALLEL`

**Option 2: Use it directly**

After approving your plan, type:
```
/superpowers-execute-plan-parallel
```

### What's Different in Parallel Mode?

**Sequential execution:**
```
Step 1 (5 min) → Step 2 (5 min) → Step 3 (5 min) = 15 minutes total
```

**Parallel execution:**
```
Step 1 (5 min) ┐
Step 2 (5 min) ├─ All run at the same time
Step 3 (5 min) ┘
Total: ~5 minutes (60% faster!)
```

**What you'll see:**
```
Analyzing plan for parallel execution...

Batch 1 (PARALLEL - 3 steps):
- Step 1: Add feature X
- Step 2: Add feature Y
- Step 3: Add feature Z

🤖 Spawning 3 subagents...
Subagent 1: Working on Step 1...
Subagent 2: Working on Step 2...
Subagent 3: Working on Step 3...

✅ Batch 1 completed in 5.2s
Time saved: 10 minutes vs sequential!
```

**Where are the logs?**

Check `artifacts/superpowers/subagents/` - you'll see one log file per subagent showing exactly what each one did.

---

## 🛠️ Troubleshooting

### "Command not found: /superpowers-..."

**Problem:** Antigravity doesn't see the workflows.

**Solution:**
1. Make sure you're in the folder that contains `.agent/`
2. Try running:
   ```
   /superpowers-reload
   ```
3. If that doesn't work, close Antigravity and reopen it in the correct folder

---

### Parallel execution fails with "gemini not found"

**Problem:** You don't have Gemini CLI installed, or it's not in your system PATH.

**Solution for Windows:**

1. **Install Gemini CLI:**
   ```powershell
   npm install -g @google/gemini-cli
   ```

2. **Verify it installed:**
   ```powershell
   gemini --version
   ```

   Should show: `@google/gemini-cli version X.X.X`

3. **If it still says "not found":**
   - Restart PowerShell (npm might have updated your PATH)
   - Check if npm's global bin directory is in your PATH:
     ```powershell
     npm config get prefix
     ```
   - The output should be something like `C:\Users\YourName\AppData\Roaming\npm`
   - Add that path to your system PATH environment variable

4. **Alternative:** Just use sequential execution instead:
   ```
   /superpowers-execute-plan
   ```
   (It's a bit slower but works without Gemini CLI)

**Solution for Mac/Linux:**

1. **Install Gemini CLI:**
   ```bash
   npm install -g @google/gemini-cli
   ```

2. **Verify:**
   ```bash
   which gemini
   ```
   Should show a path like: `/usr/local/bin/gemini`

3. **If not found:**
   - Make sure npm's bin directory is in PATH
   - Try: `echo $PATH` and look for npm's bin folder

---

### The AI starts coding immediately without planning

**Problem:** The AI isn't following the Superpowers rules.

**Solution:**
1. Make sure `.agent/rules/superpowers.md` exists
2. Try running:
   ```
   /superpowers-reload
   ```
3. Start a new Antigravity conversation
4. Explicitly use the workflows:
   ```
   /superpowers-write-plan <your task>
   ```

---

### Artifacts aren't being created

**Problem:** Files aren't being written to `artifacts/superpowers/`.

**Solution:**
1. Check if the folder was created:
   ```bash
   ls artifacts/superpowers/
   ```
2. If it's empty, the AI might not be following the workflow
3. Try explicitly saying:
   ```
   Please follow the superpowers-execute-plan workflow and write artifacts to disk.
   ```

---

### I edited a workflow but nothing changed

**Problem:** Antigravity cached the old version.

**Solution:**
```
/superpowers-reload
```

This forces Antigravity to re-read all `.agent/` files.

---

## 📂 Where Everything Lives

```
your-project/
├── .agent/                          ← The Superpowers framework (copy this!)
│   ├── rules/
│   │   └── superpowers.md          ← Rules the AI must follow
│   ├── workflows/
│   │   ├── superpowers-write-plan.md
│   │   ├── superpowers-execute-plan.md
│   │   └── ...                      ← Slash commands
│   └── skills/
│       ├── superpowers-tdd/
│       ├── superpowers-debug/
│       └── ...                      ← Building blocks for the AI
│
├── artifacts/                       ← Generated outputs (git-ignored)
│   └── superpowers/
│       ├── plan.md                  ← Your approved plan
│       ├── execution.md             ← Step-by-step execution log
│       ├── finish.md                ← Final summary
│       └── subagents/               ← Parallel execution logs
│
├── your-code-here.py               ← Your actual project files
├── tests/                          ← Tests the AI creates
└── README.md                       ← Your project docs
```

---

## 🎓 Learning by Example

### Example 1: Simple Python Script

**Task:** "Create a script that counts words in a text file"

**Commands you'd use:**
```
/superpowers-write-plan Create a Python script that counts words in a text file
→ Review plan
APPROVED
→ AI creates plan

/superpowers-execute-plan
→ AI builds: word_counter.py, test_word_counter.py
→ AI verifies it works
→ Done!
```

**Result:** Working script with tests in ~5 minutes

---

### Example 2: REST API Client

**Task:** "Build a GitHub API client that lists user repos"

**Commands:**
```
/superpowers-brainstorm I want to build a GitHub API client
→ AI asks: Authentication? Rate limiting? Which endpoints?
→ You answer

/superpowers-write-plan Build a GitHub API client with authentication, rate limiting, and repo listing
→ AI creates detailed plan
APPROVED

/superpowers-execute-plan
→ AI implements step-by-step
→ Each step verified
→ Done!
```

**Result:** Production-ready API client with error handling and tests

---

### Example 3: Three Independent Features (Parallel!)

**Task:** "Add logging, config file support, and --verbose flag to my CLI"

**Commands:**
```
/superpowers-write-plan

Add three features to my CLI:
1. Logging to a file
2. Load settings from a config file
3. --verbose flag for detailed output

Each feature should be independent.

→ AI creates plan with 3 independent steps
APPROVED

/superpowers-execute-plan-parallel
→ AI spawns 3 subagents
→ All 3 features built simultaneously
→ 60% faster than sequential!
```

**Result:** All three features done in ~5 minutes instead of ~15 minutes

---

## 🎯 Quick Reference

### Most Common Workflow

```
1. /superpowers-write-plan <describe what you want>
2. Read the plan, type: APPROVED
3. /superpowers-execute-plan
4. Done! Check your code and artifacts/superpowers/finish.md
```

### All Available Commands

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `/superpowers-brainstorm` | Explore ideas with Q&A | When you're not sure exactly what you want |
| `/superpowers-write-plan` | Create a detailed plan | Start of every task |
| `/superpowers-execute-plan` | Build code step-by-step | After approving plan |
| `/superpowers-execute-plan-parallel` | Build independent steps in parallel | When plan has 3+ independent steps |
| `/superpowers-review` | Check code quality | Before finishing, or when debugging |
| `/superpowers-debug` | Systematic debugging | When something's broken |
| `/superpowers-finish` | Create final summary | After everything works |
| `/superpowers-reload` | Reload all workflows/rules | After editing .agent/ files |

---

## 🤝 Contributing

Want to improve this framework? PRs welcome!

**Good ideas for contributions:**
- More language-specific skills (Node/TS, Go, Rust, etc.)
- Additional workflows (git worktree management, branch cleanup, etc.)
- Better parallel execution (smarter dependency detection)
- More E2E demos showing real-world usage
- Better error messages and troubleshooting

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Credits

- **Inspired by:** [obra/superpowers](https://github.com/obra/superpowers) (Claude Superpowers)
- **Adapted for:** Google Antigravity
- **Parallel execution concept:** Based on community discussions about multi-agent workflows

---

## 💡 Tips for Success

1. **Start small:** Try the calculator example first before tackling big projects
2. **Read the plans:** Don't just blindly approve - actually review what the AI suggests
3. **Use parallel mode wisely:** It's faster but harder to debug if something goes wrong
4. **Check artifacts:** The `artifacts/superpowers/` folder tells you exactly what happened
5. **Reload often:** If you edit workflows, always run `/superpowers-reload`
6. **Ask questions:** If the plan doesn't make sense, ask the AI to clarify before approving

Happy coding! 🚀
