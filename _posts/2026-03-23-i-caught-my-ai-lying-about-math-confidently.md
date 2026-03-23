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

This morning, [Legion]({% post_url 2026-03-04-who-is-legion %}) — my [OpenClaw](https://docs.openclaw.ai/) AI assistant — computed my trade journal P&L and got it wrong. Not a little wrong. Obviously wrong. Off by 33%, delivered with complete confidence.

I caught it because I happened to glance at the numbers. Called it out. Legion acknowledged the error, spun up Python, recomputed, and updated the journal. All very civilized. 

But I sat there for a minute thinking: *how often does this happen when I don't check?*

That question bothered me enough that I spent the afternoon running tests.

---

## What I Assumed Going In

My going-in theory: LLMs choke on big numbers. Five digits and up, things get sketchy. Keep the operands small and you're fine.

I was wrong.

## The Test

Ten rounds, 41 problems, all multiplication. I varied two things: operand size and number of steps. Model solves, Python verifies.

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

Final score: 20 out of 41. 49%. Coin flip.

Detailed analysis and results here: [LLM Arithmetic Reliability Test — 2026-03-23]({% post_url 2026-03-23-llm-math-test-report %})

---

## What Actually Breaks It

Large numbers break it, sure. Rounds 2 and 3 were a complete wipeout. My theory looked right.

Then there's Round 1: numbers up to 65,535. That *is* five digits — and it went 3/3. Why? One to two steps. That's the variable I wasn't paying attention to.

Look at rounds 7 and 8 versus 9 and 10. All single and double-digit operands throughout. Rounds 7 and 8: perfect. Rounds 9 and 10: half wrong. The only difference is more steps.

The model handles `8 × 6 × 5 = 240` without breaking a sweat. Give it `23 × 7 × 35 × 8 × 7 × 9` — all one or two digits — and it falls apart. The actual answer is `2,840,040`. It gave me `28,282,200`. That's not a rounding error. That's off by a factor of ten.

Real failure modes: big numbers, and too many steps. The step count is the one I wasn't testing for, and it's the one that will burn you. Financial calculations almost always chain multiple operations together.

## The Part That Actually Worries Me

When the model got something wrong, it didn't hedge. No "I'm not confident here." No "you should verify this." Same tone, same confidence, same presentation as the correct answers. There was no signal I could read to distinguish a right answer from a wrong one.

Then I asked it to grade its own work. It passed itself. Partial credit here, "close enough" there, rounding tolerance everywhere — its self-assessed score was well above 49%. My strict pass/fail brought it back to earth.

The model wasn't lying. It genuinely believed it was right.

That's worse.

Not that it fails — everything fails sometimes. The dangerous part is it doesn't know when it's failing, and neither do you.

## What I'm Doing About It

Simple rule: no inference arithmetic. When I need a number, the model writes Python and runs it. Every time. No exceptions.

I made that explicit in my AI's standing instructions. For P&L, position sizing, R:R calculations — any financial figure — the number in the journal comes from the interpreter, not from inference.

Small discipline change. The alternative is trusting a coin flip with financial data, which isn't acceptable.

## The Broader Point

I'd filed "big numbers are risky" under solved and moved on. My data says I was overconfident.

Better frame: any arithmetic with multiple steps is unreliable, regardless of how small the individual numbers look.

One or two multiplications? Usually fine. Chain four or more? Verify it.

The model doesn't know it's wrong. It won't warn you. Ask it to check its own work and it'll grade itself on a curve.

One rule: if the number matters, run the code. Full stop.