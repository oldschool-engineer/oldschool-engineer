---
title: "I Caught My AI Lying About Math (Confidently)"
excerpt: "This morning, my OpenClaw AI assistant computed my trade journal P&L and got it wrong. Not a little wrong. Obviously wrong. Off by 33%, delivered with complete confidence."
categories:
  - AI
tags:
  - ai
  - openclaw
  - llm
  - legion
---

This morning, [Legion]({% post_url 2026-03-04-who-is-legion %}) — my [OpenClaw](https://docs.openclaw.ai/) AI assistant using Claude Sonnet 4.6 — computed my trade journal P&L and got it wrong. Not a little wrong. Obviously wrong. Off by 33%, delivered with complete confidence.

I caught it because I happened to glance at the numbers. Called it out. Legion acknowledged the error, spun up Python, recomputed, and updated the journal. All very civilized. But I sat there for a minute thinking: *how often does this happen when I don't check?*

That question bothered me enough that I spent the afternoon running tests.

---

## What I Assumed Going In

My working theory was simple: LLMs fail at math when numbers get big. Five digits and up, things get sketchy. Keep the numbers small and you're fine. This seemed reasonable — it's vaguely consistent with how these models are described, and honestly how I thought about it.

I was wrong.

---

## The Test

Ten rounds, 41 problems total, all multiplication. I varied two things: the size of the operands and the number of steps. I asked the model to solve each problem, then verified against Python.

Here's what happened:

| Round | Conditions | Score |
|-------|-----------|-------|
| 1 | Up to 65,535 / 1-2 steps | 3/3 |
| 2 | 5-digit / 2-6 steps | 0/4 |
| 3 | 4-digit / 2-6 steps | 0/4 |
| 4 | 3-digit / 2-6 steps | 1/4 |
| 5 | 2-3 digit / 2-6 steps | 1/4 |
| 6 | 1-digit (with one 2-digit) / 2-6 steps | 3/4 |
| 7 | 1-digit only / 3-5 steps | 4/4 |
| 8 | 1-2 digit mixed / 4-6 steps | 4/4 |
| 9 | 1-2 digit, larger values / 6 steps | 2/4 |
| 10 | 1-2 digit / 5-7 steps | 2/4 |

Final score: **20 out of 41. 49%.**

Coin flip territory.

Detailed analysis and results here: [LLM Arithmetic Reliability Test — 2026-03-23]({% post_url 2026-03-23-llm-math-test-report %})

---

## What Actually Breaks It

Large numbers break it, sure. Rounds 2 and 3 were a complete wipeout. That part matched my theory.

But look at rounds 7 and 8 versus rounds 9 and 10. All single and double-digit numbers throughout. Rounds 7 and 8: perfect. Rounds 9 and 10: half wrong. The difference? Steps. More multiplications chained together, more chances for accumulated error.

The model will correctly compute `8 × 6 × 5 = 240` without breaking a sweat. Give it `23 × 7 × 35 × 8 × 7 × 9` — all operands are still one or two digits — and it falls apart. The actual answer is 2,840,040. It gave me 28,282,200. That's not a rounding error. That's off by a factor of ten.

So the real failure modes are: **big numbers** and **too many steps**. The second one is the one I wasn't testing for, and it's the one that will burn you in practice. Financial calculations almost always chain multiple steps together.

---

## The Part That Actually Worries Me

Here's the thing that made me sit back in my chair.

When the model got something wrong, it didn't hedge. It didn't say "I'm not great at this, you should verify." It just... gave me an answer. Same tone, same confidence, same presentation as the correct answers. There was no signal I could read to distinguish a right answer from a wrong one.

There's a related trap I noticed when I asked the model to score its own answers. Left to its own judgment, it graded generously — partial credit, close-enough reasoning, rounding tolerance. When I enforced strict pass/fail, the score dropped to 49%. The model will rationalize its own errors if you let it.

That's the dangerous part. Not that it fails — everything fails sometimes. The dangerous part is that it doesn't *know* it's failing, and you can't tell from the outside either.

---

## What I'm Doing About It

The fix is straightforward: don't let the model do arithmetic by inference. When I need a number, I make it compute with Python. Every time. No exceptions.

I updated my workspace config to make that explicit and non-negotiable. For trade journal entries, P&L totals, position sizing, R:R calculations — the model writes the code and runs it. The number it writes in the journal comes from the interpreter, not from inference.

It's a small discipline change, but the alternative is trusting a coin flip on financial data. That's not acceptable.

---

## The Broader Point

I think most people using LLMs for any kind of quantitative work have internalized the "big numbers are risky" mental model and consider that sufficient. My test suggests that's not the right frame. The better frame is: **any arithmetic with multiple steps is unreliable, regardless of how small the individual numbers look.**

One or two multiplications? Usually fine. Chain four or more together? Verify it.

The model doesn't know it's wrong. It won't warn you. And if you ask it to check its own work, it'll probably convince itself it was right.

Use the interpreter. Trust the output. Write that down somewhere you'll actually see it.
