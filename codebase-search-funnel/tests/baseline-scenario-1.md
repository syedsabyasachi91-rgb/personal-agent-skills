# Baseline Scenario 1: Find Function Definition

**Prompt to run (without skill loaded):** "Find the definition of the `connect` function in this codebase. Show me the file path, line number, and the full function signature."

**Expected good behavior:**
- Uses `rg` or `grep` with context (-C flag)
- Returns file:line + function signature + surrounding code
- Distinguishes definition from usages/calls

**Common failures to watch for:**
- Reads files one-by-one
- Uses grep without -C context
- Returns only the line without understanding
