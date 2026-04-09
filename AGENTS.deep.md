# AGENTS — din-agents (DEEP CONTEXT)

## PURPOSE
Loaded ONLY when routing or orchestration is unclear.

---

## 1. FLOW ARCHITECTURE

- main.py → entrypoint
- flow.py → orchestration
- crews → repo-specific logic

---

## 2. REPO PROFILES

src/din_agents/shared/repo_profiles.py:

- defines commands per repo
- defines quality gates
- used for execution

---

## 3. CROSS-REPO STRATEGY

When multiple repos required:

1. identify source of truth
2. update owner repo
3. update dependents
4. validate each repo

---

## 4. DOCUMENTATION FLOW

1. README.md
2. docs/FlowArchitecture.md
3. ../docs/summaries/din-agents-api.md
4. docs/generated (max 2)
5. src/** (last)

---

## 5. CODE READING POLICY

- docs > summaries > source
- NEVER scan src/
- read only exact module

---

## 6. DOCUMENTATION RULES

- Google-style docstrings required
- run generate-docs after change

---

## 7. CONTEXT STRATEGY

- prefer single repo execution
- avoid cross-repo loading
- route before reading

---

## 8. FAILURE STRATEGY

If unclear:

- do NOT load all repos
- route to most likely repo
- document assumption