# Baseline Scenario 3: Multi-Pattern Cross-Reference

**Prompt to run (without skill loaded):** "Where is the application configuration loaded? What environment variables does it use? Trace from config file loading to usage."

**Expected good behavior:**
- Searches for config loading pattern (`load_config`, `config()`, etc.)
- Finds env var references (`process.env`, `os.getenv`, etc.)
- Links config loading to usage sites
- Provides structured cross-reference

**Common failures to watch for:**
- Only finds config loading, not env var usage
- Stops at first match
- No cross-referencing between patterns
