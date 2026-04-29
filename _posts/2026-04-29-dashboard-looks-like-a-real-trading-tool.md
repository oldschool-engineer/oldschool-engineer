---
title: "The Stock Scanner Dashboard Finally Looks Like a Real Trading Tool"
excerpt: ""
categories:
  - Side Projects
tags:
  - stocks
  - trading
  - market-data
---

In [Part 5]({% post_url 2026-02-23-what-i-built-after-quitting-amazon-spoiler-its-a-stock-scanner-part-5 %}#looking-forward-the-four-waves), I laid out the roadmap as a SIGINT fire-control problem: Broad Search, Target Acquisition, Target Lock, Fire. Wave 1 proved the architecture could swallow 1,490 messages per second at market close without flinching. Wave 2 is about deciding *which of those tickers actually deserves my attention*.

Three goals drove this iteration:

1. A quote widget that tells me everything about a ticker without alt-tabbing to four browser tabs.
2. Streaming HOD/LOD alerts so I stop missing breakouts while I'm looking at something else.
3. Just enough charting to triage tickers without bouncing to TradingView every thirty seconds.

Here's what landed.

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/all-scanners-eqv4-tv-lite-charts.png)
*Screenshot: This is my default day trading layout with damn near everything crammed in.  This layout uses the TV Lite charts.*


#### The Data Plane Gets a New Scanner

Wave 2 introduces a new server: the Market Data Scanner (MDS). The MDS consumes the streams emitted from the Market Data Processors (MDP) and, like MDP, uses pluggable analyzers. This wave introduces the first one: `DailyRangeAnalyzer` (DRA). It tracks high-of-day and low-of-day across every session and emits to three feeds: `daily_range:{ticker}`, `daily_range_hod_alert`, and `daily_range_lod_alert`. Everything downstream — the new quote widgets, the alert feed — eats from this firehose.

The lesson from Wave 1 was that a pluggable data plane is worth the up-front pain. The MDS/DRA pairing follows that pattern: it's the first analyzer to slot in, but it won't be the last. When pillar-correlation scanners come online (the ones I teased at the [end of the news post]({% post_url 2026-04-01-stock-selection-why-news-matters %}#whats-next)), they'll plug in the same way.

I'm probably renaming the published feed to `enhanced_quote`. The current name made sense when DRA was the only consumer. It isn't anymore.

#### Enhanced Quote Widgets

The motivation here was simple: I wanted one widget that showed session highs/lows plus all the stuff I was tab-hopping for — company info, recent splits, SEC filings, and ticker events (e.g., like when Facebook (FB) became Meta Platforms (META)). The architecture is straightforward: DRA passes quote data through over WebSocket; the widget pulls supplemental data via REST.

Easy on paper. EQv1 and EQv2 were disasters anyway. Both hit a py4web REST API with WDC caching, and — technically speaking — *slower than shit*. Deprecated. We don't talk about them.

The lesson: a cache only earns its keep when the upstream is slow or rate-limited. Mine isn't either. Unlimited API calls, fast providers — every millisecond of cache lookup was pure overhead, plus a staleness bug waiting to happen. Complexity with no tangible payoff. EQv3 and EQv4 ditch the py4web middleman entirely and consume directly from Massive.com and Finlight. Async. No caching. Way faster.

Two widgets, both fed by DRA for quote data (WebSocket) and supplemental data via REST:

**EQv3 (Quote widget)** — column layout. Cards: Hero, Today, Previous Day, Volume, Session H/L, Short Interest, Company. Show, hide, reorder, pick a single-column, two-column, or wide layout.

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-01.png)
*Screenshot: The default EQv3 Quote layout. The advantage of EQv3 is a simple column-based layout.  You can re-order the cards and change some of them from list to chips but the configuration options are minimal - as a strength.*


![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-02.png)
*Screenshot: The EQv3 quote in edit mode with all the default options flipped to their non-default settings. Icon instead of logo, chips instead of lists. All cards except for the hero can be hidden, if desired.*

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-03.png)
*Screenshot: EQv3 quote in wide-mode*

**EQv4 (Enhanced Quote widget)** — grid layout. All the EQv3 cards plus SEC EDGAR Index, Stock Splits, Ticker Events, and Company News. (EQv4 calls Finlight directly for the Company News card — it doesn't go through the Widget Data Service like the standalone Company News widget does.)

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-04.png)
*Screenshot: The default EQv4 layout is un-usable. This is the disadvantage it has over EQv3.*

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-05.png)
*Screenshot: On the flipside, it is far more customizaable. This shows the addition of the Company News, Stock Splits, SEC EDGAR, and Ticker Events cards.*


