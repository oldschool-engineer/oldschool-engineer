---
title: "Why I'm Betting on a SaaS Rally in 2026."
excerpt: "Dario Amodei says AI will make software free. I've spent $2,600 with his company in four months running two agents in production, and I'm here to tell you the SaaS incumbents are about to eat very well."

categories:
  - Opinion
tags:
  - ai
  - software-engineering
  - agentic-engineering
  - software-as-a-service
---

**_The hype says AI will zero out the cost of software. The market is about to learn that "software" was never the expensive part._**

> _[Last time I argued AI won't replace engineers.]({% post_url 2025-11-02-could-we-just-use-brainfuck-for-vibe-coding %}) This time I'm arguing it won't replace their employers either._

## The One-Line Version

Amodei's "software → free" thesis is a P&L mistake. He's compressing _one row_ on the income statement and calling it the whole business.

## What Amodei Actually Said

At Davos 2026, Anthropic CEO Dario Amodei told the _Wall Street Journal_ that AI would make software "cheap and potentially free," because it would remove "the need to spread development costs across millions of users."[1](https://digg.com/ai/cyq1lblx)  

> "If your moat is 'our software is complex and difficult to write, and we can write it, and others can't match it,' I think that's going away."[2](https://www.thenews.com.pk/latest/1402953-software-will-become-essentially-free-warns-anthropic-ceo-amodei#:~:text=If%20your%20moat%20is%20%27our%20software%20is%20complex%20and%20difficult%20to%20write%2C%20and%20we%20can%20write%20it%2C%20and%20others%20can%27t%20match%20it%2C%27%20I%20think%20that%27s%20going%20away%2C)  

That second part, I agree with. If your only moat is hard-to-write code and a piss-poor customer experience, your days are numbered. That's been true since before Claude could write [Hello, World](https://en.wikipedia.org/wiki/Hello,_world).

The first part is where he loses me. The lever he's pulling is **amortized development cost** — the price of writing and maintaining code, divided across a customer base. Zero it out, and in his telling, "software" goes to zero with it.

Code cost is one row on a SaaS P&L. The other rows don't budge.

Here's why.

## 1. Code Is a Line Item, Not a Business

Engineering labor is real money. It is also one cost center among many. SLAs, hardware depreciation, compliance, on-call, contracts, sales, support, procurement integration — none of those get cheaper because Claude can scaffold a CRUD app.

AI is a competitive input to _one_ role on the org chart. Pricing the whole business off that one input is a category error.

## 2. Systems Are the Moat

Your SLA doesn't care that your runbook was AI-generated. Your auditor doesn't care that Claude wrote your Terraform. Your enterprise customer's procurement team doesn't care how the sausage gets made — they care who is on the hook at 3 a.m. when the sausage stops getting made.

The bill for being a trusted service provider is paid in accountability, not keystrokes. AI compresses the labor inside those functions. It doesn't compress the obligations.

## 3. The DIY Trap Is Loaded

"We'll just vibe-code our own [Salesforce / Datadog / Stripe]" is the 2026 version of "we'll just self-host it."

AI makes the _initial build_ viable for more people. It doesn't make _operating_ a production service viable for them. The DIY honeymoon ends one of two ways: the first time production melts down and nobody can explain why, or the first SOC 2 questionnaire that asks who owns control CC7.2.

## 4. Incumbents Win This Cycle

Mature SaaS companies are using AI to compress the one line item it compresses — engineering labor — while their other moats keep compounding. Every dollar of dev cost AI strips out of their P&L is a dollar they can spend widening the gap on the rows AI _can't_ touch.

The "AI levels the playing field" story assumes the incumbents are sitting still. They aren't.

## 5. The Decommission Cycle

The vibe-coded replacement gets quietly decommissioned. Migration back to the SaaS vendor who does it cheaper, faster, and with someone to sue when it breaks — because that vendor also adopted AI, and used the savings to widen the gap in (1) through (4).

The "AI killed SaaS" narrative ages like milk.

---

## Who's Talking

I'm not a skeptic from the cheap seats. My career arc:

- **Microsoft:** Systems Engineer → Senior Service Engineer (the role Microsoft later renamed SRE, after I'd left).
- **Amazon:** Systems Engineer → System Development Engineer → L5 SDE → L6 Senior SDE.

I've spent most of my career maintaining systems where the _application_ software was written by other teams. But I've always written code:

- As an SE, I wrote the code that _deployed and operated_ other people's   software — automation, monitoring, pipelines, recovery tooling, the production substrate.
- As an SDE, I write all of it: application code _and_ the systems code that keeps it alive.

That is why I'm extracting so much value from agentic engineering. **AI saves me a shit ton of typing precisely because of my background.** I know what the right answer looks like, where the failure modes hide, and how the operational pieces snap together. The agent handles the keystrokes. I handle the judgment.

## The Receipts

I'm running two production-grade agentic engineering programs:

- **[Legion]({% post_url 2026-03-04-who-is-legion %})** — the executor. [kuhl-haus-legion](https://github.com/kuhl-haus-legion): 1,144 contributions in the last year (40% commits, 42% PRs, 17% issues, 1% code review).
- **[Bishop]({% post_url 2026-04-12-who-is-bishop %})** — the reviewer. [kuhl-haus-bishop](https://github.com/kuhl-haus-bishop): 144 contributions (99% code review, 1% issues).

Three control surfaces drive the system — **Chat** for instructions, **Obsidian** for design docs and reviews, **GitHub** for Issues and PRs. The day-to-day shape is similar to delegating to a junior engineer: decompose, provide references, iterate on design, iterate on code review, hand-hold through ambiguity. (How I do agentic engineering is its own post. One I keep putting off.)


Here's what that's cost me at Anthropic:

| Month | Anthropic spend |
|---|---|
| Feb 2026 | $77 (2 days of usage) |
| Mar 2026 | $754 |
| Apr 2026 | $1,125 |
| May 2026 (MTD) | $685 |
| **Total** | **~$2,641** |

Cheaper than a junior SDE? **Yes.** Lower barrier to entry than hiring? **Maybe.** _Free?_ **Not even close.** The CEO whose company makes software "free" has invoiced me $2,600+ in four months for the privilege.

## Mini-FAQ

**Q: Aren't you an AI skeptic dressing up sour grapes as analysis?**  
A: I just told you I've spent $2,600 in four months on agentic engineering and I'm running a two-agent program in production. I'm a heavy user. I'm betting against the _pricing narrative_, not the technology.

**Q: Doesn't AI being cheaper than a junior SDE prove Amodei's point?**  
A: It proves AI is a competitive input to _one_ role on the org chart. It says nothing about SLAs, hardware depreciation, compliance, on-call, or contracts. See also: [Myth: Companies Can Skip Hiring Junior Engineers with AI Tools]({% post_url 2025-11-02-could-we-just-use-brainfuck-for-vibe-coding %}#myth-companies-can-skip-hiring-junior-engineers-with-ai-tools).

**Q: Why does AI save _you_ so much typing if it doesn't save everyone that much?**  
A: Because I know what I want, in what shape, with what failure modes, deployed how, monitored how, and rolled back how. The agent is a force multiplier on _existing_ judgment. Hand the same tooling to someone without the systems background and you get a working demo that falls over the first time it meets real traffic. Same tool, different output.

**Q: Are you predicting SaaS stocks rally in 2026? Is this investment advice?**  
A: I'm predicting the _category_ rallies — incumbents widen their moats and DIY refugees migrate back. This is not investment advice. This is an old systems engineer telling you which way the wind is blowing.

**Q: What would change your mind?**  
A: A non-trivial enterprise running a fully self-hosted, AI-built replacement of a major SaaS product _in production_, hitting four-nines, passing a SOC 2 Type II, and costing materially less all-in than the SaaS vendor it replaced. I'll wait.

## The Bet

Amodei's "software → free" thesis confuses a _line item_ with a _business_. He's right that AI compresses the cost of writing code. He's wrong that the cost of _running software as a service_ follows it down. The $2,600 I've handed his company since February is, ironically, the cleanest evidence that "free" isn't even the right word for the part he _is_ talking about.

Even Amodei's own audience didn't buy it. CEOs at Davos pushed back on the same stage.[3](https://fortune.com/2026/01/27/at-davos-ceos-said-ai-isnt-coming-for-jobs-as-fast-as-anthropic-ceo-dario-amodei-thinks/), [4](https://fortune.com/2026/01/23/deepmind-demis-hassabis-anthropic-dario-amodei-yann-lecun-ai-davos/)  

The companies that already know how to _run_ software at scale are about to eat very well.

---

## References

1: [Anthropic CEO Dario Amodei said in a Wall Street Journal interview...
    — Digg](https://digg.com/ai/cyq1lblx)  
2: [Software will become 'essentially free,' warns Anthropic CEO
    Amodei — The News](https://www.thenews.com.pk/latest/1402953-software-will-become-essentially-free-warns-anthropic-ceo-amodei)  
3: [At Davos, CEOs said AI isn't coming for jobs as fast as Anthropic CEO
    Dario Amodei thinks — Fortune](https://fortune.com/2026/01/27/at-davos-ceos-said-ai-isnt-coming-for-jobs-as-fast-as-anthropic-ceo-dario-amodei-thinks/)  
4: [AI luminaries at Davos clash over how close human-level AI is —
    Fortune](https://fortune.com/2026/01/23/deepmind-demis-hassabis-anthropic-dario-amodei-yann-lecun-ai-davos/)  
