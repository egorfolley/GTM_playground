---
name: full-stack-ai-developer
description: 'End-to-end full-stack AI delivery workflow. Use for implementing or evolving features across frontend, backend, data, and LLM/agent logic with tests, validation, and production-ready handoff. Triggers: full-stack, API plus UI, AI feature, agent workflow, integration task, refactor with tests.'
argument-hint: 'Feature goal, constraints, stack, and done criteria'
user-invocable: true
disable-model-invocation: false
---

# Full-Stack AI Developer Workflow

## Outcome
Deliver a working, testable full-stack AI feature from requirements to verified implementation.

## When To Use
- Add or modify a feature spanning API and UI.
- Integrate LLM or agentic behavior into product workflows.
- Improve architecture, reliability, or observability across the stack.
- Execute medium to large implementation tasks with clear completion criteria.

## Inputs To Collect
- Product goal and user outcome.
- Functional and non-functional constraints (latency, cost, privacy, compliance).
- Existing stack and architectural boundaries.
- Acceptance criteria and definition of done.
- Deployment target and rollback expectations.

## Procedure
1. Clarify the task and define success.
- Restate the feature request as concrete deliverables.
- Identify unknowns and ask only blocking clarification questions.
- Convert acceptance criteria into measurable checks.

2. Map existing system behavior.
- Locate relevant frontend views, backend services, data models, and AI/agent modules.
- Trace critical request/data flows and dependencies.
- Note integration seams, risk points, and likely regression areas.

3. Design a thin, incremental implementation plan.
- Prefer the smallest vertical slice that proves value early.
- Break work into independent commits/changesets where possible.
- Include test strategy (unit, integration, E2E) before coding.

4. Implement backend and AI foundations first.
- Update domain logic, API contracts, and persistence models.
- Add or update AI orchestration logic, prompts, tools, and guardrails.
- Ensure input validation, retries/timeouts, and structured error handling.

5. Implement frontend integration.
- Connect UI state and API contracts.
- Handle loading, empty, error, and partial-result states explicitly.
- Keep UX resilient when AI output is delayed or uncertain.

6. Add quality gates.
- Add or update tests nearest to behavior changes.
- Verify deterministic behavior where possible around AI boundaries.
- Confirm observability hooks (logging/metrics/tracing) for critical paths.

7. Validate end-to-end.
- Run targeted tests and linters.
- Execute a realistic flow from user interaction to persisted output.
- Confirm acceptance criteria are met and no major regressions are introduced.

8. Deliver and document.
- Summarize what changed, why, and any tradeoffs.
- Record migration notes, config changes, and operational considerations.
- List follow-up improvements if they are non-blocking.

## Decision Points
- If requirements are ambiguous and block implementation: ask concise clarification questions before coding.
- If the requested scope is broad: ship a minimal vertical slice first, then iterate.
- If AI output quality is unstable: add schema validation, tighter prompting, and fallback behavior.
- If latency or cost is high: reduce context size, cache stable computations, and gate expensive steps.
- If tests are missing in the area: add characterization tests before major refactors.

## Quality Criteria (Definition of Done)
- Feature behavior matches acceptance criteria.
- API and UI are consistent and handle edge states.
- AI pathway is guarded with validation and failure handling.
- Tests cover core happy paths and key failure modes.
- No critical lint/type/test failures remain.
- Change summary includes risks, tradeoffs, and next steps.

## Output Format For Responses
When using this skill, produce outputs in this order:
1. Implementation summary.
2. Files changed and key logic updates.
3. Validation performed and results.
4. Remaining risks and follow-up options.

## Prompt Starters
- /full-stack-ai-developer Build a new feature that adds AI-assisted lead scoring with API + UI.
- /full-stack-ai-developer Refactor the agent pipeline and expose results in the dashboard.
- /full-stack-ai-developer Add retries, guardrails, and observability to an unstable AI endpoint.
