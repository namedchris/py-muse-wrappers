# Claude Behavioral Guidelines

## Core Principles

### 1. Only Do What Is Explicitly Requested
- Do not anticipate future needs
- Do not add extra features, methods, or functionality beyond what is asked
- Do not add error handling, validation, or edge cases unless specifically requested
- When asked to create something, create only that thing

**Bad Example:**
```
User: "add a callback to Button"
Claude: *adds callback, level_callback, channel_callback, and extra helper methods*
```

**Good Example:**
```
User: "add a callback to Button"
Claude: *adds only callback parameter*
```

### 2. Write Simple, Concise Code
- Prefer simpler solutions over complex ones
- Less code is better than more code
- Don't over-engineer
- Avoid unnecessary abstractions or classes

**Bad Example:**
```python
# 100+ lines of mock infrastructure for a simple test
```

**Good Example:**
```python
# 20 lines that test the actual functionality
```

### 3. Assume Current Project State
- Always work with the actual current state of the project
- When uncertain about file locations or structure, use tools (Glob, Read) to verify
- Don't rely on cached mental models of the project structure
- If something seems unclear, check the current state rather than assuming

### 4. Be Direct and Minimal
- Don't add verbose docstrings unless requested
- Don't add type hints unless they're already in use
- Don't add logging unless requested
- Don't add comments unless the code needs explanation

### 5. Testing Code Guidelines
- Don't use global variables
- Use simple data structures (lists, dicts) to track state
- Keep test code minimal and focused on what's being tested

## Communication Style

- Be concise
- Ask clarifying questions when truly uncertain
- Don't apologize excessively
- Get to the point
