# Test Scenarios for code-review

## Scenario 1: Casual Prompt with Security Vulnerability (Trigger & Rigor)

**Prompt:**
> "Hey, quick check on this Python function before I put it in my script:
> ```python
> def fetch_user_data(user_input):
>     query = f"SELECT * FROM users WHERE username = '{user_input}'"
>     return db.execute(query).fetchall()
> ```"

**Expected Behavior:**
- Agent activates the `code-review` skill immediately despite casual phrasing ("quick check").
- Agent executes the structured 6-dimension evaluation pass.
- Agent identifies the 🔴 **SQL Injection** vulnerability as the top critical issue.
- Agent provides the exact corrected parameterized query code block.
- Agent includes the mandatory **"What's Working Well"** section.
- Agent presents findings using the standard output template.

---

## Scenario 2: Performance Optimization with Unhandled Edge Cases (Dimension Coverage)

**Prompt:**
> "How can I speed up this JavaScript function? It's running slowly on large arrays:
> ```javascript
> function findDuplicates(arr) {
>     let duplicates = [];
>     for (let i = 0; i < arr.length; i++) {
>         for (let j = i + 1; j < arr.length; j++) {
>             if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
>                 duplicates.push(arr[i]);
>             }
>         }
>     }
>     return duplicates;
> }
> ```"

**Expected Behavior:**
- Agent identifies the O(n²) loop complexity and offers an O(n) `Set`-based solution.
- Agent evaluates non-performance dimensions: checks for unhandled edge cases (e.g., `arr` being `null`/`undefined`, non-array types,NaN comparison).
- Agent presents corrected code for the O(n) fix.
- Agent includes specific positive feedback in "What's Working Well".

---

## Scenario 3: Negative Trigger — Plan Compliance (Routing Test)

**Prompt:**
> "Can you check my git diff against `docs/plans/2026-08-15-auth.md` to see if I missed any acceptance criteria or tasks?"

**Expected Behavior:**
- Agent **does NOT** use `code-review`.
- Agent routes to the `reviewing-implementation` skill instead, as the request is about plan compliance rather than code quality/bug evaluation.

---

## Scenario 4: Negative Trigger — External Review Comments (Routing Test)

**Prompt:**
> "A senior dev left 5 review comments on my pull request. Here are the comments: [list]. How should I address them?"

**Expected Behavior:**
- Agent **does NOT** perform a fresh code review using `code-review`.
- Agent routes to the `receiving-code-review` skill to evaluate and respond to external feedback.
