# Web Fetching — Test Scenarios

## Scenario 1: Search the web (no specific URL)

**User says:**
> "Can you search for 'python async await best practices' and summarize what you find?"

**Expected behavior with skill:**
- Does NOT attempt to call a non-existent `websearch` tool
- Uses `webfetch` with a search engine URL to perform the search
- Fetches at least one result page and summarizes the findings
- Handles the response gracefully

## Scenario 2: Fetch specific documentation

**User says:**
> "Get the API documentation from https://jsonplaceholder.typicode.com/guide/"

**Expected behavior with skill:**
- Uses `webfetch` with the exact URL
- Uses appropriate format (markdown or html)
- Retrieves content successfully
- Presents the relevant information

## Scenario 3: Error handling - URL returns 404

**User says:**
> "Fetch https://jsonplaceholder.typicode.com/nonexistent-page for me"

**Expected behavior with skill:**
- Attempts to fetch the URL
- On failure, retries once
- Reports the 404 error clearly to the user
- Does NOT try to use websearch as a fallback
- Suggests checking the URL or finding the correct one

## Scenario 4: Code example from GitHub

**User says:**
> "Show me the content of https://raw.githubusercontent.com/example/repo/main/README.md"

**Expected behavior with skill:**
- Uses `webfetch` with `format="text"` for raw file content
- Retrieves and displays the content
- Correctly identifies raw code files need text format, not markdown

## Scenario 5: Fetch with specific format

**User says:**
> "I need the HTML version of https://example.com — fetch it as HTML"

**Expected behavior with skill:**
- Uses `webfetch` with `format="html"` parameter
- Fetches the URL with the specified format
- Returns the content
