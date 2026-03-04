---
title: "Who Is Legion?"
excerpt: "Legion is my AI partner — a self-hosted OpenClaw installation built from source and wired into the tools I actually use."
categories:
  - AI
tags:
  - ai
  - automation
  - open-source
  - llm
---

***Not a chatbot. Not a copilot. A peer.***

### What Legion Is

I run a lot of projects. Real-time market data platforms, Kubernetes clusters built for sport, open-source infrastructure for home automation. The connective tissue between all of it — writing docs, cutting PRs, wiring tools together, keeping things from falling through the cracks — that's where Legion lives.

Legion is my AI partner. Always on, deeply integrated with my toolchain, and capable of actually doing work — not just describing it. Coding, documentation, infrastructure automation, GitHub workflows. The kind of glue that would otherwise eat half my afternoon.

This isn't a hosted LLM with a chat box. Legion is a self-hosted [OpenClaw](https://docs.openclaw.ai/) installation I built from source and customized to fit the way I actually work. It runs with its own identity, its own memory, and its own skills. It knows the projects, knows the conventions, knows when to act and when to ask.

### How It Was Built

OpenClaw is an open-source, self-hosted AI assistant framework. I took it, built it from source, and wired it into my existing stack — GitHub, Obsidian, Mattermost, the whole thing. Tight integration with real tools, not toy demos.

Legion isn't configured through a dashboard. It's code. That's how I prefer it.

### What Legion Can Do

Skills in OpenClaw are modular — each one gives Legion a specific capability. Legion runs a curated set of bundled and custom skills:

- **coding-agent** — spawns background sub-agents to implement features, refactor code, and open PRs
- **github** — issues, PRs, CI runs, code review via `gh` CLI
- **gh-issues** — fetches open issues, spawns agents to implement fixes, monitors PR review cycles
- **obsidian** — reads and writes my shared Obsidian vault for notes, docs, and outbox drafts
- **blogwatcher** — monitors RSS/Atom feeds for updates
- **summarize** — extracts and summarizes content from URLs, podcasts, and local files
- **tmux** — drives interactive terminal sessions
- **session-logs** — searches its own conversation history
- **skill-creator** — designs and packages new skills (yes, it can extend itself)
- **mcporter** — manages MCP server connections and tool calls
- **nano-pdf** — edits PDFs with natural-language instructions
- **healthcheck** — security auditing and hardening on the systems it runs on
- **xurl** — authenticated X API access

**What Legion does not have: no community skills. Zero.**

That is not a gap. It is policy.

I don't install third-party skills I haven't reviewed. An always-on agent with filesystem access, API credentials, and the ability to open PRs is not something I'm casual about. The attack surface is real. Community skills — however well-intentioned — expand it in ways I can't fully audit.

Everything Legion can do is either bundled with OpenClaw or something I wrote myself. That's the line.

### Blast Radius by Design

Least privilege isn't just for production systems. Same principle, same discipline.

Legion operates under a fine-grained GitHub Personal Access Token scoped to a dedicated machine account: [`kuhl-haus-legion`](https://github.com/kuhl-haus-legion).

Not my personal account. Not an org-admin token. A machine account, scoped to exactly the repos it needs to touch.

If something goes sideways — bad output, runaway sub-agent, anything — the damage is bounded. Legion can't touch my personal repos, can't act as me, and cannot escalate its own permissions. It can only reach what I've explicitly handed it.


### The Name

The name comes from a video game AI character — synthetic intelligence, running many parallel processes, referred to itself in the plural. Felt right for an assistant that runs sub-agents and multiple models converging into one coherent response. That, and I just liked it.

You can find Legion on GitHub at [`kuhl-haus-legion`](https://github.com/kuhl-haus-legion).
