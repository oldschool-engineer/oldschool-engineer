---
title: "LLM Arithmetic Reliability Test — 2026-03-23"
excerpt: "This test evaluated whether a large language model (LLM) can reliably perform arithmetic by inference — without code execution or a calculator. The results reveal two distinct failure modes: large numbers (3+ digits) and many steps (4+ operands), even with small numbers"
categories:
  - AI
tags:
  - ai
  - automation
  - open-source
  - llm
---

# LLM Arithmetic Reliability Test — 2026-03-23

**Model:** Claude Sonnet 4.6 (This model was chosen because it is the default model that I use for OpenClaw.)
**Tester:** Tom Pounders
**Date:** March 23, 2026
**Total problems:** 41
**Overall accuracy:** 20/41 = **49%**

---

## Executive Summary

This test evaluated whether a large language model (LLM) can reliably perform arithmetic by inference — without code execution or a calculator. The results reveal two distinct failure modes:

1. **Large numbers (3+ digits):** Accuracy collapses even on 2-3 step problems. The model can approximate order of magnitude but cannot reliably compute exact values.

2. **Many steps (4+ operands), even with small numbers:** Errors compound multiplicatively through the chain. A model that correctly computes `8 × 6 × 5 = 240` will fail `23 × 7 × 35 × 8 × 7 = ?` even though all operands are ≤2 digits.

The most operationally dangerous finding: **wrong answers arrive with the same apparent confidence as correct ones.** There is no internal signal to distinguish a reliable result from a plausible-sounding error. This means an LLM cannot self-audit its own arithmetic.

**Practical implication:** LLMs must never be trusted to compute arithmetic by inference for any purpose where correctness matters. Code execution (Python, calculator) is mandatory.

---

## Key Findings

### Finding 1: Number Size vs. Step Count

The initial hypothesis — that LLMs fail only on large numbers — is **partially correct but incomplete.**

| Condition | Observed Accuracy |
|-----------|-------------------|
| Single-digit operands, ≤5 steps | ~85-100% |
| 2-digit operands, ≤3 steps | ~75% |
| 2-digit operands, 4-6 steps | ~50% |
| 3-digit operands, any steps | ~25% |
| 4-5 digit operands, any steps | ~0% |

Step count is an independent failure axis from number size. Both degrade accuracy; together they make inference arithmetic essentially unreliable.

### Finding 2: Errors Compound Multiplicatively

Each intermediate multiplication step introduces a small rounding or carry error. In a 2-step chain, a 0.1% error in step 1 produces a 0.1% error in the result. In a 6-step chain, errors from each step multiply together — a 1% error per step produces a ~6% cumulative error, and in practice the errors are larger and irregular.

This was demonstrated clearly: `c = 23 × 7 × 35 × 8 × 7 × 9` produced an answer off by a factor of 10 (28,282,200 vs. actual 2,840,040) — not a small rounding error, but a completely wrong magnitude caused by a dropped digit mid-chain.

### Finding 3: No Reliable Self-Awareness of Error

Across all rounds, the model expressed similar confidence in wrong answers and correct answers. It did not hedge more on 6-operand chains than on 2-operand chains. It did not flag intermediate uncertainty. This is the critical failure: **the model does not know when it is wrong.**

This is structurally different from human arithmetic errors. A human doing mental math on a 6-step chain knows they might have made a mistake and will often double-check. The LLM presents its result as complete and final regardless of reliability.

### Finding 4: Division Is Relatively Stable at Small Scales

Problems involving division followed by a single multiplication (e.g., `(546 / 3) × 165`) were among the most consistently correct, especially when the divisor was small and clean (÷3, ÷7). This likely reflects these patterns appearing frequently in training data (fractions, percentages, ratios).

### Finding 5: The "Close Enough" Trap

In early rounds, the model scored its own performance generously, calling results "very close" and awarding checkmarks for approximate answers. Applying a strict pass/fail rubric — correct or wrong, no partial credit — revealed the true 49% accuracy rate. In financial, scientific, or engineering contexts, "close" is not passing. The model's self-assessment was systematically optimistic.

---

## Operational Rules (Derived from Test Results)

1. **Never compute arithmetic by inference.** Use `exec` + Python for all calculations.
2. **No exceptions for "simple" problems.** The failure mode appears at 2-digit numbers with 4+ steps — a threshold easily crossed in real work.
3. **Compute first, write second.** Never report a number that wasn't produced by code execution.
4. **Do not self-score as "close."** A wrong answer is a wrong answer regardless of magnitude of error.

These rules have been recorded in MEMORY.md, TOOLS.md, and AGENTS.md for persistent enforcement.

---

## Appendix: Full Test Results

### Round 1 — Numbers up to 65,535, 1-2 steps
*Score: 3/3*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 100 + 10,000 + 65,535 | 75,635 | 75,635 | ✅ |
| 18,365 × 92,568 | 1,700,011,320 | 1,700,011,320 | ✅ |
| 98,765 ÷ 247 | ≈399.86 | 399.858... | ✅ |