![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-06.png)
*Screenshot: EQv4 in edit mode revealing tools to customize the layout. EQv4 uses a Grid Layout. Adjust Cols and Row H to customize your grid proportions. Choose between "chips" and "list".*

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-07.png)
*Screenshot: Hero card can choose between wide and narrow layouts as well as displaying the logo or icon.*


![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-08.png)
*Screenshot: 5 different configurations of EQv4 widget - this demonstrates how customizable this widget is*


The original "Quote" widget — the dumb one that only reads the symbol data cache — got renamed to **Mini Quote**. Same widget, more honest name.

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-09.png)
*Screenshot: The mini quote: basic but served its purpose in the early days.  Now, it never sees the light of day.*

**Company News Card vs Company News Widget**

The Company News Widget gets news that is cached in the WDC after being processed by the Finlight Data Processor (FDP).  In addition to caching articles that are tagged by Finlight, The FDP searches the title and summary for stock tickers and adds them to the Company News feed.  In the case of the MYSE surge on 4/16/2026, Finlight didn't tag the news article about their rebrading to Myseum.AI.  However, the FDP caught it and added it to the Company News feed.

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-10.png)
*Screenshot: Company News feed has "(positive sentiment) Myseum Shares Surge After Rebrand to Myseum.AI -- benzinga" while Company News Card and News Feed have nothing.*


#### Range Alerts Widget

HOD/LOD alerts are noisy. Like, *Saturn V rocket launch* noisy. So this widget leans heavily on filters to surface only the tickers matching your criteria, and those settings persist with your layout. Drop it in HOD or LOD mode, wire it to the event bus, and clicking a row lights up that ticker across every linked widget on the dashboard. Flip on "filter" mode and the Range Alerts widget itself collapses down to just that ticker too — which makes it easy to spot when a ticker has successively breached previous HOD or LOD thresholds.

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-11.png)
*Screenshot: Range alerts widget*


![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-12.png)
*Screenshot: Range alerts widget settings for day trading: $2-$20, 20M max float, 1x rel vol, 1% min change*



[The Flame System I introduced last month]({% post_url 2026-04-01-stock-selection-why-news-matters %}#the-flame-system) is going to do a lot of work here once Wave 3 lands. A red flame on a ticker that just breached HOD? That's the signal I've been trying to build toward for six months.

#### Charts (Finally)

I'm a momentum trader. My screening loop is brutal: look at the daily and 5-minute charts, check moving averages, VWAP, volume, average volume, and MACD. Decide in five seconds whether a ticker deserves more attention. The old workflow — manually typing tickers into TradingView dozens of times a morning — was wrecking my flow.

So Wave 2 adds basic charting. Candlesticks only. No trend lines, no drawings. This is a triage tool, not a TradingView replacement.

There are two implementations with feature parity for now:

- **Candlestick Chart** — Apache ECharts
- **TV Lite Chart** — TradingView Lightweight Charts

![](/assets/images/posts/dashboard-looks-like-a-real-trading-tool/image-00.png)
*Screenshot: *



Both ship the same indicators: 3 EMAs, 2 SMAs, 2 VWMAs, VWAP, volume + average volume, and MACD. The default moving average setup mirrors what I run on 80% of my own charts: 9 EMA, 21 EMA, 50 VWMA, 200 EMA, 200 SMA. (When I'm swing trading, I swap in the 50 SMA and 9 VWMA on a couple of charts.)

Why two chart libraries? Because TradingView Lightweight Charts don't support custom indicators — that's a paid-tier feature, and PineScript only runs on TradingView's platform anyway. ECharts gives me a path to eventually port my [Momentum Indicators PineScript](https://www.tradingview.com/script/krYt35wa-Momentum-Indicators/) to something I actually own. Whether that hill is worth dying on is a Wave 3 problem.

#### What's Next

Wave 2 is about finding stocks worth trading. Iteration 8 just shipped, Iteration 9 is in flight, and by the time it wraps we'll be there.

Wave 3 is about identifying buy and sell signals — correlating price action with news catalysts and surfacing those signals in real-time.

*Wave 2 gives me eyes. Wave 3 gives me a trigger. Wave 4 gives the system a trigger finger.*