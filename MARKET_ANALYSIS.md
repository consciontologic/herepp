# herepp market analysis and final planning assessment

Research date: 2026-09-10  
Objective: a profitable, founder-operated side business.  
Status: completed planning assessment with unvalidated commercial assumptions. This is not evidence of a launched or profitable product.

## 1. Assessment

**Proceed to a narrow paid validation pilot. A complete phone-first experience is a credible reason to choose herepp; demand, delivery quality and sustainable payment behavior still need to be demonstrated.**

The earlier assessment gave too little weight to completing the entire workflow on a phone. Matching generated HTML features does not establish that competitors offer an equally easy creation, installation and recovery experience for nontechnical customers. This strengthens the product hypothesis. It does not establish a unique market position or justify increasing subscriber forecasts without evidence.

The opportunity is to make a particular everyday task easy enough that a reachable group pays for the convenience. The largest uncertainties are customer acquisition, installation and support effort, and whether users repeatedly need paid creation. Small inference and hosting bills help the economics but do not resolve those uncertainties.

## 2. Product assessed

The current product contract is defined in [BLUEPRINT.md](BLUEPRINT.md), implemented in the plan in [ROADMAP.md](ROADMAP.md), and illustrated in [USER_JOURNEY.md](USER_JOURNEY.md).

- Flutter is a phone-first authoring and delivery interface: text, reviewed voice transcripts, clarification, status, purchases, downloads and external-browser installation guidance.
- Go sends a constrained request to Gemini, validates the returned definition and compiles trusted HTML. AI-generated arbitrary executable code is outside the MVP.
- One downloadable HTML file runs independently outside Flutter. Flutter never previews, renders or executes the tool.
- Optional explicit publication produces a static HTTPS PWA companion with HTML, manifest, external service worker and icons. Customers do not manually unpack or upload assets in the managed installation journey.
- Everyday calculations and records stay local. Authoring requires the backend and AI provider. Initial PWA installation, updates and code recovery require static hosting.
- A downloaded HTML file is not a universally installable single-file PWA. Offline readiness, home-screen placement and record recovery are separate requirements.
- MVP tools are constrained calculators, checklists and loggers. Reliable local backup/import is essential.

The mobile installation route must be available directly from the result screen without requiring an HTML download first. Keep both delivery choices, explain publication visibility, and preserve private download-only use.

## 3. Why mobile first matters

### A concrete customer situation

A cleaner, already at a job site, says:

> Make a quote calculator using room count, floor area and optional window cleaning.

Herepp asks for the missing rates and formula instead of inventing them. The customer reviews the transcript and requirements, receives the completed tool, chooses the phone-installation route, and follows the external browser's guide. They reopen the installed calculator and check its results against a known quote. The tool works independently after offline preparation.

This is an intended experience, not an implemented demonstration. The result remains constrained to owner-checked arithmetic: invoicing, tax advice, payment collection and shared customer records are outside this pilot.

### The advantage to demonstrate

| Part of the experience | Potential customer value | Evidence needed |
| --- | --- | --- |
| Voice/text creation where a need arises | Avoids waiting for access to a computer | Target users complete real tasks on their phones |
| No model-key or technical setup | Reduces friction for nontechnical customers | Fewer setup failures than accessible alternatives |
| Small, predictable capabilities | Easier interpretation and verification | Correct output for supported requests; honest rejection otherwise |
| Guided installation | Turns a generated file into a usable phone tool | Unassisted browser handoff, installation and offline restart |
| Local independent use | Continued usefulness after authoring ends | Reopening and recovery work without Flutter or the authoring API |
| Custom branding | Useful when showing a tool to customers | Actual payment for a bounded branded deliverable |

A native prompt screen alone does not establish this advantage. Downloads, publication choices, browser switching, offline preparation and backup must all be understandable. A handoff that repeatedly requires founder assistance weakens both customer value and margins.

Suggested positioning:

> **Create your own everyday tools, directly from your phone. Keep using them independently.**

This positioning describes the intended benefit. Avoid promising instant installation, permanent browser storage, zero maintenance, universal browser support or unique technology.

## 4. Competitors and substitutes

The following are dated public product claims and price observations. They are not independent output-quality tests, traction audits or proof of willingness to pay. Proprietary credits are not equivalent to herepp queries.

