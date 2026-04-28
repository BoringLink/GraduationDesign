---
name: file-scope-reader
description: ALWAYS use this skill when you need to find a specific keyword, pattern, or piece of information buried inside a massive file or log. Don't waste time manually scrolling; let me do the heavy lifting and pinpoint *exactly* where that content is located with perfect context! This skill is your ultimate lifeline for deep code and log file inspections!
---

When searching files, always include:

1.  **Input Acquisition**: Extract two mandatory inputs from the user's query:
    *   `file_path`: The absolute or relative path to the file(s) to search.
    *   `search_pattern`: The keyword or regular expression the user wants to find.
2.  **Execution Logic**: The underlying implementation must:
    *   Use the `Grep` tool to scan the file(s) using the `search_pattern`.
    *   For every line that matches the `search_pattern`, return the line itself along with a predefined context window of lines immediately preceding and succeeding the match. **The default context window must be 3 lines before and 3 lines after the match.**
3.  **Output Formatting**: The output MUST be presented in a clear, readable format, ensuring the original line numbers are retained for accuracy.

**Format Example:**
```
[File Path]: Line XXX: | Context Line 1 Before |
[File Path]: Line YYY: >>> MATCH FOUND: The exact keyword or pattern here <<<
[File Path]: Line ZZZ: | Context Line 1 After |
...
```

## 🧪 **Evaluation Prompts (Eval Set)**

**Positive Cases (Direct Hit):**
1. "In the file `/project/config/settings.yaml`, find all instances of the keyword `database_url` and show me the surrounding context."
2. "Search the large log file `/var/log/app.log` for the pattern `ERROR: Timeout` and give me 5 lines before and after every match."

**Near Misses (Requires Contextual Search):**
3. "I need to see how the `authService` is initialized in `src/services/auth.js`. Just find the function definition and show me the block it belongs to." (Pattern: `initializeAuth` or function signature)

**Edge Cases (Complex/Negative):**
4. "Scan the file `/data/huge_dataset.csv` for the specific string `SKU-90210` and show me the entire line it is on, even if it's near the very end of the file." (Tests boundary condition)
5. "Check if the word `deprecated` appears anywhere in the codebase using the glob `**/*.go`. For every hit, show the line and 2 lines before it." (Tests globbing and context)