# herepp blueprint: local HTML apps with minimal hosting

Date: 2026-09-10  
Status: finalized planning baseline; implementation and browser behavior still need validation.

Architecture correction: Flutter is the authoring and delivery interface only. The generated HTML runs independently in the user's browser and is never rendered or executed inside Flutter. ROADMAP.md implements this same boundary.

For concrete customer examples, see [the end-to-end user journey](USER_JOURNEY.md): a reading-log prompt in Flutter, Go's HTML build, portable download, static PWA assets, phone installation, and independent offline use.

## Mobile-first positioning and commercial validation

The intended benefit is **creating useful independent tools directly from a phone**. Evaluate the entire text/voice-to-tool journey, including external installation, offline reopening and recovery. A Flutter prompt screen alone does not prove the advantage. Keep Download HTML and Install on phone as distinct choices; customers choosing installation need not download or unpack files first. Publication remains explicit.

[MARKET_ANALYSIS.md](MARKET_ANALYSIS.md) consolidates the market research, the stronger weighting of mobile-first convenience, conditional economics and paid-pilot gates. Mobile creation and offline ownership have competitors; validate a narrow audience and self-service completion before broad expansion. Premium remains the requested baseline, with price unselected; one-time exports/packs are research alternatives. Planning completion does not establish customer demand or software readiness.

## 1. Product contract

**Describe a small personal tool in Flutter using text or voice, receive a downloadable HTML file from Go, and run that file independently of herepp. Its logic and records stay on the device, with no application backend required during everyday use.**

The priorities are:

1. No server-side generated-tool logic, remote record database, authentication dependency, or runtime AI calls during everyday tool use.
2. One downloadable `app.html` containing the UI, JavaScript, CSS, and required assets.
3. Offline operation for every capability advertised as supported.
4. Minimal static hosting for discovery, downloads, and optional mobile installation.
5. Metadata generated once when publishing, rather than rendered on every visit.
6. Explicit export and restore so users can recover their records without cloud storage.

Flutter accepts prompts, displays clarification or unsupported results, manages creation requests and purchases, downloads completed artifacts, and gives browser-specific installation instructions. It has no generated-tool runner, HTML preview, WebView, native storage bridge, or generated-record database. Its optional local history contains authoring definitions and download details, not the records people enter into their generated apps. Free Flutter authoring screens may show ads; purchasing and advertising remain outside the generated tool's local execution.

“Local-only” describes the generated app's processing and records. Authoring and AI-assisted editing are online. Downloading an app, opening a sharing page, preparing a PWA for offline use, and checking for a new app version can contact hosting. None of those operations should transmit the generated app's records.

There are two unavoidable boundaries:

- **A literal downloaded HTML file cannot provide a universally installable, reliably offline PWA across platforms.** Some browsers can install sites without a service worker, but the offline PWA delivery supported here uses HTTPS and a separately served worker script, plus a manifest and installation icons. Embedding worker source in the HTML does not remove that URL requirement. [Service-worker registration](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register)
- **Server cost is broader than metadata rendering.** Go receives authoring requests, calls the AI provider, validates the result, builds the HTML, enforces budgets, and delivers the artifact. Optional PWA installation also requires continuing static asset hosting. Everyday tool use needs no API service; creation and distribution still have costs.

## 2. Deliver one app in two forms

Keep `app.html` as the primary artifact. Offer a small static PWA wrapper for people who want a mobile home-screen app with normal browser storage.

| Property | Downloaded HTML | Static PWA delivery |
| --- | --- | --- |
| Distribution | One HTML file | HTML plus worker, manifest, and installation icons |
| First use | Save the file outside Flutter, then open it in a compatible browser | Open a stable HTTPS URL in the external browser and prepare offline resources |
| Offline app logic | Yes, with all dependencies embedded | Yes, after offline preparation completes |
| Durable records | Explicit export/import is the portable baseline | IndexedDB autosave, plus export/import |
| Mobile installation | No universal home-screen installation promise | Browser/OS-specific install or home-screen flow; verify the resulting behavior |
| Server work during a calculation or save | None | None |
| Recovery after local storage is cleared | Import a previously exported backup | Reload code from hosting, then import a backup |

**Recommendation:** make a downloadable HTML file the primary deliverable and offer a separate static PWA companion for mobile installation. The file remains independent of Flutter. A downloaded file does not become a PWA merely because it contains a manifest or an “Install” button. If only a share page may be hosted, offer file delivery with its installation and saving limitations.

