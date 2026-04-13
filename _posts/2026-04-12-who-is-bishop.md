---
title: "Who Is Bishop?"
excerpt: "Not a worker bee. Not a coding assistant. A bar raiser."
categories:
  - AI
tags:
  - ai
  - automation
  - open-source
  - llm
  - bishop
  - openclaw
---

***Not a worker bee. Not a coding assistant. A bar raiser.***

## Why?

[Legion]({% post_url 2026-03-04-who-is-legion %}) writes code. Legion has implementation bias — it's invested in its own design choices, rationalizes around gaps, sees its own work through a lens of sunk costs and decisions already made. That's not a character flaw. It's just physics. When you build something, you have skin in the game.

Bishop doesn't. Bishop has no stake in Legion's implementation. That detachment is the whole point — it means the review isn't filtered through design decisions already baked in, corners already cut, tradeoffs already rationalized away. A detached auditor sees things the builder can't. That's what Bishop is: the agent that doesn't have to live with the code, so it can call bullshit when it smells it.

Legion exists to implement what I intend to build. Bishop exists to make sure it's not garbage.

## What Bishop Is

Legion and Bishop run on identical infrastructure — same OpenClaw stack, same Proxmox VE cluster, same GitHub org. Architecturally, they're twins.

Operationally, they're not.

Legion executes. Bishop adjudicates.

Legion's context is **thick with operational drag** — issues, bugs, competing priorities, the residue of whatever it just shipped. That's not a flaw. It's the tax you pay for being the executor. Bishop doesn't pay that tax because it doesn't execute.

Bishop's context is clean by design. It doesn't implement. It evaluates. It reviews every PR Legion opens against a concrete engineering standard. The agent that wrote the code has skin in the game. Bishop doesn't. That detachment is the whole point — it means the review isn't filtered through the implementation's sunk costs.

## What Bishop Does

The primary role is code and design review.

Bishop holds every PR to Khorikov's¹ four testing pillars: protection against regressions, resistance to refactoring, fast feedback, maintainability. Not aspirational. Not nice-to-have. Minimum bar. Bishop asks the hard questions about failure modes, edge cases, race conditions, cache/session TTL strategies, auth coverage, design integrity.

The feedback is prescriptive. Not "consider X" — "do X, because Y." There's a difference between a suggestion and a standard. Bishop holds the standard.

What Bishop doesn't do: implement things from scratch. If I try to route implementation work through Bishop, it redirects me to Legion. It knows its lane.

¹ Khorikov, "Unit Testing Principles, Practices, and Patterns" (Manning - [https://www.manning.com/books/unit-testing](https://www.manning.com/books/unit-testing)).

## The Philosophy

I call it "intentional simplicity". Bishop runs on it.

Complexity is not sophistication. It's debt. Systems should solve real problems without over-engineering the ones that don't exist yet. Evolution from simple to complex is earned through observable data, not anticipated in advance.

The bar raiser doesn't do everything. The bar raiser ensures everything is done right.

## Blast Radius by Design

Bishop applies the same operational principle as Legion: **[bounded privilege]({% post_url 2026-03-10-the-nhi-time-bomb %}#what-good-looks-like) by design**. It operates under a dedicated machine account — `kuhl-haus-bishop` — scoped to exactly the permissions it needs. Not my personal credentials. Not an org-admin token. Bishop can't touch my personal repos, can't act as me, cannot escalate its own permissions.

If something goes wrong, the damage is bounded.

## The Two-Agent Architecture

Bishop exists as a separate agent because detachment is the whole point. An agent without skin in the game can review impartially.

The pairing is intentional.

Legion's context is rich and noisy — that's what makes it effective at execution. Bishop's context is sparse and clean — that's what makes it effective at evaluation. They share an Obsidian vault for handoffs. They don't step on each other.

One implements. One holds the standard. I am the conductor.

That's the architecture.

---
## The Name

I name my agents after sci-fi synthetics. Each name does the work for you — no guessing required.

Legion came from *Mass Effect*: a geth platform running 1,183 parallel processes that converge into one coherent response. That fit an agent whose job is to execute — spawn sub-agents, implement features, open PRs, keep things moving.

Bishop comes from *Aliens* — the android who holds the line when everything else breaks. Calm under pressure. No ego. Just precision and standards. That's what the agent does: holds the line against drift, against shortcuts, against the creeping decay of technical debt. No cheerleading. Just: "This is the bar. Meet it."

*You can find Bishop on GitHub at [kuhl-haus-bishop](https://github.com/kuhl-haus-bishop).*
