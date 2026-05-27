# Baseline Scenario 2: Pattern Search in Scoped Directory

**Prompt to run (without skill loaded):** "Find all error handling code in the auth module. This includes try/catch blocks, error classes, error logging, and validation error responses."

**Expected good behavior:**
- Scopes search to `auth/` directory
- Uses multiple patterns (catch, throw, Error, etc.)
- Groups results by category
- Includes context lines

**Common failures to watch for:**
- Searches entire codebase instead of scoping
- Single pattern only
- Raw output without grouping/context
