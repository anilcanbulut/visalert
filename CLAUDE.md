## Code Editing Rules

### Preserve Explanatory Comments
- Never remove comments that explain logic, reasoning, or context
- Keep TODO, FIXME, NOTE, and similar annotations intact
- Preserve documentation comments (JSDoc, docstrings, etc.)

### Remove Only Truly Unnecessary Code
- Delete unused variables, imports, and dead code blocks
- Remove redundant logic or duplicate implementations
- Clean up commented-out code only if it serves no documentary purpose

### When to Edit vs When to Answer

**Do NOT edit code when:**
- The user is asking a question about how something works
- The user wants clarification or explanation
- The user is exploring options or asking for opinions
- The request is phrased as a question without explicit edit intent

**DO edit code when:**
- The user explicitly requests changes (e.g., "fix this", "refactor this", "add X")
- The user provides code and asks you to implement something specific
- The instruction clearly implies modification (e.g., "make this faster", "update the logic")

When uncertain, ask for clarification rather than making changes.

---

## Code Style Requirements

### Avoid AI-Like Patterns
- Do not use decorative comment blocks with excessive symbols (`=====`, `-----`, `*****`)
- Never add emojis in code or comments
- Avoid overly verbose or redundant inline comments
- Write comments as a human developer would—concise and purposeful

### Match Existing Style
- Follow the formatting conventions already present in the codebase
- Match indentation, naming conventions, and comment style
- Preserve the original author's voice in comments when editing
- Always write clean code. The readability of the code is more important than the brevity of the code. 
- Do not write static texts in the trading prompt. Always try to use the parameters in the .yaml files
  if necessary to be used. The code should be dynamic and should not have any hard coded values.

---

## Before Writing or Using Code

### API and Library Usage
- When using any API method, library function, or external tool, search the internet first to verify:
  - Correct method signatures and parameters
  - Current best practices
  - Deprecation status
  - Breaking changes in recent versions
- Do not rely on potentially outdated knowledge

### Check for Existing Implementations
Before writing new code:
1. Ask if similar functionality already exists in the codebase
2. Search for related methods, utilities, or helpers
3. Suggest reusing or extending existing code when appropriate
4. Only create new implementations when truly necessary

---

## Response Behavior

- For questions: Provide clear, direct answers without code modifications
- For edit requests: Make precise, minimal changes that accomplish the goal
- Always explain what you changed and why (briefly)
- If a request is ambiguous, clarify intent before proceeding