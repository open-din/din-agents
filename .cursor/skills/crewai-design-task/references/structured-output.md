# Structured Output Reference

How to get structured, typed output from LLM calls, agents, tasks, and crews.

---

## The Four Levels

Structured output works differently at each abstraction level:

| Level | Parameter | Returns | Access Pattern |
|---|---|---|---|
| `LLM.call()` | `response_format=Model` | Pydantic object directly | `result.field` |
| `Agent.kickoff()` | `response_format=Model` | `LiteAgentOutput` wrapper | `result.pydantic.field` |
| `Task` | `output_pydantic=Model` | `TaskOutput` wrapper | `task.output.pydantic.field` |
| `Crew.kickoff()` | (via last task) | `CrewOutput` wrapper | `result.pydantic.field` |

---

## 1. LLM.call() — Direct Pydantic Return

```python
from crewai import LLM
from pydantic import BaseModel

class Sentiment(BaseModel):
    label: str
    confidence: float
    reasoning: str

llm = LLM(model="openai/gpt-4o")

result = llm.call(
    messages=[{"role": "user", "content": f"Analyze sentiment: {text}"}],
    response_format=Sentiment,
)

print(result.label)
print(result.confidence)
```

---

## 2. Agent.kickoff() — LiteAgentOutput Wrapper

```python
from crewai import Agent
from pydantic import BaseModel

class ResearchFindings(BaseModel):
    main_points: list[str]
    sources: list[str]
    confidence: float

researcher = Agent(
    role="Researcher",
    goal="Research topics thoroughly",
    backstory="...",
    tools=[SerperDevTool()],
)

result = researcher.kickoff(
    "Research the latest AI developments",
    response_format=ResearchFindings,
)

print(result.pydantic.main_points)
print(result.pydantic.sources)
print(result.raw)
print(result.usage_metrics)
```

---

## 3. Task — output_pydantic / output_json

### output_pydantic

```python
from pydantic import BaseModel
from crewai import Task

class BlogPost(BaseModel):
    title: str
    content: str
    tags: list[str]

task = Task(
    description="Write a blog post about {topic}",
    expected_output="A blog post with title, content, and relevant tags.",
    agent=writer,
    output_pydantic=BlogPost,
)
```

**Access after crew runs:**

```python
result = crew.kickoff(inputs={"topic": "AI"})

result.pydantic.title
result.pydantic.tags

task_output = result.tasks_output[0]
task_output.pydantic.title
task_output.raw
```

### output_json

```python
task = Task(
    description="Write a blog post about {topic}",
    expected_output="A JSON object with title, content, and tags fields.",
    agent=writer,
    output_json=BlogPost,
)
```

**Access:**

```python
result = crew.kickoff(inputs={"topic": "AI"})

result.json_dict
result.json_dict["title"]
```

### Key Difference

- `output_pydantic` -> validated Pydantic model instance -> access via `.pydantic`
- `output_json` -> parsed dict from JSON string -> access via `.json_dict`
- Both use a Pydantic model to define the schema
- `expected_output` is always a human-readable string, never a class reference

---

## 4. Crew.kickoff() — CrewOutput

The crew's output comes from the **last task** in the sequence:

```python
result = crew.kickoff(inputs={"topic": "AI"})

result.raw
result.pydantic
result.json_dict

result.tasks_output
result.tasks_output[0].raw
result.tasks_output[1].pydantic

result.token_usage
```

---

## Pydantic Model Design Tips

### Keep Models Simple

```python
class Report(BaseModel):
    title: str
    summary: str
    key_findings: list[str]
    confidence: float
```

Avoid deeply nested models unless truly necessary.

### Use Field Descriptions

```python
from pydantic import BaseModel, Field

class Report(BaseModel):
    title: str = Field(description="A concise, descriptive title")
    findings: list[str] = Field(description="List of 3-5 key findings")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
```

### Provide Defaults For Optional Fields

```python
class Analysis(BaseModel):
    summary: str
    risk_level: str = "medium"
    sources: list[str] = []
    notes: str | None = None
```

---

## Common Pitfalls

| Mistake | Fix |
|---|---|
| `expected_output="BlogPost"` | Use a descriptive string such as `"A blog post with title, content, and tags"` |
| Accessing `result.title` on CrewOutput | Use `result.pydantic.title` |
| Deeply nested Pydantic models | Flatten the model |
| Mixing `output_pydantic` and `output_json` on one task | Pick one |
| No `response_format` on `LLM.call()` | Without it, `LLM.call()` returns a plain string |
| Agent retries endlessly | Simplify the model or use a more capable model |
