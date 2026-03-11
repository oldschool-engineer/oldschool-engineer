---
title: "The NHI Time Bomb — Why AI Agents Are an Identity Crisis Waiting to Happen"
excerpt: "AI agents are getting access to credentials faster than your governance processes can track them. Here's what the NHI explosion actually looks like — and how to bound the blast radius before it bounds you."
categories:
  - AI
  - Security
  - Identity
tags:
  - ai
  - automation
  - security
  - identity
  - nhi
---

## Your NHI Governance Wasn't Ready For AI Agents. Neither Was Mine.

I've been watching credentials go unmanaged for twenty years. The current wave of AI agents isn't different in kind — it's different in scale. It's the same governance gap, running at machine speed, across any org that's touched an AI tool. You probably already have a ghost identity in your org. You just don't know it yet.

I've been in the room when someone found active credentials tied to an engineer who left two years earlier — write access to production infra, still live, origin unknown. That's what "we didn't get ahead of it" looks like.

---

## What Is a Non-Human Identity?

A Non-Human Identity (NHI) is any identity that isn't a person — service accounts, API keys, PATs, OAuth client credentials, machine certificates, pipeline tokens, bot accounts. Every CI/CD pipeline, every microservice calling another microservice, every automated deployment job has one. Or several.

Before AI agents, the NHI problem was bad but bounded. A mid-sized engineering org has hundreds of NHIs. Ask your identity team how many. Watch the silence — some documented, many forgotten, a few terrifying.

AI agents change the dynamic. Radically.

---

## The Explosion

Traditional NHI growth was slow — tied to hiring cycles, project scopes, team headcount. An AI agent blows that model apart. It doesn't onboard once. It mints credentials every time it needs to touch something new.

An AI agent, working autonomously at machine speed, can create or consume dozens of service credentials *per project*. Every API it needs to call. Every repo it needs to push to. Every secret it needs to read. Every cloud service it needs to touch.

Multiply that by the number of AI agents running in your org. Multiply that by every org that's already running agents today and calling it a pilot. And unlike human identities — which have natural lifecycle events that trigger review (employee offboarding, role changes, terminations) — NHI lifecycles are entirely dependent on whoever created them remembering they exist. The engineer remembers the ticket. They forget the PAT. By the time anyone asks, the engineer's gone and the token's still live.

The Ghost Identity Problem: when the engineer who spun up that AI agent leaves the company, their machine user and its PATs don't have an offboarding process. They just... persist. Quietly. With whatever access they had the day they were created.

---

## The Hard Problem: Governance at Nondeterministic Scale

Traditional least privilege is hard enough. You define the minimum access a system needs, you issue credentials scoped to that access, you review periodically. It works — imperfectly, but it works — because the systems you're securing are *deterministic*. They do exactly what you programmed them to do. You can enumerate their behaviors and scope their access accordingly.

AI agents are not deterministic.

A coding agent might need GitHub write access to push code. Fine — but to which repos? During what phase of work? When it's doing exploratory research vs. when it's opening a PR? The access profile of an AI agent isn't static. It shifts with context. It shifts with the task. It shifts as the conversation history gets compacted.

How do you govern least privilege for a system whose behavior you cannot fully predict?

The honest answer is: you constrain the blast radius.

You can't perfectly enumerate what an AI agent will do. You *can* ensure that what it does is limited to a defined boundary, that those boundaries are enforced by controls it cannot bypass, and that every action it takes is attributable to an identity you own and control.

That's not least privilege in the classical sense. It's *bounded privilege* — a different mental model for a nondeterministic actor.

---

## What Good Looks Like

I run an AI agent ([Legion]({% post_url 2026-03-04-who-is-legion %})) that has GitHub access to my infrastructure repos. Here's how I've structured it:

**1. Machine user, not my user**  
Legion authenticates to GitHub as [`kuhl-haus-legion`](https://github.com/kuhl-haus-legion) — a separate account I created specifically for it. It is not me. It does not have my permissions. If I revoke its access, I'm not revoking my own. If something goes wrong and I need to audit what it did, the entire commit history is attributable to a distinct identity.

**2. Write, never Admin**  
The machine user has `Write` collaborator access to the repos it needs. Write lets it push branches and open PRs. It cannot merge without my approval. It cannot delete branches. It cannot change org settings. It cannot add collaborators.

**3. Branch protection is the enforcement layer**  
Branch protection rules apply to the machine user just like they apply to any contributor. Require PR. Require approval. Block force pushes. Restrict deletions. The AI's nondeterminism is bounded by the same controls that bound a human contributor.

**4. Fine-grained PAT with minimal scope**  
The token is scoped to specific repos, specific permissions. Code read/write. Issues. PRs. Not Actions, not secrets, not org admin. Every permission I didn't explicitly grant is a capability the agent doesn't have.

**5. Org-level enforcement**  
Every commit goes through a PR. Every PR is squash-merged. There's a clean, auditable record of every change the agent made, with a human approval in the history.

The result: Legion can do real work — branch, commit, push, open PRs, respond to review comments, iterate. It can't do catastrophic work. The blast radius is bounded.

---

## For Enterprises: It's WHEN, Not IF

What I've described above scales — but enterprises need to go further before they start, not after. If you're reading this as an engineering leader, here's the uncomfortable truth: you are going to use agentic AI.

What you need before you deploy agentic AI at scale:

- **NHI inventory**: Know what machine identities you already have. You probably don't. Start there.
- **Lifecycle process for NHIs**: Creation, rotation, review, revocation — tied to the project lifecycle, not the human lifecycle.
- **Machine user standards**: Every AI agent gets its own identity. No shared service accounts. No minting from personal accounts.
- **Scope hygiene**: Minimum permissions. Reviewed at creation and on a calendar. No "I'll scope it down later."
- **Audit trail**: Every action taken by a machine identity should be attributable and searchable.
- **Break-glass procedures**: When an agent does something unexpected, how fast can you revoke, contain, and audit?

None of this is exotic. It's IAM fundamentals applied to a new actor class. If you can't answer "how many NHIs does your org have right now?" — that's your starting point. Not the AI agent checklist. That.

---

## The Bottom Line

The identity explosion isn't coming. It's here. If you've had an AI agent running for more than six months and haven't audited its credentials — you already have a ghost identity. You just haven't found it yet.

If you're an identity engineer, this is your moment to get ahead of it. If you're a CISO, this is the gap in your NHI governance program. If you're an engineer who just gave your AI agent your own credentials — go fix that. Today.

The question isn't whether agentic AI creates identity risk. It does. The question is whether you're the person who governed it proactively, or the person who explains the incident report.

---
