# Graph Report - /Users/veacks/Sites/open-din/din-agents  (2026-04-12)

## Corpus Check
- Corpus is ~19,327 words - fits in a single context window. You may not need a graph.

## Summary
- 399 nodes · 468 edges · 53 communities detected
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.53)
- Token cost: 12,000 input · 1,800 output

## Community Hubs (Navigation)
- [[_COMMUNITY_flow.py|flow.py]]
- [[_COMMUNITY_Custom deterministic tools for|Custom deterministic tools for]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_repo_profiles.py|repo_profiles.py]]
- [[_COMMUNITY_din_core_audio_tasks.py|din_core_audio_tasks.py]]
- [[_COMMUNITY_task_guardrails.py|task_guardrails.py]]
- [[_COMMUNITY_test_din_core_audio_tasks.py|test_din_core_audio_tasks.py]]
- [[_COMMUNITY_rules.py|rules.py]]
- [[_COMMUNITY_runtime_prefs.py|runtime_prefs.py]]
- [[_COMMUNITY_model_routing.py|model_routing.py]]
- [[_COMMUNITY__out|_out]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_RepoFileReadTool|RepoFileReadTool]]
- [[_COMMUNITY_test_runtime_prefs.py|test_runtime_prefs.py]]
- [[_COMMUNITY_test_routing.py|test_routing.py]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_Per-repo CrewAI crews|Per-repo CrewAI crews]]
- [[_COMMUNITY_test_workspace_contracts.py|test_workspace_contracts.py]]
- [[_COMMUNITY_cli_prefs.py|cli_prefs.py]]
- [[_COMMUNITY_test_model_routing.py|test_model_routing.py]]
- [[_COMMUNITY_test_repo_file_read_tool.py|test_repo_file_read_tool.py]]
- [[_COMMUNITY_test_repo_profiles.py|test_repo_profiles.py]]
- [[_COMMUNITY_crew_tools.py|crew_tools.py]]
- [[_COMMUNITY_din-agent sample requests hub|din-agent sample requests hub]]
- [[_COMMUNITY__read|_read]]
- [[_COMMUNITY_test_flow_crew_inputs.py|test_flow_crew_inputs.py]]
- [[_COMMUNITY_test_report_assembly.py|test_report_assembly.py]]
- [[_COMMUNITY_test_crew_tool_budgets.py|test_crew_tool_budgets.py]]
- [[_COMMUNITY_test_flow_rate_limit.py|test_flow_rate_limit.py]]
- [[_COMMUNITY_test_repo_file_write_tool.py|test_repo_file_write_tool.py]]
- [[_COMMUNITY_test_flow_report.py|test_flow_report.py]]
- [[_COMMUNITY_resolved_path_under_repo|resolved_path_under_repo]]
- [[_COMMUNITY_Project skills map|Project skills map]]
- [[_COMMUNITY_test_repo_paths.py|test_repo_paths.py]]
- [[_COMMUNITY_test_dedupe_exact_double_markdown|test_dedupe_exact_double_markdown]]
- [[_COMMUNITY_test_select_quality_gates_returns_expecte...|test_select_quality_gates_returns_expecte...]]
- [[_COMMUNITY_search.js|search.js]]
- [[_COMMUNITY_WORKSPACE_MANIFEST routing source|WORKSPACE_MANIFEST routing source]]
- [[_COMMUNITY_design-agent SKILL|design-agent SKILL]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_Crew package surface|Crew package surface]]
- [[_COMMUNITY_Package exports|Package exports]]
- [[_COMMUNITY_LiteLLM model routing|LiteLLM model routing]]
- [[_COMMUNITY_Repo-scoped file write tools|Repo-scoped file write tools]]
- [[_COMMUNITY_AGENTS.md load order|AGENTS.md load order]]
- [[_COMMUNITY_Route to din-agents|Route to din-agents]]
- [[_COMMUNITY_Ownership boundaries|Ownership boundaries]]
- [[_COMMUNITY_main.py to flow.py pipeline|main.py to flow.py pipeline]]
- [[_COMMUNITY_Documentation reading policy|Documentation reading policy]]
- [[_COMMUNITY_din-core audio task reports|din-core audio task reports]]

