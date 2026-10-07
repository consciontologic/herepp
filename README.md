# herepp

**Create your own everyday tools, directly from your phone. Keep using them independently.**

Planning package finalized: 2026-09-10. The Flutter application, Go service and HTML/PWA runtime are not implemented or deployed. The existing executable utility assembles offline AI request examples.

## Product direction

Flutter collects text or reviewed voice prompts and delivers completed assets. Go validates an AI-generated specification and compiles a trusted standalone HTML tool. Customers run the result outside Flutter, with local computation and records. Optional static HTTPS publication provides a guided phone-installation route; a downloaded HTML file alone is not a universally installable PWA.

The founder objective is a profitable side business. Begin with one narrow paid pilot and prove a complete phone-only customer journey. Calculators, checklists and loggers define the MVP capability boundary.

## Read the planning package

| Document | Purpose |
| --- | --- |
| [MARKET_ANALYSIS.md](MARKET_ANALYSIS.md) | Market evidence, mobile-first opportunity, monetization risks, conditional economics and validation gates |
| [BLUEPRINT.md](BLUEPRINT.md) | Product, runtime independence, delivery, storage, hosting and monetization contract |
| [ROADMAP.md](ROADMAP.md) | Flutter/Go/AI interfaces, implementation phases, configuration migration and release checks |
| [USER_JOURNEY.md](USER_JOURNEY.md) | Text/voice prompt through downloaded HTML and external PWA installation, use and backup |
| [ai/README.md](ai/README.md) | Existing prompt/schema/fixture kit and offline provider-request assembly |

Blueprint and roadmap define the current product baseline. Market-analysis prices, audiences and financial results are hypotheses, not approved commercial terms. Original [idea.md](idea.md), [caveats.md](caveats.md) and [data-types.md](data-types.md) are historical material with superseded assumptions.

## Settled boundaries

- Flutter never renders generated HTML and never stores generated-tool records.
- Go owns AI validation, compilation, authorization, quotas and paid artifact features.
- Runtime AI, record synchronization, background reminders and arbitrary generated scripts are outside MVP.
- Export/import is essential; static hosting can recover app code, not lost personal records.
- Free offers 3 AI queries per calendar week. Premium offers 100 per monthly entitlement period, custom logos, watermark removal and the specified ad removal. Price remains open.
- Paid clean artifacts remain clean and usable after cancellation. V2 paid hosting is separate from generation allowance.
- A phone installation flow must not require downloading HTML first, manual asset unpacking or manual hosting setup. Publication remains an explicit choice.

## Existing utility

From this directory, inspect a provider request without making an API call:

```bash
python3 scripts/build_ai_request.py --input ai/examples/create-request.json
```

This prints the request JSON. It does not create a working HTML app, validate model quality or implement the public Go API. Example backend/Flutter configurations retain prototype settings; complete the migration in roadmap section 12 before using them as application configuration, and implement section 16 before paid release.

## Next action

Build the fixture-based reading-log delivery slice described in roadmap section 15: trusted Go compilation, thin Flutter save/handoff, independent external use and backup/restore, then the static PWA companion. Prove it on real phones before connecting AI. In parallel with implementation planning, select a reachable pilot audience and a bounded offer using the market-analysis gates.

Planning completion does not close implementation or release gates. The final checklist in roadmap section 18 records that distinction.
