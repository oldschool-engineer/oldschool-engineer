---
title: "Prevent Cache Stampedes with asyncio Events"
excerpt: "A two-layer cache-miss prevention strategy using asyncio.Event and Redis locks."
categories:
  - Software Engineering
tags:
  - python
  - asyncio
  - redis
  - caching
  - performance
---

#### Learn how a two-layer asyncio.Event and Redis lock strategy eliminates cache-miss stampedes, cutting thousands of redundant Redis calls at market open.

![](https://cdn-images-1.medium.com/max/1200/1*ejEIEJEsMaKwZzHZNWD-bA.jpeg)

*My miniature nano cow stampeding herd, heading straight for Redis at market open. Every. Single. Morning.*

[Wave 1 is done.]({% post_url 2026-02-24-what-i-built-after-quitting-amazon-spoiler-its-a-stock-scanner-part-5 %}) The second I shipped it, I turned to the thing quietly living on my mental whiteboard: a cache-miss stampede in the MarketDataCache (MDC).

Quick disambiguation: [I mentioned a stampeding herd in an earlier post]({% post_url 2026-02-11-what-i-built-after-quitting-amazon-spoiler-its-a-stock-scanner-part-4 %}) — that was a message backpressure mechanism rendered useless problem. This is a different herd. Same name, different cattle.

### The Scenario

The MDC is a Redis cache-aside layer between the platform’s analyzers and the Massive.com REST API. Check Redis first, call the API on a miss.

The incoming feed is per-second stock aggregates — OHLC, volume — for the entire market, peaking around 1,500 msg/s at close. At market open, the message rate jumps from roughly 30 msg/s to 800 msg/s within seconds. The cache isn’t just cold — it’s been reset, because opening prices invalidate the previous session’s data. Per-second aggregates only fire when a stock actually updates, so those 800 messages aren’t spread evenly across the market; they’re concentrated in the 100–200 high-volume stocks volatile enough to update every single second. Those are the tickers that hammer Redis hardest.

In the happy path, Massive.com responds in ~80ms. Fast enough that in most cases the cache is warm well before the next message arrives. The stampede is really a cold-start burst problem: multiple analyzers simultaneously requesting the same ticker, all within that 80ms window.

The ugly case is a timeout. The underlying `RESTClient` does retries with exponential backoff — a degraded API response doesn't just cost 10 seconds, it can stack well past 30.

### Why a Redis Lock Alone Isn’t Enough

The obvious fix is a distributed lock — one coroutine grabs it, fetches, the rest wait. But look at what `await lock.acquire()` actually does inside `redis.asyncio`:

```python
# Simplified from redis/asyncio/lock.py  
while True:  
    if await self.do_acquire():  # SET NX  
        return True  
    await asyncio.sleep(self.sleep)  # polls every 100ms
```

Every waiting coroutine independently hammers Redis with `SET NX` every 100ms. In the happy path at ~80ms, that's roughly one poll per waiter — annoying but not painful. In the timeout case, that's 100 polls per waiter per 10-second attempt, multiplied by retry attempts, multiplied by N waiters across 150 hot tickers. The event loop stays healthy — each `asyncio.sleep` yields — but Redis is absorbing O(N) poll traffic for absolutely nothing.

### The Fix: Two Layers

Layer 1: `asyncio.Event` collapses in-process contention to zero network traffic.  
Layer 2: Redis lock handles cross-pod contention.

```python
async def get_ticker_snapshot(self, ticker: str) -> TickerSnapshot:  
    cache_key = f"{MarketDataCacheKeys.TICKER_SNAPSHOTS.value}:{ticker}"
```

Waiting coroutines do a true `await event.wait()` — zero network, zero polling, event-loop-native. The loop wakes them via epoll/kqueue when the event fires. Not a timer. Whether the API responds in 80ms or grinds through retries for 30+ seconds, in-process waiters generate exactly zero Redis traffic while they wait.

The Redis lock in `_fetch_snapshot_with_lock` handles what `asyncio.Event` can't — multiple pods competing across process boundaries:

```python
async def _fetch_snapshot_with_lock(self, ticker, cache_key):  
    lock_key = f"{MarketDataCacheKeys.TICKER_SNAPSHOT_LOCK.value}:{ticker}"  
    lock = self.redis_client.lock(  
        lock_key,  
        timeout=MarketDataCacheTTL.TICKER_SNAPSHOT_LOCK.value,  # 30s  
    )  
    try:  
        await lock.acquire()  
        result = await self.read(cache_key=cache_key)  # double-check  
        if result:  
            return TickerSnapshot.from_dict(result)  
        start = time.monotonic()  
        snapshot = self.rest_client.get_snapshot_ticker(  
            market_type="stocks", ticker=ticker,  
        )  
        duration = time.monotonic() - start  
        self.snapshot_api_duration.record(duration)  # OpenTelemetry histogram  
        data = ticker_snapshot_to_dict(snapshot)  
        await self.write(data=data, cache_key=cache_key,  
                         cache_ttl=MarketDataCacheTTL.TICKER_SNAPSHOTS.value)  
        return snapshot  
    finally:  
        if await lock.locked():  
            await lock.release()
```

The double-check read after `lock.acquire()` handles the cross-pod version of the same problem: another pod may have already populated the cache while this one was waiting.

### When the Leader Dies

The `finally` block is load-bearing. Three distinct failure modes:

**Leader throws a non-retry exception (process still alive):** `event.set()` fires immediately. In-process waiters wake up, find the cache empty, fall through, and one steps up as leader. Without the `finally` guarantee, they'd block until the Redis lock TTL expired.

**Leader pod crashes entirely:** The `asyncio.Event` dies with it — in-process waiters are already dead too. Cross-pod waiters are stuck on the Redis lock, and the 30-second TTL is their only backstop. It auto-expires, one pod grabs the lock, and we're back in business.

**Leader’s retries outlive the 30-second TTL:** This is the interesting one. The lock auto-expires. A cross-pod waiter grabs it, checks the cache — miss, because the original thread hasn’t written yet — and fires another API call. The original thread eventually succeeds, tries to release a lock it no longer owns, and `if await lock.locked()` quietly saves us from the error. The duplicate API call already happened though.

30 seconds isn’t outrageous given the retry behavior, but it’s also not right-sized. That’s the whole point of the OpenTelemetry histogram — once I have real p99 data including retry scenarios, I can set a TTL that covers the realistic worst case without leaving cross-pod waiters in limbo longer than necessary.

### Same Pattern, Three Methods

`get_avg_volume` and `get_free_float` use the identical two-layer pattern — their own `_pending_*` dicts, their own lock keys, their own histograms. Nothing exotic, just applied consistently.

### The Scorecard

[v0.2.27](https://kuhl-haus-mdp.readthedocs.io/en/latest/changelog.html#version-0-2-27-2026-02-24) ships with 425 passing tests — 57 of them in `test_market_data_cache.py` — 99% overall coverage, 100% on `market_data_cache.py` (254 statements, 48 branches). Flake8 clean. Full source on [GitHub](https://github.com/kuhl-haus/kuhl-haus-mdp).
