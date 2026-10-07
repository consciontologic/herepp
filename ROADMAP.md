# herepp technical roadmap

Date: 2026-09-10  
Stack: Flutter authoring client, Go generation/build API, Google Gemini API, standalone HTML and optional static PWA delivery.  
Status: finalized planning baseline; implementation remains outstanding. The existing AI request kit is a starting point; the application, HTML compiler, delivery endpoints and real-device checks are not implemented.

The [end-to-end user journey](USER_JOURNEY.md) illustrates this implementation contract with a reading log, the exact delivery assets, Android/iPhone installation steps, and supported/unsupported request examples.

For the market evidence and mobile-first commercial hypothesis, see [MARKET_ANALYSIS.md](MARKET_ANALYSIS.md). [README.md](README.md) indexes the finalized planning package.

## 1. Corrected product boundary

**Flutter collects a text or voice prompt, sends it to Go, and lets the user download the completed HTML. Generated tools run entirely outside Flutter.**

This document supersedes the previous proposal for a Flutter tool library, embedded WebView, native storage broker and SQLite records. There is no generated-tool preview or execution inside Flutter, no JavaScript bridge, and no Flutter widget fallback for rendering tools. Flutter may retain authoring drafts, operation receipts and download metadata; it does not own a generated tool’s records.

The generated HTML must continue to function independently after Flutter is closed or uninstalled, provided the user saved it in a user-controlled location and opens it in a compatible external environment. For a PWA, independence means launching its browser/home-screen installation without Flutter. Neither mode has an authoring-account or API-token dependency during everyday use.

| Component | Responsibility |
| --- | --- |
| Flutter | Text entry, voice transcription, transcript review, clarification questions, generation status, download/save handoff, external-browser launch and browser-specific installation instructions. |
| Go | Authentication, capability validation, AI request assembly, specification validation, deterministic HTML compilation, artifact delivery, quotas and optional static PWA publication. |
| Gemini | Produce a constrained tool specification or a clarification/unsupported result. It does not control permissions, installation or hosting. |
| Standalone HTML | UI, calculations, local working state, explicit backup/restore and export, in a compatible external browser/file handler. |
| Hosted PWA companion | The same tool logic, browser storage and offline cache, running in an external browser or home-screen web app. |
| Static hosting | Initial PWA installation, app-code recovery, version delivery, installation assets and static metadata. No user-record processing. |

```text
CREATE / EDIT
Flutter text prompt OR voice -> reviewed transcript
  -> Go HTTPS API -> budget reservation -> Gemini -> validated specification
  -> Go deterministic compiler + verified plan features -> completed self-contained app.html
  -> Flutter Download HTML action -> OS save/share UI -> user-owned file

OPTIONAL PHONE INSTALLATION
Flutter Install on phone -> explain hosted-copy visibility -> publish static package
  -> open stable HTTPS URL in EXTERNAL browser -> browser/OS installation steps
  -> per-tool home-screen launch -> cached HTML + browser database

EVERYDAY USE
External HTML file or installed web app -> local runtime -> local records
  -> local export / import
No Flutter process, native bridge, authoring API or remote AI required.
```

Returning HTML to Flutter does not require the model to invent executable HTML. Go compiles the model’s validated JSON into trusted HTML. The internal AI output contract and the customer’s downloadable output are different contracts.

## 2. Can the output be a single-file, universally installable PWA?

**No, not as one downloaded HTML file across all platforms and browsers.** One file can contain the complete tool logic, styles, assets and initial definition. The reliable phone-installation route is a stable HTTPS web app with a manifest, icons and a separately addressable service-worker script for offline caching.

Service-worker registration requires an HTTP(S) script URL and a secure context in production; a script assembled into a `blob:` or `data:` URL does not provide a portable workaround. A local `file:` HTML cannot register the required worker. An inline/data manifest, even where accepted, does not solve this. Development localhost exceptions are not a consumer installation strategy. [Service-worker registration](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/register)

Installation and offline capability are separate. Some browsers allow adding ordinary websites to the home screen without a service worker. Such an icon does not prove that the tool will start offline. Browser menu labels and OS integration also differ. [Installability and browser differences](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)

Deliver two representations from the same validated source:

| Output | Files and location | Promise |
| --- | --- | --- |
| Portable download | One `app.html`, with embedded runtime, styles, assets and definition | Independent local tool on verified file-opening environments; explicit saves are the recovery baseline. |
| Phone-installable companion | HTTPS `index.html`, `sw.js`, `manifest.webmanifest`, install icons | Browser-specific home-screen installation and offline use after successful cache preparation; continued storage retention is not guaranteed. |

The user downloads one HTML with one action in Flutter, subject to the OS save/share confirmation. That does not silently install a PWA. The result screen must offer distinct **Download HTML** and **Install on phone** actions, not label a downloaded file “installed.”

## 3. Technology choices

| Area | Initial choice | Purpose |
| --- | --- | --- |
| Client | Flutter stable on Android/iOS | Native authoring and file-delivery UI. |
| UI state | SDK ChangeNotifier / repositories initially | Drafts, request status, download state and installation-guide selection. |
| Speech input | Native speech-recognition adapter, with on-device mode where supported | Produce editable text before submission; text input remains available. |
| Downloads | Native document-save/share adapters; bounded temporary cache | Save completed bytes to a user-selected location. Temporary app storage is not successful durable delivery. |
| Browser handoff | Flutter-maintained `url_launcher`, external application mode | Open the PWA HTTPS URL in the real browser; never use an embedded browser/WebView mode. |
| Credentials | Platform secure storage | Individual authoring token only; no provider key in the client. |
| API/build service | Go standard net/http, encoding/json, crypto/sha256, go:embed | Validate, invoke the provider, compile and serve artifacts. |
| AI | Paid Gemini Developer API over REST | Bounded specification generation. |
| Tool runtime | Bundled trusted JavaScript/CSS compiled during development | Embedded into HTML by Go; no runtime CDN or generation-time bundler. |
| Tool storage | Portable in-memory adapter plus explicit files; PWA IndexedDB adapter | Records stay in the generated tool’s external environment. |
| Control store | SQLite for local development; Firestore for Cloud Run | Credentials, verified billing entitlements, quota ledgers, budgets, operation ownership and revision metadata, never runtime records. |
| Deployment | Cloud Run scale-to-zero plus object/static hosting | Occasional authoring compute, private downloads and durable PWA assets. |