For file URLs, `localStorage` behavior is undefined across browsers. It may be used as a tested convenience, never as the only promised recovery mechanism. Mobile file viewers may also display HTML without providing the browser environment needed to run the app. Publish support only for opening flows verified on real devices. [File-URL storage behavior](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)

### Browser installation guidance

Flutter provides an “Open installation link” action and instructions for the user's browser/OS. It opens the PWA's HTTPS URL in an external browser; downloading the HTML and installing a hosted PWA are separate actions. It cannot bypass a browser's eligibility checks, force a home-screen installation, or install a generated app itself.

Use Safari's documented Add to Home Screen / Open as Web App flow as the authoritative iPhone fallback. Other iOS browsers may expose home-screen actions, but their available menus and behavior must be verified for the supported browser and OS version. On Android, supported browsers may offer an Install action, a WebAPK-backed experience, or an ordinary home-screen shortcut; those outcomes are not interchangeable. Do not label a shortcut as proven offline installation.

ROADMAP.md contains the browser-specific instruction matrix and source links. Maintain a dated real-device support matrix before release; provide a Safari/Chrome fallback when the current browser cannot complete the tested flow. A service worker supplies offline behavior in this design; it is not a universal prerequisite for every browser's install UI.

## 3. Architecture

```text
CREATION / EDITING — occasional work

Flutter: text prompt or reviewed voice transcript
       -> authenticated request to Go
       -> capability check + AI-generated structured specification
       -> schema/semantic validation + trusted deterministic HTML build
       |
       +--> unsupported / clarification message, with no runnable artifact
       |
       +--> authenticated app.html download
       |      -> Flutter Download button -> OS save/share UI
       |      -> user-controlled file outside the Flutter app sandbox
       |
       +--> optional, explicitly published static PWA companion
              -> stable HTTPS URL + HTML + SW + manifest + icons
              -> external browser + installation guidance

EVERYDAY USE — on the user's device

External browser: app.html or installed PWA
       -> trusted local rendering and calculations
       -> file-mode state or browser records
       -> export / import files

No Flutter execution, runtime API, remote record store, or server computation.
```

The AI can still return constrained JSON internally. Go compiles it with an approved runtime into the final HTML; Flutter receives completed artifact metadata and downloads the actual HTML bytes. Returning HTML to the customer does not require asking the AI to write arbitrary executable code.

For voice, start with OS-native speech recognition or keyboard dictation. Show the transcript for correction before submitting it as an ordinary text prompt. Recognition availability, language support, and whether audio is processed on device depend on the platform and recognizer; do not promise offline/private transcription without verification. A cloud transcription service would be a separately disclosed and metered feature. No audio is embedded in generated tools.

A single Download tap starts the native download/save flow; the OS may require a destination or share-sheet choice. A file held only in Flutter's private storage is not the completed portable delivery. Verify export to a user-controlled Files/Downloads location on actual devices. Flutter never opens the generated artifact in an embedded renderer, including for previews.

## 4. Metadata needs no per-request rendering

At publication time, write these values into the initial HTML response:

- Page title and description.
- Open Graph title, description, URL, type, and image URL.
- Social-card metadata where useful.
- A canonical public URL.