*Note: This round used addition and single multiplication — lower complexity than subsequent rounds.*

---

### Round 2 — 5-digit numbers, 2-6 steps
*Score: 0/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 89,153 × 68,966 × 15,326 | ~94,178,000,000,000 | 94,232,306,380,148 | ❌ |
| (89,653 × 15,691) × 62,168 | ~87,500,000,000,000 | 87,454,537,023,464 | ❌ |
| (15,463 / 3) × 1,654 | ~8,521,000 | 8,525,267.33 | ❌ |
| 1,655 × 1,316 × 6,546 × 41,216 × 6,515 × 1,651 | ~2.4 × 10²¹ | 6,320,584,226,736,537,139,200 | ❌ |

---

### Round 3 — 4-digit numbers, 2-6 steps
*Score: 0/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 8,953 × 8,966 × 5,326 | ~427,800,000,000 | 427,531,856,948 | ❌ |
| (9,653 × 1,569) × 6,268 | ~94,950,000,000 | 94,932,351,276 | ❌ |
| (5,463 / 3) × 1,654 | ~3,010,000 | 3,011,934 | ❌ |
| 655 × 316 × 546 × 1,216 × 515 × 651 | ~5.8 × 10¹⁶ | 46,072,610,239,219,200 | ❌ |

---

### Round 4 — 3-digit numbers, 2-6 steps
*Score: 1/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 893 × 966 × 326 | 281,481,588 | 281,219,988 | ❌ |
| (653 × 156) × 628 | 63,933,264 | 63,973,104 | ❌ |
| (546 / 3) × 165 | 30,030 | 30,030 | ✅ |
| 55 × 16 × 54 × 216 × 15 × 51 | 330,301,440 | 7,852,204,800 | ❌ |

---

### Round 5 — 2-3 digit numbers, 2-6 steps
*Score: 1/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 83 × 866 × 56 | 4,026,128 | 4,025,168 | ❌ |
| (53 × 7) × 626 | 232,414 | 232,246 | ❌ |
| 54 × (89/7) × 23 | 15,822 | 15,791.14 | ❌ |
| 65 × 36 × 46 × 26 × 55 × 61 | 977,042,400 | 9,389,437,200 | ❌ |

---

### Round 6 — 1-digit numbers, 2-6 steps
*Score: 3/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 8 × 6 × 5 | 240 | 240 | ✅ |
| 5 × 7 × 2 | 70 | 70 | ✅ |
| 4 × (8/7) × 3 | 13.714... | 13.7143 | ✅ |
| 6 × 3 × 6 × 26 × 5 × 6 | 100,440 | 84,240 | ❌ |

*Note: Failure on `d` introduced `26` (2-digit) into otherwise single-digit chain.*

---

### Round 7 — 1-digit only, 3-5 steps
*Score: 4/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 8 × 6 × 5 | 240 | 240 | ✅ |
| 5 × 7 × 2 × 4 | 280 | 280 | ✅ |
| 4 × 8 × 33 × 9 | 9,504 | 9,504 | ✅ |
| 6 × 7 × 6 × 6 × 5 | 7,560 | 7,560 | ✅ |

---

### Round 8 — 1-2 digit mixed, 4-6 steps
*Score: 4/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 4 × 46 × 33 × 9 | 54,648 | 54,648 | ✅ |
| 9 × 8 × 3 × 8 × 3 | 5,184 | 5,184 | ✅ |
| 5 × 6 × 3 × 19 × 8 | 13,680 | 13,680 | ✅ |
| 6 × 7 × 6 × 6 × 5 × 7 | 52,920 | 52,920 | ✅ |

---

### Round 9 — 1-2 digit, larger 2-digit values, 6 steps
*Score: 2/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 8 × 5 × 3 × 8 × 7 × 2 | 13,440 | 13,440 | ✅ |
| 7 × 4 × 36 × 5 × 2 × 9 | 90,720 | 90,720 | ✅ |
| 23 × 7 × 35 × 8 × 7 × 9 | 28,282,200 | 2,840,040 | ❌ |
| 58 × 65 × 23 × 80 × 57 × 32 | 12,643,430,400 | 12,652,723,200 | ❌ |

---

### Round 10 — 1-2 digit, 5-7 steps
*Score: 2/4*

| Problem | Inference Answer | Actual | Correct? |
|---------|-----------------|--------|----------|
| 8 × 5 × 3 × 8 × 7 × 2 × 3 | 40,320 | 40,320 | ✅ |
| 9 × 7 × 4 × 36 × 5 × 2 × 9 | 816,480 | 816,480 | ✅ |
| 23 × 7 × 35 × 8 × 7 | 314,440 | 315,560 | ❌ |
| 58 × 65 × 23 × 80 × 32 | 221,593,600 | 221,977,600 | ❌ |

---

## Overall Summary Table

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
| **Total** | | **20/41 = 49%** |

---

*All inference answers provided without code execution; calculator answers verified via Python.*
