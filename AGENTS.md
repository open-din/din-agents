# AGENTS — din-agents (CONTROL PLANE)

## CORE RULE
Route to the correct repository. Load MINIMUM context. Avoid cross-repo unless required.

---

## 1. ROLE

din-agents = orchestration layer

- routes tasks across:
  - react-din (API)
  - din-core (runtime)
  - din-studio (UI)

Does NOT own domain logic.

---

## 2. ROUTING (CRITICAL)

Map task → repo:

- "component / API / schema" → react-din
- "runtime / compiler / validation" → din-core
- "UI / editor / workflow / MCP" → din-studio
- "automation / routing / crews" → din-agents

If unclear → choose smallest scope

---

## 3. HOOKS (MANDATORY)

### HOOK: ROUTE_TASK
IF task received:

1. classify task
2. select ONE repo
3. STOP loading others

---

### HOOK: CROSS_REPO
IF task involves:

- schema
- serialization
- runtime + UI

THEN:

1. identify contract owner (source of truth)
2. update owner FIRST
3. propagate to consumers

---

### HOOK: REPO_PROFILE

LOAD ONLY:
- src/din_agents/shared/repo_profiles.py

USE:
- repo-specific commands
- quality gates

---

### HOOK: FLOW_EXECUTION

IF task uses crew/flow:

LOAD ONLY:
- src/din_agents/flow.py
- relevant crew module

---

### HOOK: DOCS

IF missing info:

LOAD (max 2):
1. docs/summaries
2. README / FlowArchitecture.md
3. docs/generated

STOP when sufficient

---

## 4. HARD CONSTRAINTS

- ALWAYS start with 1 repo
- NEVER load multiple repos by default
- cross-repo ONLY if contract requires

---

### NEVER:

- implement domain logic here
- duplicate logic from other repos
- modify multiple repos blindly

---

## 5. EXECUTION LOOP

1. classify task
2. route to repo
3. load minimal context
4. execute
5. validate in target repo

---

## 6. CONTEXT LIMITS

- max 1 repo (default)
- max 2 files
- NEVER scan repos
- NEVER load all repos

---

## 7. SELF-OPTIMIZATION

Continuously:

- reduce repo scope
- drop unused repos
- minimize file loading

If multiple repos loaded → reduce

---

## 8. LOAD DEEP CONTEXT ONLY IF

- routing unclear
- contract ambiguous
- failing validation

---

## 9. VALIDATION

uv run pytest  
uv run ruff check src  

(optional) generate-docs