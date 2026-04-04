---
name: crewai-ask-docs
description: Query official CrewAI documentation for current answers. Use when a CrewAI question needs authoritative API details, troubleshooting guidance, newer feature coverage, CLI reference, deployment information, or confirmation beyond the curated local design skills.
---

# Ask CrewAI Docs

Use this skill when the official docs are the best source of truth.

## When To Use

Use this skill if:

- the question is API-specific
- the feature seems newer or less common
- the user is debugging an error
- the curated local skills might be incomplete for the request
- you need to verify exact syntax or configuration

Do not use this skill first when the answer is already clearly covered by:

- `crewai-getting-started`
- `crewai-design-agent`
- `crewai-design-task`

## Docs Workflow

1. Fetch the docs index at `https://docs.crewai.com/llms.txt`
2. Find the most relevant page URL
3. Fetch that page
4. Synthesize the answer
5. Include the docs URL in the response

## Fetch Pattern

Use:

```text
WebFetch: https://docs.crewai.com/llms.txt
```

Then fetch the relevant page:

```text
WebFetch: https://docs.crewai.com/<path-from-index>
```

## Response Rule

Give a direct answer first, then cite the CrewAI docs URL used to confirm it.

## Typical Triggers

- "What parameters does `Crew()` accept?"
- "How do I configure memory?"
- "What CLI commands exist?"
- "How do I deploy a Flow?"
- "Why am I getting this validation error?"

## Related Skills

- `crewai-getting-started`
- `crewai-design-agent`
- `crewai-design-task`
