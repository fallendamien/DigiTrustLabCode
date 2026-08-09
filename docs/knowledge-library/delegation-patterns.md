# Delegation Patterns

Simple reference for deciding when Sol should use one Luna worker or several workers in parallel.

## The simple idea

Think of 🧠 Sol as the teacher and the subagents as helpers.

Sol remains responsible for the full task: understanding the request, coordinating the work, combining the results, and performing the final verification.

The helpers are useful when a task can be divided into separate pieces without the pieces depending heavily on one another.

## Tightly connected work: use one worker

Use one worker when the task is really one chain of cause and effect.

Imagine building a LEGO car. If 👨‍💻 one helper changes the engine, another changes the gearbox, and a third changes the wiring, all three changes may depend on the same design. Parallel work can create 💥 conflicts or inconsistent assumptions.

Example: fixing an authentication redirect bug.

```text
  🧠 Sol Light
  |
  | Investigate the complete authentication flow
  v
  🌙 Luna Medium
  |
  +-- inspect the login controller
  +-- trace the authentication service
  +-- inspect the session
  +-- inspect middleware and routing
  +-- identify the root cause
```

One 🌙 Luna worker can keep the whole mental model of the bug.

## Independent work: use several workers

Use parallel workers when each workstream has a clear boundary and the workers will not edit the same files or depend on each other's unfinished results.

Example: auditing an application before release.

```text
                 🧠 Sol Light
                Coordinator
                     |
       +-------------+-------------+
       |             |             |
   🌙 Luna 1      🌙 Luna 2     🌙 Luna 3
   Security       Performance   Tests
```

Possible assignments:

- Security: authentication, access control, validation, and secrets
- Performance: slow queries, N+1 calls, caching, and bottlenecks
- Tests: coverage gaps, failures, and edge cases

Sol then compares the findings and produces one final recommendation.

## Does task size decide the number of agents?

No. Task size is only one factor.

The better question is:

> Can this work be safely split into independent pieces?

| Situation | Recommended setup |
|---|---|
| One bug with a connected cause-and-effect chain | One worker |
| Several unrelated audits | Several workers in parallel |
| Multiple workers would edit the same files | One worker, or strictly separated write scopes |
| Quick fact-check or smoke test | One worker |
| Broad review with clear domains | Several workers, then synthesis |

## Practical rules

1. Keep 🧠 Sol as the coordinator and final verifier.
2. Give every 🌙 Luna worker one bounded, self-contained assignment.
3. Do not give two workers overlapping write scopes.
4. Use one worker when the next step depends on the previous step's result.
5. Close completed workers after the result has been collected.

## Current project setup

The configured default is:

```text
Parent:  🧠 Sol Light
Worker:  🌙 Luna Medium
```

The number of workers that can run at once is controlled by the active Codex runtime's concurrency limit. It is not determined automatically from the task's size. More workers are useful only when the work is genuinely parallelisable.

## DigiTrust Lab article example

For one article, 🧠 Sol keeps the Goal, Plan, publishing decision, and final
verification. 🌙 Luna Medium should handle bounded work whenever it can do so to
the same standard with fewer coordinator tokens.

```text
🧠 Sol Light
   |
   +-- 🌙 Luna: calendar, status, and content-gap evidence
   +-- 🌙 Luna: one connected WriterZen and Content Creator chain
   +-- Isolated Claude + OpenAI sessions: independent final Malay review
   +-- 🧠 Sol: integrate, authorize publication, and verify every hard gate
```

Independent, disjoint read-only workstreams may run in parallel, including
calendar analysis, content-gap analysis, source checks, and immutable-file
reviews. The Claude and OpenAI naturalness reviewers are isolated fresh sessions
that receive only the same frozen content and never see each other's review.
WriterZen, WordPress, ClickRank, Screpy, Google Search Console, and canonical
documentation must each have one sequential owner because they share
authenticated or mutable state. Close every worker after collecting its result.

## Example prompts

### One connected worker

```text
Investigate this login redirect bug end to end. Trace the complete flow,
identify the root cause, and propose one integrated fix. Do not edit files yet.
```

### Several independent workers

```text
Review this project in three independent workstreams:

1. Security: authentication, authorization, validation, and secrets.
2. Performance: slow queries, N+1 calls, caching, and bottlenecks.
3. Tests: coverage gaps, failures, and edge cases.

Keep each review read-only. Do not duplicate work. Return separate findings so
the coordinator can synthesize them.
```

## One-sentence memory aid

If the pieces must understand each other while they work, use one worker. If the pieces can work independently and report back, use several.