Generate one preview image at build time, or use a shared static image initially. Serve the page and image as ordinary static files. Crawlers receive the metadata without running JavaScript or calling an application server. Open Graph defines these values as HTML metadata. [Open Graph protocol](https://ogp.me/)

Use a separate sharing page when the app itself is distributed privately as a file. A local file cannot provide a remotely fetchable link preview. Publication is an explicit choice: private download only, an unlisted hosted companion, or deliberate public sharing. An unlisted URL is accessible to anyone who obtains it and is not private access control. Publish only the title, description, image, and app definition the creator chooses to expose; never derive a public preview from their saved records. A user who requires private hosted access needs a separately designed access-control option or self-hosting; that is outside the unauthenticated static-hosting baseline.

Treat public metadata as untrusted text during building: escape attributes, bound lengths, and validate URLs. Use stable public URLs without access tokens. Metadata changes require rebuilding the static page; social platforms may retain their previous preview until their caches refresh.

**A dynamic metadata function is unnecessary for the initial version.** If introduced later, render on a metadata-version cache miss and cache the result. Record its cost separately.

## 5. Artifact and hosting layout

Illustrative paths, not existing deployments:

```text
Local build output
  exports/<app-id>/app.html
  public/a/<app-id>/index.html
  public/a/<app-id>/sw.js
  public/a/<app-id>/manifest.webmanifest
  public/a/<app-id>/icons/icon-192.png
  public/a/<app-id>/icons/icon-512.png
  public/a/<app-id>/icons/apple-touch-icon.png
  public/share/<app-id>/index.html
  public/share/<app-id>/preview.png
```

The exported HTML omits PWA registration and external installation metadata. The hosted HTML uses the same application runtime and app specification, with a delivery-specific bootstrap.

Go produces the downloadable file with an attachment response and a bounded filename. Flutter authenticates the download, checks the expected size/hash, and hands the bytes to native save/share APIs. Generation JSON and the internal AI schema are control messages; neither substitutes for delivering the completed HTML file. Keep credentials and download authorization out of the HTML, public URLs, and share metadata.

Use a static host/CDN with HTTPS, response-header configuration, and controlled publication of versioned artifacts. No continuously running application process or per-app server is needed. Check the host's file-count, deployment-size, custom-domain, and request limits before choosing it.

Static delivery can be extremely inexpensive. For example, Cloudflare documents free and unlimited static-asset requests when served without invoking Worker code, subject to its platform limits. This does not make AI generation, custom routing functions, domain registration, or every possible hosting arrangement free. [Static-asset billing and limits](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/)

**Keep published PWA URLs stable. Do not delete an app ten minutes after installation.** Preserve the current build and a bounded number of prior builds for repair. Temporary private generation-result/download retention is a separate policy; expiring those private results must not remove an explicitly published PWA. An expired download can require a fresh build or import of the user's retained source definition. Changing an app's origin can separate it from its existing browser storage, so origin changes need an export/import migration path.

## 6. Build the HTML without runtime dependencies

Bundle everything required for the supported experience:

- Inline compiled CSS; no Tailwind browser/CDN compiler.
- Inline trusted JavaScript; no remote module imports.
- System fonts and embedded icons/images.
- Inline only the charting or export code actually needed.
- No analytics, remote fonts, external images, or automatic update SDKs.
- No API keys in artifacts.

The free artifact may include a bundled, clearly labeled static sponsor or herepp promotion panel. Its artwork and text must be embedded and work without an ad server, tracking pixel, SDK, remote image, or runtime entitlement check. This is the initial PWA advertising format; it does not imply guaranteed advertising income. Premium builds omit the panel. See the monetization contract below for Flutter ads and any later network-ad option.

Start with ordinary JavaScript and IndexedDB for hosted delivery. SQL is not necessary for a small logger, list, or calculator. Introduce SQLite only when a demonstrated query or data-volume requirement justifies its additional binary and storage machinery.

COOP/COEP is not a default requirement for this design. SQLite's `opfs-sahpool` option also demonstrates that those headers are not universally required for SQLite persistence. [SQLite persistence options](https://www.sqlite.org/wasm/doc/trunk/persistence.md)

Use a provisional artifact-size budget of 1 MiB for the basic HTML before transfer compression, excluding user-imported records. This is a design target to benchmark, not a performance guarantee. Large embedded models and media do not belong in the first version.

## 7. Generate within a trusted runtime

A strict prompt cannot guarantee valid or safe arbitrary JavaScript. For the first version, have the model produce a validated app specification, then have Go compile it into HTML using trusted code. The trusted runtime is bundled into the output and executes only when the user opens the artifact externally.

The compiled artifact's definition envelope describes the following; Go assigns identity/version metadata, and the model supplies only schema-permitted tool choices. The MVP subset is defined in ROADMAP.md; the broader screen/component catalog is a later extension.

- Stable app identity, app version, and data schema version.
- Typed fields, defaults, validation, and stable field IDs.
- Screens assembled from supported forms, lists, buttons, charts, and text.
- Operations such as create, update, delete, filter, sort, and aggregate.
- Calculations expressed through a bounded expression grammar.
- Theme choices and the required supported capabilities.

Do not accept executable scripts, arbitrary HTML/CSS, arbitrary URLs, or JavaScript expressions through this specification. Evaluate supported formulas with a small parser/interpreter, not `eval()` or `new Function()`. Render user text as text. Validate embedded specification data so strings cannot break out of script or markup contexts.

This intentionally limits what users can build. An unsupported request should explain the missing capability before generating an app that appears to support it.

Preserve a bounded, non-executable authoring definition with each generated app so it can be edited without uploading its records. Flutter can retain this definition or import the definition section from an artifact without executing its HTML. Go owns artifact identity, runtime version, revision metadata, and validation; the model cannot assign privileges or choose storage namespaces. Publishing rights are checked against the authenticated creator, not established by possession of an app ID.

## 8. Data persistence and recovery

### Hosted PWA

Use IndexedDB through a trusted storage adapter. Namespace records by app identity and version the data schema. Commit writes transactionally and show “Saved on this device” only after the transaction completes. On write failure, keep the user's current input available and offer export; do not silently fall back to temporary memory while claiming a save succeeded.

Check available storage and request persistent storage where supported. The browser decides whether to grant the request. An installation or granted persistence request does not replace backup. [Persistent-storage requests](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist), [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/)

### Downloaded HTML

Make explicit saves the baseline:

1. The user opens `app.html` and works locally.
2. “Export backup” creates a JSON file containing the app ID, schema version, records, and export timestamp.
3. “Import backup” validates and restores that file.
4. Optionally, “Save portable copy” creates a new HTML file with a snapshot of those records embedded.

A downloaded HTML file generally cannot silently overwrite itself after every edit. The portable copy is a new file, and subsequent edits require another explicit save. Browser download/share dialogs control where the file goes. Do not promise an automatic write into a particular mobile Downloads folder.

Mark file-mode changes as unexported and provide an obvious save action. A page-close warning is only a convenience; mobile termination may bypass it.

### Rules shared by both modes

- Export and restore must work offline.
- Keep “Share blank app” separate from “Export my records.”
- Treat backups as private files; local-only does not imply that exported JSON/HTML is encrypted.
- Validate app identity, schema version, types, size limits, and record counts before importing.
- Restore transactionally, with a recoverable copy of existing records; malformed files must not partially replace data.
- Preserve raw user values when importing, but never interpret them as code or markup.
- A snapshot in the same browser database helps recover from a bad edit, but cannot recover from browser-storage deletion.
- A new phone starts with no records until the user imports a backup. A shared app URL does not synchronize data.

Clearing site data can delete the app's local database and caches. Hosting can recover the app code; only a separate backup can recover lost records. [OPFS and site-data deletion](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system)

## 9. Offline readiness and safe updates

Use a platform-owned service worker for hosted delivery. Never ask the model to generate it.

1. Scope the worker to `/a/<app-id>/`; avoid an application-wide root worker that controls other apps.
2. Cache the exact HTML build and its required installation assets with a versioned inventory.
3. Fail preparation if required resources cannot be cached. Do not declare offline readiness based only on home-screen installation.
4. Show offline readiness only once the page is controlled and the required cached build has been verified.
5. Serve the active app from cache during ordinary use. Background browser checks for worker updates may still contact the static host.
6. Stage a complete new build before offering to activate it. Do not force activation halfway through a form submission.
7. Preserve compatible previous assets until active clients no longer need them. Never remove another app's cache.

App-record writes do not trigger HTTP requests. Disable external-resource and runtime-API paths instead of queuing network operations for later. There is no synchronization subsystem in this version.

Offline launch depends on the local cached copy still being available. Do not claim “runs forever,” “zero load time,” or “installation guarantees permanence.” [Offline and background lifecycle](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation)

For data-schema changes, initially allow only compatible additive changes with stable field IDs. Stage and validate the new representation before committing. Destructive changes require an explicit data transformation and backup; they are outside automatic MVP editing. Rolling back HTML alone is unsafe if its expected schema no longer matches the records.

AI-assisted edits send only the prior source definition and the requested change through Flutter to Go. Never request a record backup to perform a label, formula, or layout edit. Preserve app identity and field IDs, compare the base revision before publishing, and create a new artifact version. The user keeps a separate backup before moving records into an edited downloaded file; Go and Flutter cannot overwrite an arbitrary external file or migrate the user's browser database remotely. For a PWA, the external runtime stages a compatible update and asks before activation while preserving the same app identity and origin. An older downloaded file remains an independent copy.

## 10. Privacy and app isolation

The MVP may serve multiple apps under one static origin **only because every app executes the same trusted runtime and accepts a non-executable specification**. App IDs prevent accidental record collisions; they are not browser-enforced security boundaries. A vulnerability in the trusted runtime could expose other apps' data on that origin.

If arbitrary generated JavaScript, uploaded executable HTML, or third-party plugins are introduced, require separate app origins and an isolated preview environment before releasing that feature. Different paths on one origin do not isolate IndexedDB or other origin storage. Keep any builder account interface on a separate origin from app execution. [Browser origin boundaries](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy)

Defense in depth for the trusted runtime:

- Apply a restrictive Content Security Policy; allow only approved runtime scripts and embedded resources.
- Block application fetch, WebSocket, beacon, forms, remote frames, and remote media pathways that the local-only product does not need.
- Account separately for the hosted worker's required static-asset fetching and update policy.
- Do not allow app specifications to introduce navigations or network destinations.
- Set restrictive permission policies for hardware outside the supported capability set.
- Use a compatible meta CSP for the downloadable file, recognizing that it cannot replace every HTTP-header policy.
- Audit the runtime and inspect network activity during real workflows. CSP alone does not prove arbitrary code cannot disclose data, and a static code scan alone is insufficient.

Hosting necessarily sees ordinary requests for app files and public share pages. Prompts sent to a remote model leave the device. Free Flutter advertising introduces a separate, disclosed online flow in the authoring interface; it must not receive prompts, transcripts, app definitions, or generated-tool records. Disclose those distinct flows; keep saved app records out of prompts, URLs, telemetry, and publishing payloads.

## 11. Capability decisions

| Original capability | Decision under this blueprint |
| --- | --- |
| Database | Local structured records; IndexedDB for hosted mode and explicit backups for portability. |
| Backend logic | Move supported calculations and record operations into the trusted local runtime. |
| Network and synchronization | No runtime network dependency or cloud sync; manual export/import between devices. |
| Location | Later, foreground-only and device-tested; map tiles/geocoding need separate offline data if offered. |
| Bluetooth | Excluded from the cross-platform MVP; investigate separately for explicitly supported devices. |
| Wi-Fi/local network | Excluded; no SSID scanning or local-network discovery promise. |
| Camera and microphone | Excluded from generated-tool MVP; later only with explicit permission and tested local processing. Flutter voice authoring is a separate input feature. |
| Games | Later, small bounded offline games; no general 60 FPS or full hardware-access promise. |
| Notifications and timers | Visible foreground timers only initially. No guaranteed closed-app or locked-screen alarm. |
| Accounts and external login | None inside generated apps. Ownership of local records requires no account. |
| Local AI | Excluded initially. Later models must be bundled/cached and benchmarked on target devices. |
| Audio | Basic foreground sound after user interaction; no background reliability promise. |
| Payments | Excluded from local-only generated apps. Herepp Premium and future hosting purchases belong to the online authoring/account service. |
| Export | JSON backup and CSV first; embed a PDF library later if a validated use case needs it. |
| Physical diagnostics | Excluded initially; sensor availability and accuracy must be verified individually. |

For the workout example, calculate elapsed time from timestamps so the display can recover after suspension. This repairs the displayed countdown when reopened; it does not guarantee a bell at the target time while the app is suspended. Service workers are event-driven and may be stopped by the browser. [Background execution constraints](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation)

## 12. Monetization and plan contract

The requested paid benefits are custom PWA logos, removal of the herepp watermark, removal of Flutter and generated-PWA ads, a larger AI query allowance, and optional paid hosting in v2. The initial packaging below groups the first four benefits into **Premium**. Prices, separate add-ons, and hosting limits remain product decisions to validate; no price or revenue is assumed here.

| Benefit | Free | Premium, proposed initial bundle |
| --- | --- | --- |
| AI creation and editing queries | 3 per calendar week | 100 per subscription month |
| Existing downloaded tools and cached PWAs | Unlimited local use, subject to device storage and the stated hosting/recovery policy | Same unlimited local use; no ongoing subscription check inside the tool |
| PWA logo / installation icon | Herepp's default icon treatment | Upload a custom logo for PWA manifest icons and Apple touch icon; rebuild the install assets |
| Herepp watermark | Visible herepp footer in generated HTML and PWA | Omitted from newly built HTML and PWA versions |
| Flutter ads | Ads may appear in online authoring screens | No Flutter ads while the entitlement is active |
| Generated HTML / PWA ads | Bundled static sponsor or promotion panel | Panel omitted from newly built HTML and PWA versions |
| Hosting | Primary HTML download and any explicitly offered, bounded basic shared PWA publication | Premium does not imply unlimited hosted apps, storage, traffic, or domains; optional paid hosting is a separate v2 offering |

### Clear allowance wording

Use **“100 AI queries per month; unlimited use of your existing tools”** for Premium. Do not describe generation as “limitless” or “unlimited” with the actual cap hidden in plan details. Display the allowance before purchase, in the plan details, and beside the prompt action, with the remaining balance and the next reset time. A query is an AI attempt to interpret or change a tool; it is not a guarantee that a supported app will be produced.

The quota policy is:

- Free gets three queries in each calendar week, resetting Monday at 00:00 UTC. Show the reset in the customer's local time. Unused queries do not carry over.
- Premium gets one hundred queries in each subscription-anchored monthly window, replacing the free allowance. An annual payment still supplies one hundred per monthly subperiod, not the entire year's allowance at once. Unused queries do not carry over. Calendar anchoring and plan transitions must be defined consistently in the billing implementation.
- One user-initiated create or AI-assisted edit that passes preflight and is dispatched to the provider uses one query. A valid clarification question or unsupported-result explanation still counts; make this visible before submission. A subsequent user reply that requires another AI call is another query.
- Automatic provider retries and repair attempts belong to the original query and do not consume another customer query. Preflight rejection, deduplicated re-submission, and cancellation before provider dispatch do not consume an additional query.
- If an infrastructure/provider/build failure yields no usable artifact or valid clarification/unsupported outcome, release the reserved customer query. Record any provider spend internally and retain operational rate limits so failure credits cannot create unbounded spend.
- Downloads, installation, offline tool use, export/import, and a deterministic logo, watermark, or ad-treatment rebuild do not consume AI queries. Voice transcription is an input step; the reviewed transcript counts only when submitted as a query. Any future paid cloud transcription has its own disclosed limit and cost.

Go owns the quota and paid entitlements. Flutter displays the server's result; changing client state or an app specification cannot grant extra queries, paid branding, or publishing rights. Quotas protect authoring costs and never disable an existing standalone app.

### Branding, ads, and the independent artifact

Go applies the current branding and advertising entitlement when building the artifact; the AI cannot select paid privileges. Accept bounded image uploads, decode and re-encode them into supported raster icon sizes, and reject executable or unsupported content. The first custom-logo option is an upload, not an unmetered AI image-generation feature. Preserve necessary third-party license notices when removing the herepp marketing watermark.

Free generated tools use an embedded, labeled sponsor/promotion panel so the advertised tool functions remain fully offline. An optional sponsor action may open an external page only after a deliberate tap; keep it separate from record actions, open a separate browser context without a referrer, and never attach prompts, tool definitions, or records to that link. The supported tool must work when the sponsor page is unavailable. Do not sell verified impressions or engagement based on local panels without a separately designed measurement method and disclosure.

Flutter may use native online ads in its free authoring interface. Missing ad connectivity must not prevent opening the interface, retrieving an available download, or reading installation guidance. Premium removes that Flutter placement and omits the generated-tool panel from new builds. Recurring ad revenue is an unproven option, not part of the baseline viability assumption.

Third-party network ads inside a PWA are a later, optional policy change. They would add online requests and privacy obligations beyond the initial static-ad design. They require an isolated advertising surface with no access to app records, no untrusted ad SDK executing on the records' origin, and failure/offline behavior that never blocks the tool. Do not silently enable them under the v1 local-only promise.

Paid clean exports remain clean and usable after cancellation; there are no account, ad, or license checks inside them. Cancellation changes future authoring entitlements and Flutter's ad treatment. Existing free downloads retain their watermark/panel until the owner requests an entitled rebuild and downloads the new version. An existing PWA changes only after an entitled build is published and its update is safely activated; a subscription purchase cannot rewrite already downloaded files or force an offline PWA to update. Browser launchers may retain an old icon until an update or reinstall, so custom-logo delivery needs device testing.

An editable HTML file cannot enforce durable watermark or ad protection. A technically capable recipient can alter it, and a clean file can be shared. Sell the convenient supported build, creation allowance, and optional hosting; do not add DRM or periodic verification that breaks independent local operation.

### V2 hosting options

Paid hosting is a v2 product extension, beyond any basic shared PWA installation offered initially. Keep generation allowance and hosting resources separate: one hundred AI queries does not entitle a customer to one hundred indefinitely hosted apps.

| Hosting option | Scope and charging basis to evaluate |
| --- | --- |
| Download-only | Deliver the self-contained HTML with bounded private download retention. No continuing herepp PWA hosting or universal installability promise. |
| Self-hosted PWA package | Export a static ZIP containing HTML, worker, manifest, and icons, with HTTPS/header/deployment instructions. The customer supplies hosting and a stable origin; package/support pricing, if any, remains undecided. |
| Managed shared hosting | Retain a defined number of published PWA slots on herepp's shared HTTPS host, with explicit storage, traffic, retained-version, and service limits. Offer additional capacity only with disclosed pricing and caps. |
| Managed custom domain | Add a customer's domain or supported subdomain, certificate/routing management, and defined support. Domain registration is a separate cost unless explicitly included. An origin change requires a backup/import migration plan. |

Hosting sells distribution, stable installation URLs, update delivery, and code recovery. It does not include users' record databases, record backups, synchronization, or per-tool application servers. Private hosted access would require a separate design and is not implied by an unlisted link or a paid domain.

Before taking hosting payment, define published-slot limits, bytes and traffic allowances, overage behavior, renewals, and the cancellation/expiry notice and grace period. Do not promise unlimited hosting. Give customers time to export the static package and their local record backups. Preserve published URLs throughout the advertised service period; a ten-minute private-download expiry must never delete an active hosted PWA. After hosting ends, an existing cached installation may still run, but fresh installation, code recovery, and updates cannot be promised. Never remotely disable cached tools to enforce cancellation.

Separate custom-logo, watermark-removal, or ad-free one-time add-ons can be tested later. Their scope must distinguish a permanently clean generated artifact from removal of ongoing Flutter ads; purchasing one must not imply the other unless the offer explicitly includes it.

## 13. Cost model

| Cost | Baseline treatment |
| --- | --- |
| App calculations and record storage | On device; zero platform compute/database cost per operation. |
| Metadata rendering | Once per publication or metadata change; no per-visit renderer. |
| Private artifact delivery | Authenticated Go/object-storage delivery with bounded result retention and byte costs. |
| PWA and share-preview delivery | Continuing static hosting/CDN; provider limits and billing apply. |
| Domain | Ordinary recurring domain cost if using a custom domain. |
| AI generation and revisions | Metered remote inference through the Go authoring API; cap calls, tokens, repairs, and user spending. |
| Build and verification | Deterministic server-side compilation of approved assets plus bounded artifact checks. |
| Authoring control records | Minimal durable authentication, quota, operation ownership, and idempotency state; no generated-tool records. |
| Voice transcription | OS recognition initially; provider-dependent processing and availability. A separate cloud transcription API would add cost. |
| Support and compatibility maintenance | Ongoing human/engineering work; not eliminated by local execution. |
| Payments and entitlements | Payment/store fees, refunds, purchase verification, and durable quota/billing state. Budget using the actual payment route and prices once selected. |
| Branding and free ads | Bounded logo processing and static panel build costs; Flutter ad integration and consent/support work where applicable. Do not assume ad revenue will subsidize every free user. |
| V2 managed hosting | Published slots, storage, traffic, retained builds, domain/certificate operations, and customer support; cap and price separately from AI queries. |

Do not optimize by deleting recoverable app code. Set limits on app size, retained build versions, generation attempts, and build retries. Reuse one trusted runtime and avoid loading unnecessary libraries into every app.

For a public builder, measure generation cost per accepted app and support time per retained user. Track all provider attempts, including credited failures and repairs, to measure the true cost of the free allowance and a Premium customer using all one hundred monthly queries. Static hosting cost alone is not the product's total cost. Choose prices only after including payment fees, refunds, acquisition, support, and the promised benefits; advertising income should be modeled as uncertain upside until measured.

## 14. Build sequence and release gates

### Phase 1: prove the local app contract

Build one hand-authored logger with forms, a history list, a numeric summary, JSON backup, and CSV export. Produce both downloadable HTML and the static PWA companion. Exercise a Flutter Download action and external-browser installation guidance using these fixtures before connecting AI routing.

Release gate: tested offline use, honest save status, portable backup recovery, and a documented file-opening flow on the target devices.

### Phase 2: prove safe customization

Add the validated specification, Go's deterministic compiler, a few trusted UI components, and compatible schema evolution. Connect Flutter's text/reviewed-voice prompt flow to the authenticated Go authoring endpoint. Generate a small collection of calculators, checklists, and personal logs.

Release gate: generated apps perform the requested tasks, preserve records through supported edits, and reject unsupported requests before publication.

### Phase 3: add inexpensive distribution

Deliver authenticated HTML downloads and explicitly chosen PWA publication. Generate static sharing metadata and preview images during publication. Complete browser-specific installation guidance. Retain stable published URLs and bounded previous versions, independently of temporary private result retention.

Release gate: social crawlers see metadata in the initial HTML, a fresh installation works, and interrupted publication cannot replace a working offline build with an incomplete one.

### Phase 4: validate usefulness before expanding

Give the tools to a small group with recurring personal tasks. Record, with their participation, whether they can start unaided, return to use the tools, export/restore successfully, and request worthwhile customizations. Implement the free allowance and Premium entitlement controls, then test willingness to pay for the bundled creation allowance, custom logo, watermark removal, and ad removal. Verify the billing lifecycle before accepting payment; paid managed hosting remains v2.

Release gate: the purchase screen explains the actual one-hundred-query monthly cap, quota accounting survives retries and concurrent requests, and paid build benefits do not introduce a runtime dependency. Confirm that free sponsor panels work offline and Premium removes the promised placements.

### Phase 5: v2 paid hosting

Validate demand for managed published slots, greater storage/traffic allowances, custom domains, and self-hosted package support. Define limits and a sustainable price before implementation. Add publication entitlement checks, usage visibility, migration instructions, and cancellation/export handling while retaining the standalone local runtime.

Release gate: hosting charges and limits are explicit; install/update/recovery behavior matches the advertised retention period; expired hosting never causes loss of records already saved on a customer's device.

Do not add generated-tool hardware integrations, payments, accounts, or cloud features simply to complete the original list of 15 capabilities. Flutter/Go authoring, authorization, and delivery already belong to the core product.

## 15. Acceptance checks

These are implementation gates, not claims already verified in this repository:

- **Flutter boundary:** text and reviewed voice prompts reach Go, supported results offer an HTML download, and unsupported requests produce no artifact. No generated HTML is rendered or executed inside Flutter.
- **Download:** a tap starts the OS save/share flow, delivers the expected HTML bytes to a user-controlled location, and leaves a usable independent file after Flutter is removed. Cancelling the OS dialog must not be reported as a completed save.
- **Standalone:** open the exported HTML in each supported environment with networking disabled; all advertised core features work.
- **First PWA install:** verify required assets finish caching before offline readiness is shown; test interrupted preparation.
- **Offline restart:** create records, close the app, reopen in airplane mode, and verify both app launch and saved data.
- **File-mode saving:** export, reopen/import, and verify all records. Moving or renaming the HTML must not make backup recovery depend on a previous file URL.
- **Storage failure:** simulate denied persistence, a failed transaction, and quota exhaustion; no false “saved” status.
- **Recovery:** clear site data, reload the hosted app, and restore from a separate backup. Confirm that unrecoverable records are not falsely promised to return.
- **Edits:** change a label and add a field while preserving record identity and values. An incompatible change must leave the previous usable state intact.
- **Imports:** reject malformed, oversized, or incompatible files without partially replacing existing records; render markup-like strings harmlessly as text.
- **Isolation:** an app specification cannot select another app's record namespace, inject code, or add a network destination.
- **Network:** normal input, calculation, save, export, and import create no app-originated data requests. Distinguish expected static delivery/worker-update traffic from record transmission.
- **Quota:** the fourth admitted free query in a calendar week and the one-hundred-and-first Premium query in a monthly window are rejected before provider dispatch. Verify reset boundaries, annual-plan monthly subperiods, plan transitions, concurrent submissions, deduplication, automatic repairs, and credited failures. Clarification/unsupported outcomes follow the disclosed counting rule.
- **Premium artifacts:** only a verified entitlement produces a custom-icon, watermark-free, ad-free build. Paid clean files still work after cancellation and in airplane mode. Upgrading alone does not claim to have modified an old download or offline PWA; rebuilding and update activation are explicit.
- **Advertising:** a free generated artifact contains only the trusted static panel and no remote ad resources or trackers. Premium Flutter has no ad placement, and a Premium generated build has no panel. Sponsor navigation requires a tap and sends no tool records or identifiers.
- **Hosting plans:** generation quotas do not bypass slot/storage/traffic limits. V2 cancellation provides the disclosed notice/export/grace behavior and cannot delete local records or remotely disable cached operation.
- **Timers:** lock the phone and reopen; elapsed time is correct, and the UI has never promised an unsupported background alarm.
- **Sharing:** publication follows the selected visibility; initial HTML contains escaped metadata and a fetchable preview image; private records never appear in hosted builds. Expiring a private download does not remove a published PWA.
- **Devices:** test actual iOS Safari/home-screen and Android Chrome/home-screen flows for PWA support; report downloaded-file support separately. Desktop emulation is insufficient for installation and file-opening claims.

## 16. Definition of the first shippable version

Flutter accepts text or a reviewed voice transcript, Go rejects unsupported requests or returns a completed downloadable HTML artifact, and the customer saves the artifact through the OS. One reliable personal logger, one calculator, and one checklist run independently of Flutter. They work offline in supported external environments, have explicit backup/restore, and need no runtime backend. Optional static PWA delivery adds browser-specific installation and browser autosave. Public metadata is built once and served statically. Free authoring has a three-query weekly allowance; the proposed Premium bundle offers one hundred queries per subscription month, custom PWA logos, removal of the herepp watermark, and removal of Flutter ads and newly built artifact ad panels. Optional paid hosting plans follow in v2.

This keeps recurring server work focused on authoring and distribution, while preserving an honest distinction between a portable HTML document and an installed web app whose cached code and browser records still require recovery planning.
