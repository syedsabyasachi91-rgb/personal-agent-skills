# Baseline Scenario 4: Embedded Multi-Language Search

**Prompt to run (without skill loaded):** "There's a Python script at app.py that generates HTML using f-strings. Find all `<button>` elements with class `submit-btn` in it. Show me file path, line numbers, and surrounding context."

**Expected good behavior:**
- Does NOT use `-t py` (which filters by Python syntax and may miss string content)
- Uses `rg -rn -C 5 "submit-btn" app.py` (plain text, no type flag)
- Reports the host file with the right line numbers
- Shows enough context to understand the f-string embedding

**Common failures to watch for:**
- Uses `-t py` and misses matches inside string literals
- Uses `grep` without context flags
- Doesn't find anything because they filtered by language type
- Reports the wrong file or none at all