| Alternative | Observed overlap | Implication for herepp |
| --- | --- | --- |
| SaaSet | Markets downloadable single-HTML apps, independent use and continued operation after cancellation. Standard listed at $9.90/month. | Offline ownership is already a competing proposition. Compare actual phone completion and correctness. [Product](https://saaset.com/), [pricing](https://saaset.com/pricing) |
| GenSiteHub | Advertises mobile-ready, self-contained offline HTML and an external Android packaging route; free builder with a customer-supplied OpenRouter key and separate model costs. | Herepp can test whether removing key setup and guiding PWA installation is meaningfully easier. Android packaging is a different journey. [Product](https://www.gensitehub.com/) |
| Claude artifacts | HTML artifacts and file downloads are available through a general assistant, including Free accounts. Output dependencies determine offline behavior. | Customers may already have a substitute. Benchmark getting a usable independent tool, not just generating code. [Artifacts](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them) |
| Anything | Its November 2025 iPhone announcement describes phone-based app creation and voice prompting, with broader backend and publishing capabilities. | Mobile authoring itself is not unique. A focused independent-tool journey still merits comparison. The announcement does not prove current output quality or phone-only completion. [iPhone announcement](https://www.anything.com/blog/anything-ios) |
| Lovable | Broader app building and publication; Pro listed at $25 with monthly billing. | Competes for attention and creation budgets, although its full project workflow is not equivalent to standalone local HTML. [Plans](https://docs.lovable.dev/introduction/subscription-plans) |
| Memento | Advertises unlimited free local mobile libraries and offline functionality. | Personal loggers face capable free substitutes. [Plans](https://mementodatabase.com/pricing.html) |
| Track & Graph | Free local tracking; Google Play displays 50K+ cumulative downloads. | Evidence of category usage, not active users, paying demand or herepp's reachable market. [Listing](https://play.google.com/store/apps/details?hl=en&id=com.samco.trackandgraph) |
| Calconic | Hosted calculators with branding removal; an entry price equivalent to $5/month on annual billing. | Branding is worth testing for customer-facing tools. An asking price for hosted calculators does not establish herepp willingness to pay. [Pricing](https://www.calconic.com/pricing) |

The older Anything iOS documentation URL redirected to a testing page during the follow-up. Its stale search excerpt was not used to establish current app availability or Android availability. The linked dated launch announcement supports the narrower observation that phone/voice authoring has already been marketed.

## 5. Customers worth testing

1. **Solo makers and service operators:** manual-input estimate calculators using customer-supplied rates and verified formulas. A specific repeated task and optional branding give a concrete offer. This is the first commercial hypothesis, supported indirectly by existing calculator products, not validated herepp demand.
2. **Hobby users:** reading, gardening or craft logs are a good technical fit and clear demonstration. Free alternatives and infrequent creation may limit payment.
3. **Tutors or workshop creators:** repeatedly distributing simple tools could create repeat authoring demand. No direct payment evidence for this segment was established in this research.

Choose the first pilot audience based on who the founder can actually reach. Do not expand the capability set to accommodate unrelated bespoke requests before verifying a repeatable supported job.

## 6. Monetization assessment

The agreed baseline remains:

- Free: three submitted AI queries per calendar week.
- Premium: no weekly cap, 100 AI queries per monthly entitlement period, custom PWA logo, removal of the herepp watermark, no Flutter ads while entitled, and no bundled ad panel in new authorized artifacts.
- Existing clean tools remain clean and usable after cancellation. Installing, reopening, downloading and local backup do not consume AI quota.
- Basic PWA publication, if offered, has disclosed capacity and retention. Paid hosting capacity and custom-domain options belong to v2.

Price is not selected. The $7.99 used below is only an analytical scenario. Publish the 100-query limit prominently; use “unlimited use of existing tools,” not unqualified unlimited generation.

### Renewal risk

A customer can pay for one month, create several clean tools, cancel and use those tools indefinitely. Three free weekly queries may already satisfy occasional authors. Conversely, clarification submissions can consume those queries before one useful tool exists. Measure queries-to-useful-tool as well as usage of the allowance.

**Continued installed-tool use, new authoring and paid renewal are three different behaviors.** Mobile convenience could improve the first purchase without improving renewal. The independent-use promise should not be weakened to force subscriptions.

Test a one-time clean-artifact purchase or finite creation pack alongside Premium for occasional creators. These are research alternatives, not newly approved plans, prices or unlimited future service commitments. Repeat creators may better fit subscriptions.

### Advertising and hosting

Assume no ad revenue before it is secured and measured. The free generated artifact contains a static embedded sponsor/house panel, not a network-impression business. Flutter may have little repeat exposure once customers leave to use their tools.

V2 managed hosting can sell stable URLs, distribution, update delivery and code recovery. It does not back up local records. Its demand, capacity, cancellation terms and support costs require separate validation. No hosting income is included below.

## 7. Conditional financial model

All figures are USD for a hypothetical typical operating month. Subscriber counts have no forecast date or probability. Assumptions are unmeasured and should be replaced with pilot evidence.

| Input | Reference hypothesis |
| --- | --- |
| Monthly Premium price | $7.99 |
| Payment/platform expense allowance | 20% of revenue |
| Refund/failure reserve | 5% of revenue |
| Pooled paid and free author AI expense | $0.75 per paid subscriber-month |
| Replacement acquisition | 10% monthly paid churn × $10 per acquired payer = $1 per paid subscriber-month |
| Fixed operating cash expense | $150/month |
| Founder workload | 40 fixed hours/month plus 3 support minutes per paid subscriber-month |
| Founder time valuation | $25/hour |

The fees are allowances, not confirmed store terms. The pooled AI cost does not establish a free-to-paid ratio or guarantee capacity. The workload and retention assumptions are favorable and unvalidated; additional free or legacy-user support worsens results.

Cash contribution per subscriber-month is $7.99 × (1 − 0.20 − 0.05) − $0.75 − $1 = **$4.2425**. Variable founder support costs $1.25, leaving **$2.9925** after valuing that time. Fixed costs are $150 cash, or $1,150 including fixed founder time.

| Active paid subscribers | Revenue | Operating cash surplus | Assumed founder hours | Result after founder time |
| ---: | ---: | ---: | ---: | ---: |
| 100 | $799.00 | $274.25 | 45 | −$850.75 |
| 300 | $2,397.00 | $1,122.75 | 55 | −$252.25 |
| 1,000 | $7,990.00 | $4,092.50 | 90 | $1,842.50 |

Under these inputs, monthly break-even rounds up to **36 active payers for cash expenses**, or **385 including founder time**. Neither repays initial development. A population of 1,000 payers is already substantial ongoing work for a side business; no evidence shows it can be acquired at the assumed cost.

### Sensitivity at 300 active payers

| Changed hypothesis | Cash surplus | Result after founder time |
| --- | ---: | ---: |
| Reference | $1,122.75 | −$252.25 |
| Price $4.99, holding population constant only for comparison | $447.75 | −$927.25 |
| Churn 20% and acquisition $20/payer | $222.75 | −$1,152.25 |
| Pooled AI expense $3/payer-month | $447.75 | −$927.25 |
| Support 10 minutes/payer-month | $1,122.75 | −$1,127.25 |

These are arithmetic sensitivities, not price-elasticity estimates or industry benchmarks. Higher replacement acquisition makes contribution after variable founder support slightly negative; additional volume would not solve that case.

The model excludes initial development/equipment, initial and growth acquisition, taxes, settlement timing, financing and exceptional support. Cash surplus is not a cash-flow forecast or disposable personal income. There is no assumed advertising, hosting or one-time-sale revenue.

RevenueCat's 2026 report provides context for subscription risk, including weaker median twelve-month retention for monthly AI subscriptions in its selected app sample. It does not estimate herepp churn, conversion or success probability. [Research](https://www.revenuecat.com/state-of-subscription-apps)

## 8. Validation and decision gates

The following are proposed pilot thresholds, not completed work or statistically established benchmarks:

1. Choose one reachable niche and a bounded paid offer. Interview about 20 qualified unrelated prospective users about recent tasks and existing workarounds.
2. Observe 10 users attempting a supported task on their phones. Compare herepp with accessible alternatives, using the same task and including external installation, offline reopening and recovery. Do not require a laptop or give hidden founder assistance.
3. Aim for at least 8 of 10 completing the installation/offline flow unaided. No silent record loss or incorrect accepted calculation is acceptable in the tested flows. Treat the small sample as directional evidence.
4. Seek at least five genuine paid commitments or purchases with clear delivery terms; distinguish an expression of interest, a commitment and a completed payment. Do not present a prototype as a live service.
5. After paid launch, observe first and second renewals. Record tool use, new creation and renewal separately. Use participant feedback and authoring/billing data; do not add runtime record tracking to obtain metrics.
6. Measure real provider expense, acquisition cash and founder effort, support minutes and refunds. Set the cash and time budget before the experiment; none has been selected or spent by this analysis.

Expand when payment, reliable self-service delivery and contribution after founder time support the desired return. Rework packaging when tool use continues but authoring and renewal do not. Pause expansion when free substitutes are equally convenient, requested capabilities exceed scope, or support makes the economics unattractive.

## 9. Final planning decision and open items

The selected direction is a **phone-first creator of small, independent personal tools**, with an optional managed PWA installation journey. Keep the constrained architecture and requested Premium bundle as the planning baseline; validate one niche before expanding. Mobile first receives greater weight as an experience advantage, while uniqueness and repeat paid demand remain unproven.

Before a paid release, resolve target niche/geography, price/currency, founder time and income goal, pilot budget, basic hosting limits/retention and supported device/browser versions. These are explicit open decisions, not reasons to invent a forecast or claim readiness.

The planning documentation is complete for handoff. Implementation, real-device acceptance, live AI evaluation, customer research and paid validation remain outstanding. [ROADMAP.md](ROADMAP.md) defines the implementation sequence and release gates.
