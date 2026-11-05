# Track A - A2 r340 (139x139x340, 6,569,140 cells) smoke + projection (job water-engine-mail-20261025-1830)
Executed on mail 2026-10-26T02:11:15Z-02:20:24Z UTC (7:11-7:20 PM PDT Oct 25), 12 ranks, ai-job cpu-heavy.
Smoke STOPPED EARLY by Grok Bot at sim t = 1.194e-5 s (ClockTime 401 s) because the projection is decisive;
ledger shows rc 137 = deliberate docker stop, NOT a solver failure.
Measured: r340 37.6 s per us sim (t 9.44e-6..1.19e-5) vs r225 (6 ranks) 9.1 s per us (t 9.14e-6..1.25e-5) -> ratio ~4.1
(cumulative ClockTime at ~1.2e-5 s: 401 vs ~80 s -> ~5x). r225 full 3 ms = 42,239 s.
Projection full 3 ms at 12 ranks: ~48-59 h (4.1-5.0 x 42,239 s).
Lower bound with perfect scaling: cells x3.45, dt ~x1/1.51 (same maxCo), ranks x2 -> 2.6 x 42,239 s = ~30.5 h.
Both exceed the 18 h limit -> per job rule r340 NOT launched. No GCI r150/r225/r340 recompute.
Options for Claude: (a) r340 on more cores elsewhere (would need ~32+ ranks for <18 h even at ideal scaling),
(b) accept r225 + G1 noise floor (A2 spray NOT converged within noise per G1_RESULT), (c) shorter window (to t_eoi 2.0 ms = ~2/3 of cost, still >18 h).