## God Nodes (most connected - your core abstractions)
1. `DinControlPlaneFlow` - 15 edges
2. `RoutingDecision` - 13 edges
3. `_out()` - 9 edges
4. `TruncatingCrew` - 9 edges
5. `route_request()` - 9 edges
6. `Custom deterministic tools for the DIN control plane.` - 7 edges
7. `RepoFileReadTool` - 7 edges
8. `_build_profile()` - 7 edges
9. `main()` - 6 edges
10. `RepoFileWriteTool` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Control-plane crew input shaping.` --uses--> `DinControlPlaneFlow`  [INFERRED]
  tests/test_flow_crew_inputs.py → src/din_agents/flow.py
- `Flow report assembly (no LLM).` --uses--> `DinControlPlaneFlow`  [INFERRED]
  tests/test_flow_report.py → src/din_agents/flow.py
- `Merged control plane markdown report` --semantically_similar_to--> `control-plane-report output`  [INFERRED] [semantically similar]
  output/control-plane-report.md → docs/FlowArchitecture.md
- `Cross-repo routing examples` --semantically_similar_to--> `Cross-repo coordination strategy`  [INFERRED] [semantically similar]
  din-agent/examples/cross-repo.md → AGENTS.deep.md
- `Sequential task context truncation.` --uses--> `DinCoreCrew`  [INFERRED]
  tests/test_crew_context.py → src/din_agents/crews/din_core/din_core_crew.py

## Hyperedges (group relationships)
- **din-agents portable skills cluster** — skill_router, skill_ask_docs, skill_getting_started, skill_design_task, skill_design_agent [EXTRACTED 0.90]
- **Per-repo example request files** — ex_din_studio, ex_din_core, ex_react_din [EXTRACTED 0.95]

## Communities

### Community 0 - "flow.py"
Cohesion: 0.09
Nodes (31): ControlPlaneState, _crew_tasks_markdown(), DinControlPlaneFlow, _estimate_prompt_budget_chars(), _is_input_tpm_rate_limit(), _rate_limit_wait_seconds(), CrewAI Flow wiring that routes user requests across per-repo crews., Return a deterministic markdown brief when a repo crew fails guardrail validatio (+23 more)

### Community 1 - "Custom deterministic tools for"
Cohesion: 0.07
Nodes (21): BaseTool, ChangeBriefTool, ChangeBriefToolInput, Input schema for ChangeBriefTool., Builds a routing and escalation brief from a raw user request., Custom deterministic tools for the DIN control plane., QualityGateTool, QualityGateToolInput (+13 more)

### Community 2 - "Crew package surface"
Cohesion: 0.11
Nodes (14): Crew, _get_context(), CrewAI sequential context limits — avoid multi-task input TPM spikes.  CrewAI's, Cap length of aggregated prior-task text injected into the next task., Same as ``Crew``, but caps default sequential context size., truncate_sequential_context(), TruncatingCrew, DinCoreCrew (+6 more)

### Community 3 - "repo_profiles.py"
Cohesion: 0.15
Nodes (20): BaseModel, _build_profile(), get_repo_profile(), get_repo_profiles(), _load_workspace_manifest(), _quality_gate_name(), QualityGate, Manifest-driven repo profiles for DIN workspace routing and tool constraints. (+12 more)

### Community 4 - "din_core_audio_tasks.py"
Cohesion: 0.16
Nodes (16): AudioTaskSpec, build_request(), get_task(), list_tasks(), main(), Executable din-core audio backlog: compose control-plane requests per-task., Run every backlog task in order (each full control-plane kickoff).      ``pause_, One implementable audio surface for din-core. (+8 more)

### Community 5 - "task_guardrails.py"
Cohesion: 0.17
Nodes (16): _as_message_dict(), clear_din_core_guardrail_echo(), din_core_require_tools_and_markdown(), _has_path_route_fingerprints(), _output_text(), Programmatic CrewAI task guardrails for thin or tool-skipping agent outputs.  No, True if both required tools appear in structured tool_calls or tool-result messa, Match Path:/Route: as emitted by tools, allowing markdown bullets or bold. (+8 more)

### Community 6 - "test_din_core_audio_tasks.py"
Cohesion: 0.13
Nodes (3): Tests for din-core audio backlog helpers., EOF on input() ends the backlog after the first task., test_run_all_sequential_prompt_stops_on_eof()

### Community 7 - "rules.py"
Cohesion: 0.21
Nodes (14): _extract_repo_mentions(), _match_contract_repos(), _mentions_multi_repo_scope(), _mentions_repo_tooling(), _normalize_repo_hint(), Heuristic router and quality command selector for multi-repo DIN requests., Route to one repo by default and escalate only for shared contracts or explicit, Map repo ids to ordered shell commands from each repo profile. (+6 more)

### Community 8 - "runtime_prefs.py"
Cohesion: 0.16
Nodes (13): any_anthropic_route_enabled(), compact_prompts_enabled(), env_truthy(), max_repo_read_tool_chars(), max_sequential_task_context_chars(), pre_crew_sleep_seconds(), Environment-driven toggles for prompt size, pacing, and CLI ergonomics., True when any configured model route targets Anthropic. (+5 more)

### Community 9 - "model_routing.py"
Cohesion: 0.21
Nodes (13): agent_llm_kwargs(), _anthropic_native_tools_enabled(), _configure_llm(), get_function_calling_llm(), get_llm(), get_model(), LiteLLM-compatible model routing via environment variables.  CrewAI resolves com, Anthropic native tool calling is opt-in until CrewAI/LiteLLM final-answer calls (+5 more)

### Community 10 - "_out"
Cohesion: 0.33
Nodes (10): _out(), Mentioning tools in assistant prose must not satisfy the guard (prompts repeat t, test_execution_brief_guard_prepends_path_and_route_echo(), test_execution_brief_guard_rejects_short_non_markdown_output(), test_guard_fails_on_intent_only_answer(), test_guard_passes_when_path_route_markdown_bold(), test_guard_passes_when_tool_fingerprints_embedded(), test_guard_passes_when_tool_names_only_in_plain_text_messages_fail_until_structured() (+2 more)

### Community 11 - "Crew package surface"
Cohesion: 0.2
Nodes (2): plan_studio_execution(), studio_brief_runner()

### Community 12 - "RepoFileReadTool"
Cohesion: 0.24
Nodes (7): make_repo_file_read_tool(), Scoped file read: one CrewAI tool instance per repo (din_core, react_din, din_st, Arguments for reading from a single DIN checkout., Reads are limited to ``get_repo_profile(allowed_repo_id).path``., Build a reader bound to one DIN sibling repo., RepoFileReadInput, RepoFileReadTool

### Community 13 - "test_runtime_prefs.py"
Cohesion: 0.22
Nodes (1): Runtime environment toggles.

### Community 14 - "test_routing.py"
Cohesion: 0.22
Nodes (0): 

### Community 15 - "Crew package surface"
Cohesion: 0.25
Nodes (2): plan_rust_validation(), rust_brief_runner()

### Community 16 - "Crew package surface"
Cohesion: 0.25
Nodes (2): library_brief_runner(), plan_library_validation()

### Community 17 - "Per-repo CrewAI crews"
Cohesion: 0.22
Nodes (9): Per-repo CrewAI crews, DinControlPlaneFlow, control-plane-report output, route_request / select_quality_gates, ControlPlaneState, Merged control plane markdown report, DIN Agents control plane, CrewAI orchestration (+1 more)

### Community 18 - "test_workspace_contracts.py"
Cohesion: 0.39
Nodes (4): _line_count(), test_route_cards_stay_compact(), test_summary_and_api_summary_budgets_stay_compact(), _word_count()

### Community 19 - "cli_prefs.py"
Cohesion: 0.25
Nodes (7): cli_verbose(), mcp_task_scope_guard(), CLI ergonomics: quiet runs and stricter task prompts for terminal/CI use., False when DIN_AGENTS_QUIET is set (1/true/yes); reduces Crew/agent terminal noi, Merge shared CLI discipline into a CrewAI task config loaded from YAML., Extra description suffix for the MCP review task only., with_cli_task_config()

### Community 20 - "test_model_routing.py"
Cohesion: 0.33
Nodes (0): 

### Community 21 - "test_repo_file_read_tool.py"
Cohesion: 0.33
Nodes (0): 

### Community 22 - "test_repo_profiles.py"
Cohesion: 0.33
Nodes (0): 

### Community 23 - "crew_tools.py"
Cohesion: 0.33
Nodes (5): analysis_tools(), execution_tools(), Shared CrewAI tool lists tuned for prompt size and repo-scoped execution., Minimal analysis toolkit: targeted repo reads only., Execution toolkit: targeted reads and optional writes.      Quality gates are in

### Community 24 - "din-agent sample requests hub"
Cohesion: 0.33
Nodes (6): Cross-repo coordination strategy, din-agent sample requests hub, Cross-repo routing examples, din-core example prompts, din-studio example prompts, react-din example prompts

### Community 25 - "_read"
Cohesion: 0.7
Nodes (4): _read(), test_din_core_prompt_contract_contains_expected_agents_and_tasks(), test_din_studio_prompt_contract_contains_expected_agents_and_tasks(), test_react_din_prompt_contract_contains_expected_agents_and_tasks()

### Community 26 - "test_flow_crew_inputs.py"
Cohesion: 0.4
Nodes (1): Control-plane crew input shaping.

### Community 27 - "test_report_assembly.py"
Cohesion: 0.4
Nodes (1): Report assembly helpers (no LLM).

### Community 28 - "test_crew_tool_budgets.py"
Cohesion: 0.5
Nodes (3): Prompt-budget regressions for repo-scoped toolsets., test_analysis_tools_are_smaller_than_execution_tools(), _tool_desc_chars()

### Community 29 - "test_flow_rate_limit.py"
Cohesion: 0.4
Nodes (1): Rate-limit backoff helpers on the control-plane flow.

### Community 30 - "test_repo_file_write_tool.py"
Cohesion: 0.5
Nodes (0): 

### Community 31 - "test_flow_report.py"
Cohesion: 0.5
Nodes (1): Flow report assembly (no LLM).

### Community 32 - "resolved_path_under_repo"
Cohesion: 0.5
Nodes (3): Safe path resolution for sibling-repo file tools., Return an absolute path inside ``repo_root``, or raise ValueError., resolved_path_under_repo()

### Community 33 - "Project skills map"
Cohesion: 0.5
Nodes (4): Project skills map, ask-docs SKILL, getting-started SKILL, skills-router SKILL

### Community 34 - "test_repo_paths.py"
Cohesion: 0.67
Nodes (0): 

### Community 35 - "test_dedupe_exact_double_markdown"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "test_select_quality_gates_returns_expecte..."
Cohesion: 1.0
Nodes (0): 

### Community 37 - "search.js"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "WORKSPACE_MANIFEST routing source"
Cohesion: 1.0
Nodes (2): WORKSPACE_MANIFEST routing source, Repo purpose summary

### Community 39 - "design-agent SKILL"
Cohesion: 1.0
Nodes (2): design-agent SKILL, design-task SKILL

### Community 40 - "Crew package surface"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Crew package surface"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Crew package surface"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Crew package surface"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Package exports"
Cohesion: 1.0
Nodes (0): 

### Community 45 - "LiteLLM model routing"
Cohesion: 1.0
Nodes (1): LiteLLM model routing

### Community 46 - "Repo-scoped file write tools"
Cohesion: 1.0
Nodes (1): Repo-scoped file write tools

### Community 47 - "AGENTS.md load order"
Cohesion: 1.0
Nodes (1): AGENTS.md load order

### Community 48 - "Route to din-agents"
Cohesion: 1.0
Nodes (1): Route to din-agents

### Community 49 - "Ownership boundaries"
Cohesion: 1.0
Nodes (1): Ownership boundaries

### Community 50 - "main.py to flow.py pipeline"
Cohesion: 1.0
Nodes (1): main.py to flow.py pipeline

### Community 51 - "Documentation reading policy"
Cohesion: 1.0
Nodes (1): Documentation reading policy

### Community 52 - "din-core audio task reports"
Cohesion: 1.0
Nodes (1): din-core audio task reports

## Knowledge Gaps
- **94 isolated node(s):** `Mentioning tools in assistant prose must not satisfy the guard (prompts repeat t`, `Runtime environment toggles.`, `Report assembly helpers (no LLM).`, `Tests for din-core audio backlog helpers.`, `EOF on input() ends the backlog after the first task.` (+89 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `test_dedupe_exact_double_markdown`** (2 nodes): `test_dedupe_exact_double_markdown()`, `test_report_dedupe.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `test_select_quality_gates_returns_expecte...`** (2 nodes): `test_select_quality_gates_returns_expected_commands_for_each_repo()`, `test_quality_gates.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `search.js`** (2 nodes): `search.js`, `e()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `WORKSPACE_MANIFEST routing source`** (2 nodes): `WORKSPACE_MANIFEST routing source`, `Repo purpose summary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `design-agent SKILL`** (2 nodes): `design-agent SKILL`, `design-task SKILL`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crew package surface`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crew package surface`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crew package surface`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Crew package surface`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Package exports`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `LiteLLM model routing`** (1 nodes): `LiteLLM model routing`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Repo-scoped file write tools`** (1 nodes): `Repo-scoped file write tools`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `AGENTS.md load order`** (1 nodes): `AGENTS.md load order`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Route to din-agents`** (1 nodes): `Route to din-agents`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Ownership boundaries`** (1 nodes): `Ownership boundaries`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `main.py to flow.py pipeline`** (1 nodes): `main.py to flow.py pipeline`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Documentation reading policy`** (1 nodes): `Documentation reading policy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `din-core audio task reports`** (1 nodes): `din-core audio task reports`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RoutingDecision` connect `flow.py` to `repo_profiles.py`, `rules.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `DinControlPlaneFlow` connect `flow.py` to `test_flow_crew_inputs.py`, `test_flow_report.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `DinControlPlaneFlow` (e.g. with `Control-plane crew input shaping.` and `Flow report assembly (no LLM).`) actually correct?**
  _`DinControlPlaneFlow` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `RoutingDecision` (e.g. with `ControlPlaneState` and `DinControlPlaneFlow`) actually correct?**
  _`RoutingDecision` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TruncatingCrew` (e.g. with `DinStudioCrew` and `Crew specialized in din-studio ownership and validation.`) actually correct?**
  _`TruncatingCrew` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Mentioning tools in assistant prose must not satisfy the guard (prompts repeat t`, `Runtime environment toggles.`, `Report assembly helpers (no LLM).` to the rest of the system?**
  _94 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `flow.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._