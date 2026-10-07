# AI request kit

These files define the first provider integration and its local fixtures. They are not a running Go API or Flutter application. No live model call has been made to validate generation quality.

Current product authority: [BLUEPRINT.md](../BLUEPRINT.md) and [ROADMAP.md](../ROADMAP.md). These are internal provider fixtures, not Flutter runtime messages. Prototype configuration still requires the migration recorded in roadmap section 12.

## Files

- `../config/ai.json`: server-owned model, generation parameters, token/cost limits, and prompt paths.
- `capabilities.json`: the capabilities actually available in specification version 1.0.
- `prompts/system.md`: instructions common to all calls.
- `prompts/create.md`, `edit.md`, `repair.md`: operation-specific instructions.
- `schemas/generation.schema.json`: authoritative local output schema, also used to derive the provider schema.
- `examples/`: client task bodies and representative result objects.
- `evals/cases.jsonl`: behavioral scenarios for later live evaluation; they are not benchmark results.
- `../scripts/build_ai_request.py`: an offline utility that assembles a real generateContent request body; it makes no network calls and does not load credentials.

Paths in config files resolve from the repository root. In the Go binary, embed the prompts, schema, and manifest at build time with `go:embed`, using a generated internal assets directory. Record their SHA-256 digests with the service version. Client requests cannot override these resources.

## Selected provider

Start with the paid Google Gemini Developer API and stable `gemini-2.5-flash-lite`. The pricing page currently lists text input at $0.10 and output at $0.40 per million tokens. `gemini-3.1-flash-lite` is a disabled evaluation fallback, listed at $0.25/$1.50. Prices were checked on 2026-09-10; verify before launch. Google's lifecycle page currently lists no announced shutdown date for the chosen stable model. [Pricing](https://ai.google.dev/gemini-api/docs/pricing), [Lifecycle](https://ai.google.dev/gemini-api/docs/deprecations)

Do not use the similarly named retired `gemini-2.5-flash-lite-preview-09-2025`. This provider choice is a cost-focused starting hypothesis, not proof it is the cheapest provider at the required success rate.

## What actually goes to the API

The API does not read local Markdown files or paths. Go must read their contents and assemble:

1. `systemInstruction.parts[0].text`: system instructions, the operation instructions, and the serialized capability manifest.
2. `contents[0].parts[0].text`: JSON containing operation, prompt, locale, and current_spec for edits. This is task data, never concatenated into the instruction section.
3. `generationConfig`: primary model settings plus `responseMimeType: application/json` and the provider-compatible `responseJsonSchema`.

For repair, retain the original operation's instructions and add the repair instructions. Send the rejected candidate and concise validation errors as task data. Preserve the same output schema and remaining operation budget.

The generation schema uses nullable app data and a separate status. The provider schema strips local string length/pattern constraints not in generateContent's documented JSON Schema subset. The full schema and semantic checks run in Go before compilation. The trusted external runtime validates local inputs and imported records; Flutter validates delivery metadata, not generated-tool execution. No schema setting guarantees correct calculations or an appropriate interpretation of the user's request. [generateContent API](https://ai.google.dev/api/generate-content)

## Generate an inspectable request without spending money

From the repository root:

```bash
mkdir -p ai/generated
python3 scripts/build_ai_request.py --input ai/examples/create-request.json > ai/generated/request.json
```

The resulting body targets:

```text
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent
Content-Type: application/json
x-goog-api-key: <GEMINI_API_KEY from backend secret storage>
Body: contents of ai/generated/request.json
```

In Go, construct this HTTPS request using `net/http` and JSON serialization. Set the key in the header; do not put it in a URL, log, HTML artifact, or Flutter config. Use a context deadline and a bounded response reader. Do not follow redirects with the credential header to a different host. No tools, search grounding, file uploads, or provider-side conversation history are enabled.

The script is a request-assembly reference, not an authentication, quota, or security boundary. The Go service must implement the validation, budget reservation, and idempotency controls in ROADMAP.md before using it with public traffic.

## Response handling contract

1. Check HTTP status, bounded response size, prompt blocking, candidate presence, and finish reason. Accept only a complete normal completion for schema parsing. Surface refusals/blocked content as a controlled error.
2. Extract the candidate's ordinary text parts, excluding thought parts. Reject missing text, unexpected tools, truncation, and malformed JSON; do not execute or display partial output as an app.
3. Validate with the full JSON Schema, then semantic validation. Ready requires a non-null app and no questions; other statuses require app=null. Clarification requires one to three questions; unsupported requires none.
4. Check unique IDs, references, kind requirements, formula stack correctness, total sizes, and edit compatibility. Flutter checks response metadata and downloaded size/hash; it never installs or executes a tool runtime. The external runtime validates its own input and import boundaries.
5. A repairable invalid result may consume one more provider call. Both transport retries and repairs share the absolute two-call limit. Never repair a provider refusal or silently activate a fallback model.
6. Derive usage from provider metadata, including billable thinking output if enabled later. Missing usage after a timeout remains potentially charged; keep its cost reservation instead of recording a free attempt.

For exact counting and budget admission, implement the provider countTokens operation or a demonstrably conservative upper bound for the complete request including instructions, schema, and repair context. The offline assembler does not estimate tokens. Never assume the user's prompt length equals total billed input.

`max_provider_calls_per_operation` counts generateContent inference attempts. An optional countTokens preflight is a separate request and must still fit the operation deadline. Budget checks use integer microdollars; decimal prices in configuration are parsed into exact fixed-point values.

## Required semantic checks

- Logger: at least one field; optional summary references a numeric input.
- Checklist: at least one text field and exactly one boolean field. The boolean is the completion state.
- Calculator: numeric fields only, at least one calculation, summary_field_id=null; no persisted history in v1, just the last local input state.
- Calculations: unique IDs, input-only numeric references, at most 32 postfix instructions; operand counts and null conventions must be correct. Exactly one stack value remains. Runtime handles absent values, non-finite results, and zero division as visible validation errors.
- Edits: same kind; existing field IDs, types, required flags, and calculation IDs retained; new fields optional. Go checks the base revision before issuing or publishing a new artifact; the external PWA runtime checks compatibility before a local migration. A display-unit edit does not transform historical records.
- Record limits and string sizes are enforced when the runtime receives local values, not just when the app definition is generated.

Use a paid provider project for real users. The published free/paid data-use terms differ; do not equate free quota with private production processing. The service sends descriptions and app definitions to the provider, never runtime records by design. [Gemini data-use terms](https://ai.google.dev/gemini-api/terms)