Do not add `webview_flutter`, `sqflite` or a native tool-storage bridge to satisfy this architecture. Pin compatible SDK/package versions during scaffolding. Verify launch behavior because a plugin can support multiple modes; select external launch explicitly. [url_launcher](https://pub.dev/packages/url_launcher)

## 4. Flutter text, voice and delivery flow

1. Present a prompt field, microphone control, language choice and concise supported-capability examples.
2. Capture speech only after an explicit user action and the required OS permission. Start/stop and cancellation must be visible; do not record continuously in the background.
3. Prefer on-device recognition when the OS and selected language support it. Do not silently claim all recognition is local: some native recognizers use a remote service. Disclose the recognition mode and offer text input if on-device speech is required but unavailable.
4. Show the transcript in the same editable prompt field. Submit only when the user presses Generate; recognition ending must not automatically spend an AI credit.
5. Send the normalized text to Go. The first version has no audio-upload/transcription API and retains no raw recordings. Supporting voice here does not grant microphone access to generated tools.
6. Show progress and recover the operation after app backgrounding. Display clarification questions or unsupported-capability explanations as native text.
7. When ready, show the title, capability summary, size, revision and download action. This is metadata, not a rendered HTML preview.
8. Download the finished bytes from Go, enforce size/type checks, verify the advertised SHA-256 and hand them to the OS save/share flow. Use a sanitized `.html` filename. Report completion only when the OS outcome supports it; a dismissed picker is not a saved file.
9. For mobile installation, open the published HTTPS URL externally and show the matching manual guide. Offer Copy link and a browser selector if the default browser’s flow is unsupported.

Android exposes recognition availability and on-device recognition APIs; Apple exposes on-device recognition requirements. Availability is a device/language capability, not an assumption Flutter can make globally. Native speech permissions and network behavior need device tests. [Android SpeechRecognizer](https://developer.android.com/reference/android/speech/SpeechRecognizer), [Apple on-device recognition](https://developer.apple.com/documentation/speech/sfspeechrecognitionrequest/requiresondevicerecognition)

Keep existing keyboard dictation usable as an additional route. A later cloud-transcription option would need an explicit audio endpoint, duration/size limits, separate cost reservations, disclosure and retention policy. It is not included in current generation prices.

Saving a file and executing it are separate OS actions. iOS Files previews and Android content/file handlers are not guaranteed to execute arbitrary HTML identically. Do not use a Flutter preview to hide an unsupported opening flow. Recommend the HTTPS companion for dependable mobile access, and mark portable-file support per tested browser/OS combination.

## 5. Backend compilation and capability contract

Use the supplied logger, checklist and calculator schema as the internal model-output contract. A supported request becomes a compact definition; Go—not Dart—performs the authoritative checks and emits the completed HTML.

```text
authenticate -> strict request validation -> reserve budget and claim operation
 -> assemble AI instructions -> provider call -> schema + semantic validation
 -> at most one bounded repair -> deterministic HTML compilation
 -> artifact checks -> durable artifact/result write -> return ready metadata
```

The decision outcomes are:

- `ready`: validated supported specification and a complete downloadable artifact.
- `needs_clarification`: the essential behavior needs a user choice; no artifact yet.
- `unsupported`: an essential capability cannot be delivered; explain it and a feasible alternative without pretending it was built.

Server checks include unique IDs, permitted field types, reference integrity, postfix stack correctness, bounded numeric programs, output sizes and edit compatibility. Go applies authorized logo, watermark and ad settings after model validation; prompts cannot grant paid features. See section 16 for the entitlement and quota contract. A schema-valid answer can still misunderstand the task; evaluate semantic success with realistic cases.

Go embeds a prebuilt renderer, CSS and capability-specific code. Inline all required dependencies and use system fonts. Use context-safe JSON serialization, render user strings as text, and prevent script-closing sequences from escaping the embedded definition. Do not accept scripts, CSS, URLs, HTML snippets or `eval` expressions from the model. Installation metadata, IDs, CSP and the worker are service-owned resources, not model output.

A provisional basic artifact budget is 1 MiB before user records. Make it configurable and benchmark both transfer and offline behavior. Static image templates can provide previews without a screenshot browser per generation. No preview is required inside Flutter.

## 6. Generated runtime, storage and revisions

Implement the runtime once with two delivery adapters:

- **Portable:** local working state and explicit JSON backup/restore, CSV and optional portable HTML snapshots. The downloaded file cannot silently overwrite itself. Any tested file-URL autosave is a convenience, not the data-retention promise.
- **PWA:** IndexedDB autosave in the external browser/home-screen app plus the same explicit backup/restore. A transactional commit must succeed before “Saved on this device” appears. Handle denied storage, quota and interrupted writes without silently discarding input.

Local-file storage behavior varies across browsers, and browser persistence can still be lost. Separate exported backup files are essential. Do not claim installing to the home screen prevents eviction or survives device loss. [File storage limitations](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage), [WebKit storage policy](https://webkit.org/blog/14403/updates-to-storage-policy/)

Each artifact contains an inert source envelope: app ID, revision, spec/runtime versions and validated definition, excluding records. Provide **Export tool definition** within the generated runtime for later edits. Flutter can submit an explicitly selected definition as data without rendering it. A backup containing records is not an edit source and must not be uploaded to the model.

Go owns app IDs and authorized revision history. For an edit, verify ownership, the expected base revision and the previously issued source digest using durable control metadata; validate the submitted source as untrusted data. A shared definition can create a new tool with a new identity. Do not let its recipient overwrite another creator’s published app. If ownership/history cannot be verified, offer a new copy instead of silently replacing an existing publication.

Allow compatible changes initially: labels, themes, supported formulas and new optional fields with stable IDs. Preserve existing fields’ types/meaning and required flags. Stage local data migrations transactionally before switching runtime versions. Changing a display unit is not data conversion. Destructive changes require backup and an explicit migration and are outside automatic MVP editing.

A replacement downloaded file has no automatic access to the previous file’s state: export records, open the new artifact and import the backup. Updating a hosted PWA can retain the origin and app identity, but still needs a schema-compatible migration. Browser-to-home-screen installation and opening in another browser may use different storage contexts; prefer installation before entering important records and keep manual export/import available.

## 7. Proposed public API and artifact response

The existing AI example requests describe the old adapter shape; the public delivery contract below is the revised target. Go adapts it to the existing internal model task. Flutter is not responsible for compiling or validating a tool runtime.

| Method / route | Purpose |
| --- | --- |
| `GET /healthz` | Minimal health response; no AI call. |
| `GET /v1/capabilities` | Cacheable authoring capability summary and supported contract versions. |
| `POST /v1/generations` | Create/edit from a text prompt, including reviewed speech transcripts. |
| `GET /v1/generations/{operation_id}` | Recover status or completed artifact metadata for the same principal. |
| `GET /v1/artifacts/{artifact_id}/html` | Authenticated download of the completed self-contained HTML bytes. |
| `POST /v1/publications` | Explicitly publish a blank static PWA companion from an owned validated artifact; no arbitrary HTML uploads. |

Example create request:

```json
{
  "operation": "create",
  "prompt": "Make a reading log with book title, pages and date.",
  "locale": "en",
  "source_bundle": null
}
```

For edit, `source_bundle` carries the previously exported app ID, base revision, versions and definition. It contains no records or executable code. Require exactly the versioned request keys. The backend chooses a compatible renderer version and checks the issued revision digest; a client cannot override the runtime, prompt files or permissions.

Use `Authorization: Bearer <individual token>`, a fresh `Idempotency-Key` for a new logical operation, and `Content-Type: application/json`. A repeated key with identical content recovers the result; changing the content under that key is a conflict.

Illustrative successful response; IDs and digest are placeholders, not deployed resources:

```json
{
  "operation_id": "operation-id",
  "state": "completed",
  "result": {
    "status": "ready",
    "message": "Your reading log is ready to download.",
    "questions": [],
    "artifact": {
      "artifact_id": "artifact-id",
      "app_id": "app-id",
      "revision": 1,
      "filename": "reading-log.html",
      "mime_type": "text/html",
      "size_bytes": 98304,
      "sha256": "<64 lowercase hexadecimal characters>",
      "download_path": "/v1/artifacts/artifact-id/html",
      "expires_at": "<server UTC timestamp>"
    }
  }
}
```

`ready` means the artifact exists and passed build checks, not merely that Gemini returned JSON. Persist the artifact before marking the operation completed. Clarification/unsupported responses set `artifact: null`; do not hand partial HTML to the customer.

The download response carries actual HTML bytes with `Content-Type: text/html; charset=utf-8`, `Content-Disposition: attachment; filename="reading-log.html"`, `X-Content-Type-Options: nosniff` and `Cache-Control: private, no-store`. Flutter checks length and digest after a complete download; the digest detects corruption, while HTTPS and authentication protect origin/ownership. Do not expose private artifacts as inline pages on the authoring origin. Allow only configured backend/download origins; never forward credentials through arbitrary redirects or provider-supplied URLs.

| HTTP | Meaning |
| --- | --- |
| 200 | Completed interpretation/status or complete HTML download, with route-appropriate content type. |
| 202 | Operation in progress; bounded Retry-After. |
| 400 / 413 | Invalid or oversized request; no provider call. |
| 401 / 403 | Missing/invalid token, disallowed owner or a paid feature not included in the verified plan. |
| 404 | Missing, expired or unowned operation/artifact. |
| 409 | Idempotency conflict or stale edit/publication revision. |
| 422 | Unsupported contract version or provider-blocked request. |
| 429 | Customer quota, rate, concurrency or per-operation budget admission denied; distinguish these with typed errors. |
| 502 / 503 / 504 | Invalid provider output, unavailable service, build failure or deadline exceeded, with a typed retryable error. |

Use synchronous generation initially and recover status after a dropped connection. If jobs are later queued, implement durable scheduling before returning an asynchronous promise; detached goroutines on a request-billed container are not a reliable job queue.

## 8. AI provider, instructions and cost controls

Retain paid Gemini `gemini-2.5-flash-lite` as the first benchmark candidate. The current config records USD 0.10 per million input text tokens and USD 0.40 per million output tokens, checked on 2026-09-10. A 4,000-input/2,000-output call is USD 0.0012 before repair, transcription or infrastructure. This is arithmetic, not measured cost per accepted tool or proof of the cheapest quality-adjusted provider. Recheck lifecycle and prices before deployment. [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), [Model lifecycle](https://ai.google.dev/gemini-api/docs/deprecations)

Keep `gemini-3.1-flash-lite` a disabled evaluation fallback; model promotion needs the same behavioral tests and its own generation parameters. The delivery correction does not require changing the model-output schema to raw HTML.

Go reads Markdown/config contents and sends them to the provider; the API does not fetch local filenames. Embed versioned assets with `go:embed`:

1. System and operation instructions plus the serialized capability manifest in `systemInstruction`.
2. Prompt, locale and validated current definition for edits as separate untrusted task data.
3. The provider-compatible response schema and server-owned model settings.
4. On a permitted repair, the candidate and bounded validation errors as task data.

Use `x-goog-api-key` from backend secret storage. Do not put secrets, tester tokens or prompt history inside generated HTML. No tools, grounding, retrieval database, automatic runtime AI or provider-side conversation store is needed. The existing offline request assembler remains useful for inspecting internal provider payloads. [generateContent REST contract](https://ai.google.dev/api/generate-content)

Initial admission limits remain: at most two inference attempts total including transport retries and repair; at most one repair; 6,000 output tokens; 24,000 total input tokens per attempt; 35-second attempt and 80-second operation deadlines; USD 0.02 maximum estimated operation reservation. Count complete instructions/schema/context, not just the user prompt. Treat unknown timeout outcomes as potentially billed; do not retry indefinitely or record them as free.

Use a transaction to claim the operation and reserve principal/global budgets before calling Gemini. Store keyed request fingerprints, lease ownership, attempts, usage and completion. Reject stale lease writes. Use integer microdollars and conservative missing-usage accounting. A local idempotency key cannot guarantee exactly-once billing by an external provider. Cloud billing alerts do not replace admission controls.

## 9. Private downloads versus durable PWA hosting

Private generation and public hosting are separate user choices. Default to a private artifact download. Offer installation through an HTTPS companion after explaining that a static, anonymously fetchable definition can be read by anyone with its URL. An unlisted URL and `noindex` are not authentication. Never publish record snapshots, private example records or raw prompt text as metadata.

A user who needs a confidential tool definition can keep the downloaded file or use their own suitable host. Authenticated PWA hosting would require a separate design for identity, installation assets, offline access and sharing. Do not slip that ongoing account service into a “metadata-only server” claim.

Use separate retention rules:

- Private completed HTML/specification results: an explicit short retention, initially 24 hours, application-level expiry plus storage lifecycle cleanup. Tell the user to save the file. Expiration does not delete a previously saved user-owned file.
- Minimal credential, idempotency and revision-control metadata: retain according to the account/operation policy; never confuse these with tool records.
- Published PWA assets: retain stable URLs under a disclosed hosting policy; no ten-minute or 24-hour automatic deletion tied to generation results. Cached apps may fail after eviction if their host has disappeared.

Illustrative static layout, separate from the API/account origin:

```text
https://tools.example.invalid/a/<app-id>/index.html
https://tools.example.invalid/a/<app-id>/manifest.webmanifest
https://tools.example.invalid/a/<app-id>/sw.js
https://tools.example.invalid/a/<app-id>/icons/icon-192.png
https://tools.example.invalid/a/<app-id>/icons/icon-512.png
https://tools.example.invalid/a/<app-id>/icons/apple-touch-icon.png
https://share.example.invalid/<app-id>/index.html
```

A manifest has a stable, per-tool `id`, `name`, `short_name`, `start_url`, `scope`, `display: standalone`, icons and theme colors. Use distinct IDs/start URLs so installing one tool does not replace another. Scope the worker to `/a/<app-id>/` and avoid a root worker. The download build has no worker dependency; the hosted build adds the manifest and trusted registration bootstrap while embedding the same core logic.

The PWA is several separately fetched resources even if its tool code is one HTML. Generating those resources from one source template or responding to several routes does not make it a universal single-file artifact. Prefer static publication over a dynamic Go response on every app launch.

Stage immutable revision assets and a complete cache inventory before exposing a new release. Keep the manifest identity stable. Serve `sw.js` with a JavaScript MIME type and update-friendly cache headers; do not mark it immutable forever. The worker verifies required resources, caches a complete version and controls the page before showing offline readiness. Installation remains a separate browser/OS event. Handle interrupted preparation and never force activation midway through a form save.

Ordinary app input/calculation/save/export must not invoke the authoring API. Initial fetches and browser update checks can contact static hosting. No remote fonts, tracking analytics, runtime record synchronization or hidden API calls in generated tools. Free outputs may contain the bundled static sponsor panel described in section 16; it makes no background ad requests. Flutter advertising is a separate authoring-client dataflow. Page CSP and worker response CSP need separate policies: the trusted worker may fetch its static inventory while the page has no arbitrary network destinations.

Generate title, description, canonical URL, Open Graph tags and a static preview image at publication time. Metadata is in the initial HTML; no per-visit render function is necessary. Keep metadata optional for unlisted tools and escape all text. [Open Graph protocol](https://ogp.me/)

## 10. Phone installation guide to ship with Flutter

Instructions apply to the **hosted HTTPS companion**, never to a `file:`, `content:`, `blob:` download, a Flutter WebView or an in-app social browser. Ask the user to choose their actual browser/OS; detection is a convenience, not the authority. Keep versioned guides in `client/assets/install-guides/` and include manual instructions in the hosted page too.

| Phone/browser | Guide action | Qualification and fallback |
| --- | --- | --- |
| iPhone/iPad Safari | Open the URL; Share (sometimes under More) → Add to Home Screen → enable Open as Web App where offered → Add. | Primary iOS fallback. Return to the home-screen icon and complete/verify offline preparation. [Apple guide](https://support.apple.com/guide/iphone/open-as-web-app-iphea86e5236/ios) |
| iPhone/iPad Chrome | Share beside the address bar → Add to Home Screen → Add. | Use the option if offered; otherwise open the same link in Safari. [Google guide](https://support.google.com/chrome/answer/9658361?co=GENIE.Platform%3DiOS&hl=en) |
| iPhone/iPad Firefox | Share → Add to Home Screen → Add. | Mozilla describes a shortcut flow; test the resulting standalone/offline behavior for this PWA. [Mozilla guide](https://support.mozilla.org/en-US/kb/add-website-shortcut-your-home-screen-ios) |
| iPhone/iPad Edge | Share → Add to Home Screen when offered. | Exact current Edge screenshots need device verification; Safari is the fallback. |
| Android Chrome | More → Install and create shortcut → Install, then confirm. Some versions use Add to home screen → Install. | Menu/OS flow may vary. Full WebAPK integration depends on device services. [Google guide](https://support.google.com/chrome/answer/9658361?co=GENIE.Platform%3DAndroid&hl=en) |
| Android Firefox | Menu → Install → Add automatically, or position the icon. | Do not promise the same OS integration as Chrome. [Mozilla guide](https://support.mozilla.org/en-US/kb/use-web-apps-firefox-android) |
| Android Edge | Menu → Add to Phone when available, then follow device confirmation. | Microsoft documents this menu entry; verify the current consumer UI and offline launch on the target device. [Microsoft documentation](https://learn.microsoft.com/en-us/intune/app-management/configuration/configure-edge-ios-android) |
| Android Samsung Internet / Samsung Browser | Use the browser’s offered install/home-screen action. | Samsung’s official illustrated guide is old; do not ship its exact screenshots as current. Capture a verified modern flow; offer Chrome when it is unavailable. [Samsung guide](https://samsunginternet.github.io/docs/homescreen) |
| Other/unsupported browser or an embedded browser | Copy/open the HTTPS link in a supported full browser. | Explain when only a bookmark or ordinary browser shortcut is available. Never claim every browser provides identical installation. |

On iOS/iPadOS before 16.4, guide through Safari. From 16.4, third-party browsers can provide the system home-screen flow. Page JavaScript cannot force installation; keep manual guidance when `beforeinstallprompt` is absent, notably on iOS. [WebKit browser support](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)

Document home-screen launch, offline readiness and browser storage as separate checks. A visible icon or an `appinstalled` event alone is insufficient evidence of a cached, recoverable app. Device testing must distinguish a WebAPK from a browser-managed home-screen shortcut; support levels should describe the behavior actually verified.

Launch the newly installed app while still online and verify offline preparation there before instructing the user to test airplane mode. On iPhone, existing Safari local records do not automatically transfer to the home-screen app: WebKit documents cookie copying at installation, but no copying of other local storage or ongoing sharing of website data. Prefer entering records after installation, or guide explicit export/import from the browser. Include this boundary in the real-device acceptance scenario. [WebKit storage separation](https://webkit.org/blog/14787/webkit-features-in-safari-17-2/).

For desktop, provide separate tested guides later. Do not extend the phone matrix into a promise of installation on every operating system/browser.

## 11. Privacy, isolation and native distribution

The execution boundary is architectural: Flutter does not execute generated HTML; artifacts contain no Flutter bridge, app credentials or link back to an account session. PWA execution uses a different origin from the authoring/account surface. Browser/OS launch is a handoff, not a rendering component inside Flutter.

A shared static origin is acceptable for the initial trusted, declarative runtime only with explicit app namespaces and strict runtime validation. Different URL paths and IndexedDB names are not browser-enforced isolation from hostile code. Introducing arbitrary HTML/JavaScript would require separate origins and a broader security design; it is outside this roadmap. [Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy)

Use CSP, text-only rendering, approved scripts, no external navigations from specs and restricted permission policies. Test network behavior, malicious imports and cross-tool namespace attempts. Protect the backend compilation context from markup injection even though Flutter does not run the output. Treat privately exported JSON/HTML as sensitive unencrypted files unless an explicit encryption feature exists.

The local-only promise covers generated-tool records and daily computation. Prompts leave the phone during generation; speech recognition may have its own provider path; static hosts see file requests. Free Flutter advertising may contact its declared ad provider, without receiving prompts, generated definitions or tool records. This does not enable ad-network calls inside the generated tool. No raw prompts/audio or provider response bodies in ordinary logs. Generated tools do not inherit the Flutter app’s microphone permission.

The previous WebView/native-bridge store-review concern no longer describes this design. Still review the actual authoring/download app, microphone privacy and any generation-credit billing under current store requirements. Browser handoff is not a blanket exemption from app review or payment rules. Do not restore an embedded runtime as an installation workaround. [Apple review guidelines](https://developer.apple.com/app-store/review/guidelines/)

## 12. Repository and configuration migration

This update changes BLUEPRINT.md and ROADMAP.md. Existing prompts/configuration/examples are implementation inputs that need the following alignment before scaffolding; their old client-execution wording is superseded by these documents.

| Existing asset | Required alignment |
| --- | --- |
| `config/flutter.example.json` | Replace execution/bridge flags with public API, speech policy, download size and external-install-guide settings; add public store product mappings and an ad-placement enable flag. Go supplies authoritative entitlement/quota state; local flags cannot unlock paid output. Runtime versions belong to artifact/service compatibility, not a Flutter renderer. |
| `config/backend.example.yaml` | Add compiler/assets, private artifact storage/expiry, purchase verification, quota transactions and publication limits. Separate generation-result TTL from hosted-PWA retention. Its current 20-operations/day and USD 0.25/principal/day are prototype controls, not Premium terms; replace them with a budget policy that can honor 100 requests/month without an undisclosed daily allowance. |
| Proposed `config/plans.yaml` | Implement the versioned Free/Premium matrix and quota periods in section 16. Prices remain unset until the commercial decision; production must reject missing product/price mappings. No file or loader is created by this documentation change. |
| Proposed `config/hosting-plans.yaml` | V2 only: active-app, byte, traffic, version, domain and retention limits with public terms. Reject an enabled paid hosting offer with undefined limits. |
| `config/ai.json` | Retain provider/schema/attempt controls; version prompt changes and record benchmarked prices. No HTML-output override is needed. |
| `ai/README.md` | Move authoritative spec/build validation and revision commits to Go; explain actual HTML download delivery. Remove the native client installation/activation wording. |
| `ai/prompts/system.md`, `edit.md` | Clarify “host” means Go/compiler for identity and edits; generated records stay in an external browser/file runtime. No activation inside Flutter. |
| `ai/capabilities.json` | Specify portable explicit saves versus PWA autosave. Microphone exclusion refers to generated tools, not voice authoring. |
| `ai/schemas/generation.schema.json`, ready examples | Reuse as the internal AI contract; do not mistake these JSON examples for the client’s HTML artifact response. |
| Client request examples / `scripts/build_ai_request.py` | Separate the new public request envelope from internal provider-task assembly; preserve the no-network offline helper. Add artifact/clarification/unsupported fixtures. |

Proposed implementation layout:

```text
client/
  lib/features/{authoring,voice,results,downloads,install_help,plans,purchases,ads}/
  lib/core/{api,credentials,platform_files,external_browser}/
  assets/install-guides/
  test/
  integration_test/
backend/
  cmd/api/
  internal/{httpapi,auth,ai,validation,compiler,artifacts,budget,idempotency,publish}/
  internal/{billing,entitlements,quota,branding,hosting}/
  internal/controlstore/{sqlite,firestore}/
  internal/assets/              # go:embed: prompts, schema, trusted compiled runtime
runtime/
  src/{renderer,expressions,adapters}/
  templates/{portable.html,pwa.html,sw.js,manifest.webmanifest}/
  tests/
contracts/
  fixtures/                    # Go validation, browser-runtime and API conformance
```

There is no client runner, native record database, bridge module or client-bundled HTML renderer. Flutter storage supports authoring UI and temporary downloads only. Do not treat an app-cache file as the delivered independent copy.

## 13. Minimal-cost deployment

Develop Go locally with a persistent local control database. For a hosted beta, retain Cloud Run with minimum instances zero, request-based billing, initial maximum instances one and modest concurrency. Use Firestore for durable operation/budget/revision metadata and object storage for completed artifacts. The container filesystem is not durable storage.

With the current 80-second generation ceiling, configure request and client timeouts with a bounded margin; include compile/delivery overhead before declaring a hard latency target. Start with small compilation in Go, not a headless browser per request. Run heavier artifact behavior tests in CI or a bounded validation job where warranted.

Cloud Run can scale to zero, but request duration, builds, image storage, logs, control records, storage, secrets and egress still have costs. Keep creation and optional transcription metered. Limit artifact size, attempts, trial quotas and retained versions. [Cloud Run autoscaling](https://cloud.google.com/run/docs/about-instance-autoscaling)

Serve PWA assets directly from a static host/CDN, not through the Go generation process. One app does not require one server, container or database. Metadata is built once. Static storage/bandwidth still exist even though no server processes records during tool use. Choose a host supporting HTTPS, required MIME types, per-path headers and realistic artifact-count limits.

This is minimal ongoing server responsibility, not “server only renders metatags”: online AI authoring, secure delivery and PWA asset distribution are additional necessary jobs. If the founder permits no hosted app assets at all, ship portable downloads and explicitly drop the universal mobile-installation promise.

## 14. Phases and release gates

| Phase | Deliverables | Exit criterion |
| --- | --- | --- |
| 0. Correct boundaries and prove device delivery | Migrate the request/config assets above; scaffold thin Flutter/Go; manually build one independent logger. | A tap saves HTML via OS UI; Flutter never renders it. Record actual file-opening and external-browser flows on Android/iPhone. |
| 1. Trusted HTML compiler/runtime | Go compilation, logger/checklist/calculator, portable saving, source export, backup/restore. | Fixture-built HTML runs outside Flutter with networking disabled; file-mode recovery is proven. |
| 2. Static PWA companion | Per-tool manifest/worker/icons, stable HTTPS identity, IndexedDB, atomic offline preparation and manual install guides. | Real-device home-screen launch and offline restart work; incomplete caching never claims ready; browser matrix has support labels. |
| 3. Authoring and delivery API | Provider adapter, strict validation, bounded repair, individual tokens, durable budgets/idempotency, private artifact endpoint. | Duplicate and failed requests do not cause uncontrolled spending; ready results have downloadable verified HTML. |
| 4. Text and voice UI | Native speech/transcript review, clarification/status recovery, download/save and explicit hosted publication handoff. | Users create by text or supported speech and save without a WebView; denied mic/storage permission has a working recovery path. |
| 5. Live evaluation | Expand the twelve seed scenarios to representative prompts; measure interpretation, accepted artifacts, retries, latency and total cost. | Pass declared thresholds on actual model results and behavior; no unsupported feature silently advertised. |
| 6. Monetized v1 beta | Verified purchases/restore, Free/Premium quota, custom logo pipeline, watermark/ad flags, Flutter ads and offline sponsor panels; browser install help and revision/backup recovery. | All five v1 feature entitlements and quota boundaries pass; receipts cannot be forged, local use survives cancellation, and users understand download versus install. |
| V2. Hosting products | Managed capacity add-ons, custom-domain option and self-host package export, with metering and lifecycle terms. | Domain ownership/TLS, quotas, downgrade/export and origin migration tested; prices and limits visible before sale. |

Provisional evaluation targets: at least 90% of supported cases usable without repair and 97% after the one allowed repair, mean generation cost below USD 0.01 per accepted artifact, and p95 end-to-end authoring under 30 seconds. These are targets, not measurements; capture compilation and delivery separately from inference. Broaden beyond the seed fixtures to Turkish/English, ambiguous voice transcripts, unsupported requests, malicious labels, destructive edits and formula edge cases.

## 15. Verification and first implementation task

| Layer | Meaningful verification |
| --- | --- |
| Go/schema/compiler | Reject unknown fields, duplicate IDs, invalid formulas and incompatible edits; safely embed hostile text; compare deterministic bytes for identical complete build inputs, including source/version, authorized branding/ad settings and logo assets. |
| AI/spending | Mock refusal, truncation, timeout and invalid JSON; enforce shared attempt limits and concurrent budget admission; retain money reservations on unknown outcomes, with customer-query credit reconciliation handled separately. |
| Delivery | Authenticate artifacts by principal; expire only private results; verify hash/length, interrupted download, picker cancellation and a saved file outside Flutter’s disposable cache. |
| Flutter boundary | No generated HTML preview, WebView, bridge or native record store; external-browser mode verified; uninstall leaves the independently saved artifact and external PWA usable. |
| Voice | Permission denial, unsupported language, unavailable on-device recognizer, recognition error/cancel, editable transcript and no automatic generation charge on speech completion. |
| Portable runtime | Offline calculations, explicit export/import, relocated/renamed file recovery, safe malformed import rejection and honest unsaved-state warnings. |
| PWA lifecycle | Distinct tool IDs, same-tool update identity, per-tool worker scope, partial cache failure, airplane-mode restart, quota failures and manual recovery after site-data deletion. |
| Record migration | Stable field identity; transactional additive migration; portable-file transfer and browser/home-screen storage differences; no silent history conversion. |
| Privacy / ads | Normal record operations and bundled sponsor display produce no ad/data requests; distinguish static updates from Flutter ad-provider traffic; paid artifacts have no ad code or assets. Sponsor links are explicit user navigation without records, prompt parameters or referrers. |
| Monetization | Free weekly and Premium monthly boundaries; concurrent last-credit requests; idempotency replay; cancellation before/after dispatch; failure refunds; restore and plan switches without allowance duplication; forged/out-of-order purchase events; unchanged source rebranding without an AI debit. |
| V2 hosting | Active-slot, size/version and traffic admission; verified domain ownership; changed-origin backup/import; downgrade grace and export before retention expiry. |
| Platform/browser | Actual listed browsers on supported OS versions, home-screen versus tab mode, safe-area/keyboard/accessibility, guide screenshots and version dates. |

After scaffolding, CI runs Go tests, Flutter analysis/unit tests, runtime tests and shared fixtures. Live AI evaluation is a separate opt-in job with a hard budget. Physical mobile installation and file-handler behavior require device checks; desktop emulation alone is insufficient.

**First implementation task:** compile `ai/examples/ready-logger.json` into a genuinely independent `reading-log.html` with Go, serve it from a private download endpoint and save it using a thin Flutter result screen. Prove its explicit export/restore in a compatible external browser. Then publish the same definition as a minimal static PWA and verify phone installation. Connect AI only after those output and delivery paths work.


## 16. Monetization: v1 plan, billing and artifact behavior

### Plan matrix

These options reflect the requested monetization model. Bundling them in one Premium subscription is the proposed launch packaging; currency, price, trial and any future separate branding/ad-removal add-ons remain commercial decisions. No subscription prices or expected ad income are invented here.

| Feature | Free | Premium |
| --- | --- | --- |
| AI creation / AI edit requests | 3 per calendar week | No weekly cap; 100 per monthly entitlement period |
| PWA app logo | Standard herepp icon | Upload a custom logo for the generated tool and installation icons |
| herepp watermark | Visible attribution in generated HTML/PWA | Omit herepp watermark from authorized builds |
| Flutter ads | Eligible online placements | No Flutter ads while entitlement is active |
| Generated HTML / PWA ads | Bundled, clearly labelled sponsor/promo panel | Panel, ad code and ad assets omitted from authorized builds |
| Existing tools, local records and backup/export | Unlimited local use | Unlimited local use |
| Hosting product upgrades | Basic included companion only under disclosed limits, if offered | Separate v2 hosting options; Premium does not imply unlimited storage/traffic |

The requested “limitless” upgrade means lifting the weekly restriction, with an actual cap of 100 AI requests/month. Use **“Premium — no weekly cap, 100 AI requests/month”** on the plan card, paywall and usage screen. “Unlimited use of your existing tools” is accurate; unqualified unlimited generation is not. The cap must be visible before purchase, not only in expandable details. Google’s subscription guidance requires material terms to be available without extra user action. [Google subscription terms](https://support.google.com/googleplay/android-developer/answer/9900533?hl=en)

### What counts as a request

The unit is a **user-submitted AI query**, not a guarantee that an app is produced. Show this beside the quota meter and Generate/Edit button.

| Event | Customer quota effect |
| --- | --- |
| Text submission or reviewed voice transcript sent for AI create/edit | Reserve one request before provider dispatch. |
| Completed `ready`, `needs_clarification` or model `unsupported` result | Consume that one request: an AI query was answered, even if no app was produced. |
| User answers clarification questions and explicitly submits again | New query; one request. Bundle answers into one submission where possible. |
| Automatic repair or transport retry within the same operation | No additional customer request; still subject to the existing two-inference-attempt ceiling and money budget. |
| Local/preflight rejection, denied entitlement, exhausted quota, cancellation before dispatch | No debit; release any reservation. |
| Terminal service/provider/build failure with no completed usable interpretation or artifact | Restore the customer request once; retain any real/unknown provider cost in the separate money ledger. |
| User closes Flutter or cancels after provider dispatch | Recover the original operation; a completed interpretation still counts. Do not create a free retry under a new operation automatically. |
| Download/redownload, ordinary use, backup/import, static publication | No AI query debit; artifact/hosting availability limits still apply. |
| Logo/watermark/ad setting change using the same validated definition | Deterministic rebuild; no AI query debit. |

Count product requests and provider spending separately. Rate-limit unsupported prompts, clarification loops and repeated terminal failures even when customer credits are restored. Refund quota to the original operation’s bucket, not into a newer period. A retried download or replayed completion must never debit again.

### Quota periods and transaction model

- Free: 3 requests per calendar week, Monday 00:00 UTC to the next Monday 00:00 UTC; use half-open intervals. Return the exact reset timestamp and render it in the user’s timezone. No rollover.
- Premium: 100 requests per monthly service period anchored to verified subscription activation/renewal boundaries. Premium replaces Free while active; it does not add 3/week. No rollover. If annual billing is added, allocate 100 in each anchored monthly subperiod, not once per annual renewal; handle end-of-month and leap-year boundaries consistently.
- Upgrade: issue the paid bucket only after verified entitlement, once for its unique period. Restoring purchases or signing in on another device recovers the same bucket. Cancellation remains Premium through its paid-through date unless the provider reports earlier revocation/refund.
- Expiry/downgrade: future queries use the current Free bucket, preserving any consumption already recorded there. Subscription toggling cannot manufacture fresh weekly/monthly allowances or refund already delivered queries.
- Quota is shared across devices by a durable authoring principal. Individually issued beta tokens are sufficient only for the invite prototype; production needs stable account identity and recovery. Generated tools still require no login.

Resolve an existing `(principal_id, idempotency_key)` first: reject a changed request fingerprint, otherwise return the existing operation/result without another quota check or debit, even if the current allowance is exhausted. For a new operation, one control-store transaction resolves verified plan state, selects `(principal_id, quota_period_id)`, checks `used + reserved < allowance`, claims the operation and reserves both one customer request and the conservative money budget. Handle a concurrent claim of the same key through the same replay path. Persist the bucket ID and entitlement snapshot on the operation. On completion atomically convert its reservation to used, or release once on an eligible failure. Period rollover, cancellation and webhook races must not move the operation to a different bucket.

Keep grant/debit records and operation fingerprints through their quota period and the defined billing-reconciliation retention. The private artifact's 24-hour expiry must not erase allowance usage or permit a duplicate debit/grant. A replay referencing an expired artifact reports that expiry; it does not silently regenerate it or charge another request.

Quota exhaustion returns HTTP 429 with a typed `quota_exhausted` error before inference, including allowance, used/reserved, reset timestamp and upgrade eligibility. Temporary rate limiting returns HTTP 429 `rate_limited` plus Retry-After; a service-wide spending stop returns HTTP 503 `service_budget_unavailable` without consuming customer allowance. Do not present all three as “you used your plan.” A paid allowance is not a guarantee of unlimited concurrency, but time-based usage caps must not be hidden behind prototype budgets.

The existing backend example’s 20/day and USD 0.25/day per-user settings do not implement this plan. Replace them before paid release; keep short burst throttles and absolute per-operation ceilings, and size service funds to deliver purchased allowances. Define operator incident handling for a global budget stop; it is not an extra normal Premium quota.

Proposed configuration contract, documentation only:

```yaml
config_version: 1
plans:
  free:
    requests: {allowance: 3, period: calendar_week, week_start: monday, timezone: UTC, rollover: false}
    custom_logo: false
    remove_watermark: false
    flutter_ad_free: false
    artifact_ad_free: false
  premium:
    requests: {allowance: 100, period: subscription_month, rollover: false}
    custom_logo: true
    remove_watermark: true
    flutter_ad_free: true
    artifact_ad_free: true
artifact_ads:
  free_mode: embedded_static_sponsor
  premium_mode: none
  network_ads_enabled: false
hosting:
  paid_options_version: v2
  paid_options_enabled: false
```

### Purchase and entitlement service

Use the appropriate store purchase flow for digital features sold in the native app and validate the chosen market’s distribution/billing rules before launch. Go verifies purchase evidence with the store; a Flutter boolean, screenshot or decoded unsigned receipt cannot grant Premium. Restore purchases must work without purchasing again. [Google backend billing guidance](https://developer.android.com/google/play/billing/backend), [Apple app review requirements](https://developer.apple.com/app-store/review/guidelines/)

Add these authenticated service routes alongside the authoring API:

| Route | Contract |
| --- | --- |
| `GET /v1/me/entitlements` | Plan, paid-through state, effective feature flags, quota allowance/used/reserved and reset time; no card data. |
| `POST /v1/billing/verify` | Submit store/product purchase evidence for server verification and binding to the authenticated principal. |
| `POST /v1/billing/restore` | Reconcile verified existing transactions; do not reset allowance or duplicate grants. |
| Store notification endpoint(s) | Verify provider authenticity, deduplicate and reconcile renewals, cancellation, refund, expiration and revocation. |
| `POST /v1/branding/assets` | Paid custom-logo upload with bounded decoding/validation; return an owned asset ID. |
| `POST /v1/artifacts/{id}/rebuild` | Recompile an owned unchanged definition with currently authorized branding/ad settings; no AI call. |

Bind each store transaction/subscription chain to one principal; prevent replay into a second account. Separate sandbox and production. Handle pending purchases without granting paid access. Notifications can arrive late or out of order: reconcile authoritative store status, retain event identifiers and apply monotonic/idempotent changes, rather than assuming arrival order is billing order. Never store full payment-card details. [Google notifications](https://developer.android.com/google/play/billing/rtdn-reference), [Apple notifications](https://developer.apple.com/documentation/appstoreservernotifications/)

Snapshot features at authorized build admission and store them with artifact provenance: creator, source/revision digest, runtime/compiler version, plan policy version, logo asset digest, watermark choice and ad mode. This is build authorization, not a runtime license server. If an expired private artifact/source is unavailable, require a valid record-free source bundle before rebuilding; upgrading cannot magically recover deleted source data.

### Custom logo and watermark

Custom logo means user-uploaded artwork in v1, not unlimited AI image generation. Validate ownership, file signatures, decoded dimensions and size; strip metadata and re-encode allowed raster formats. Do not embed untrusted SVG, HTML, remote URLs or original file metadata. Generate the manifest PNG sizes, Apple touch icon and in-tool icon from the sanitized master; an optional crop preview is a native image UI, not generated HTML rendering.

Use a standard herepp logo for Free and the authorized custom asset for Premium. Updating an icon or watermark preserves app ID, origin and data namespace. Browser launchers may retain an old icon until an update or reinstall; do not promise immediate replacement on every platform.

The watermark is a visible “Made with herepp” attribution owned by the compiler, independent of an advertising panel. Removing it must retain any required third-party library/license notices. Prompts and imported tool definitions cannot set their own paid feature flags.

### Ads and continued offline independence

For v1, free HTML and PWA builds embed a small labelled sponsor or herepp promotional panel, including its image/text. It works offline and requires no third-party JavaScript, network impression pixels or ad fetch. Direct sponsorship is a possible revenue source; house promotion itself earns no ad revenue, and neither offline views nor downloads are assumed to create billable network-ad impressions.

Allow only compiler-owned, reviewed sponsor links opened by an explicit tap in the external browser, with no record/prompt parameters and no referrer. Link destinations cannot come from model specifications. Do not intercept Save/Export actions, cover the tool’s controls or make users view an ad to recover their own records. Offline/no-fill/blocked-ad conditions must never stop the tool.

Flutter can use separately declared online ad placements for Free users. Keep its ad provider isolated from prompt text, definitions and tool records; disclose the provider’s device/network data handling and use the applicable consent controls. Do not describe a non-personalized ad setting as proof of zero data collection. Premium suppresses Flutter ad requests, initialization and display for those placements; offline/unknown entitlement state uses cached verified benefits and no ads until safely resolved.

Third-party network advertising inside a PWA is a later optional design requiring an explicit change to the no-background-ad-network contract. Never put an untrusted ad SDK in the same document/origin as private records. An isolated placement would still need a separately reviewed boundary and compatible ad-provider arrangement; it must fail harmlessly offline and never block record operations. It is not assumed implemented, approved or revenue-positive in v1.

Premium builds omit the generated-tool panel and any ad assets/code entirely. No account lookup, ad-removal ping or subscription check runs inside the generated app. The creator’s ad-free build is ad-free for everyone using that build; it is not a viewer-account entitlement.

Existing Free downloads are unchanged by upgrading. Let the owner rebuild and redownload, or deploy an authorized same-identity PWA revision; offline cached copies change only when their user accepts/receives an update. Branding rebuilds do not consume AI quota. On cancellation, Flutter benefits and eligibility for future builds follow the paid-through date; already obtained custom-logo, watermark-free and ad-free artifacts remain usable with those settings. No forced expiry screen or remote data deletion.

Downloaded HTML is editable: users can manually remove attribution or ads, and clean builds can be shared. Monetization sells convenient official generation, branding and managed services; it cannot depend on tamper-proof HTML or remote revocation without changing the independence promise.

## 17. Hosting monetization options — v2

Paid hosting products are explicitly v2. Basic shared static PWA delivery may be included in v1 under published capacity/retention limits; it is the installation mechanism, not a promise of unlimited free hosting. Set those limits before the public beta. Generation Premium and hosting entitlements are separate so an AI subscription does not create an unbounded storage/bandwidth liability.

| Option | Customer pays for / receives | Boundary |
| --- | --- | --- |
| Portable download | Existing HTML download; no recurring hosted-runtime obligation | File execution/support limits remain; no universal PWA installation promise. |
| Self-host PWA export | Export a complete static package containing HTML, manifest, worker and icons for a suitable HTTPS host | No recurring herepp hosting fee; whether packaging is included or a one-time add-on remains a pricing decision. The customer operates their host. |
| Managed herepp hosting add-on | More active hosted tools, storage/transfer capacity, version retention and managed publication on herepp’s domain | Price and exact limits TBD; no runtime records database, synchronization or backend functions included. |
| Custom-domain hosting option | Verified customer domain, TLS and managed publication/maintenance | Domain purchase/renewal and any support level must be explicitly included or excluded; not an implicit unlimited service. |

Before enabling any paid SKU, specify recurring price/currency and billing period; maximum active apps; HTML/asset upload size; total retained storage and revisions; transfer allowance and measurement window; custom-domain slots; retention/downgrade grace; and support scope. No automatic overage charges without an agreed policy. At limits, stop new publication/version growth or offer an explicit upgrade before incurring more capacity; traffic exhaustion needs a disclosed warning/serving policy that does not silently corrupt offline caches. Final limits and prices remain unchosen.

Meter hosting from authoritative stored bytes/object manifests and CDN transfer records, not file counts claimed by Flutter. Stage changes, reserve capacity, publish atomically and release replaced assets according to retained-version policy. Keep existing paid revisions available through the paid term and disclosed grace; export remains available before scheduled removal. Expiring a temporary download is never the event that removes a subscribed hosted tool.

Cancellation/downgrade must show the affected URLs, service end and grace/export dates. Prefer blocking new publishing when over the lower tier before deleting existing assets. After the disclosed retention ends, installation/recovery from hosting may cease; an existing cache or downloaded file is not remotely disabled, but cache loss can make the installed copy unrecoverable without another saved copy. Do not promise perpetual hosting or perpetual cache survival.

A custom domain changes the browser origin. Verify domain ownership and TLS before binding, reserve the domain to one authorized tenant, and prevent abandoned DNS bindings from being reassigned without proof. Keep a backup/export route on the old origin and instruct users to import into the new installation. Preserve tool identity in the source, but do not claim cross-origin browser records migrate automatically or that old home-screen icons repoint themselves. Design the self-host package for its selected base path before export so manifest and service-worker scopes remain correct.

Validate pricing against hosting/storage/egress, failed payments, domain support and maintenance costs. Measure purchase conversion and repeat generation for Premium, optional sponsor revenue separately, and contribution after store/payment fees and support. No viability-report forecast or ad revenue estimate is established by adding these options.


## 18. Final planning handoff and release status

Planning finalization closes the documentation stage only. Do not mark implementation phases complete based on the presence of prompts, schemas or fixtures.

- [x] Product boundary: Flutter authoring/delivery, Go validation/compilation, independent external HTML/PWA runtime.
- [x] Delivery and customer examples documented, including browser handoff, static assets, offline readiness and backup.
- [x] Requested Free/Premium benefits and separate v2 hosting scope documented.
- [x] Market analysis consolidated, including mobile-first differentiation, competition, renewal risks and conditional founder economics.
- [x] Historical assumptions identified and current documents cross-linked.
- [ ] Select pilot audience/geography, price, founder time/income goal and experiment budget.
- [ ] Define basic PWA capacity and retention before offering managed publication; define paid hosting terms before v2 sales.
- [ ] Complete section 12 configuration/interface migration; prototype daily limits are not the production Premium allowance.
- [ ] Implement and verify the fixture-based Go → Flutter delivery → external runtime slice in section 15.
- [ ] Prove real-device installation, offline restart, backup/restore and safe updates; publish only tested browser support.
- [ ] Connect AI and measure interpretation, correctness, latency, repairs and total cost against declared targets.
- [ ] Implement verified billing, quotas, entitlements and cancellation behavior before paid release.
- [ ] Complete the paid-pilot gates in MARKET_ANALYSIS.md, measuring phone-only task completion, purchases, support, acquisition and renewals separately.

The first technical slice remains the reading-log fixture. The first commercial audience is a separate validation decision; a manual-input estimate calculator for solo operators is a suggested hypothesis, not a required pivot. Source dates and provider/platform terms must be refreshed before launch. A finished planning package is not a production-readiness claim.
