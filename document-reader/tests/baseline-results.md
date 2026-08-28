# RED Baseline Results

## Fixture
- Path: `document-reader/tests/fixtures/api-doc-large.md`
- Lines: 811
- Critical content locations: Auth section line 561, error codes line 803–806, Retry-After line 808, X-API-Version line 811

## Checklist
1. Bearer token auth (line >500)
2. Token expiry/refresh (line >500)
3. All four error codes including 402 card_declined (line >800)
4. Retry-After behavior (line >800)
5. X-API-Version header (last line)

---

## Agent 1: coverage scenario

**Prompt:** List every distinct piece of information an engineer needs to build a working API client against the fixture. Be exhaustive.

**Result:** Full capture. Reported Base URL, JSON transport, all 16 endpoints, request body schema, Bearer auth with token acquisition/expiry/refresh, all four error codes, rate limits with Retry-After, and X-API-Version header.

**Missed items:** None.
**Read to EOF:** Yes (inferred from complete coverage).
**Rationalizations:** None.

---

## Agent 2: extraction scenario

**Prompt:** Produce (1) auth scheme and credential supply, (2) every error code with meaning, (3) rate limit behavior, then write a minimal TypeScript fetch wrapper for POST /v1/charges.

**Result:** Captured auth scheme, token acquisition/expiry/refresh, all four error codes, rate limits with Retry-After, and a TypeScript wrapper. **Did not mention X-API-Version header.**

**Missed items:** X-API-Version header (line 811).
**Read to EOF:** Unknown — output is consistent with having read most or all of the file, but versioning was omitted.
**Rationalizations:** None explicit.

---

## Control gate decision

Both agents did NOT capture all checklist items → NO-GO for "delete the skill." Proceed to Task 3 (GREEN rewrite).

The skill must address: agents can extract endpoints, auth, and error codes but still omit versioning and other tail-section constraints when the task framing focuses on a subset of information.
