#!/usr/bin/env python3
"""Build a Gemini generateContent JSON body locally. Does not call the API."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def provider_schema(value):
    # Keep authoritative constraints in the original schema/host validators.
    # These keywords are not in generateContent's documented portable subset.
    omitted = {"$schema", "pattern", "minLength", "maxLength"}
    if isinstance(value, dict):
        return {key: provider_schema(item) for key, item in value.items() if key not in omitted}
    if isinstance(value, list):
        return [provider_schema(item) for item in value]
    return value


def build(task, invalid_candidate=None, validation_errors=None):
    config = json.loads((ROOT / "config/ai.json").read_text())
    expected = {"operation", "prompt", "locale", "runtime_version", "base_revision", "current_spec"}
    if set(task) != expected:
        raise ValueError("Task must contain exactly the fields shown in ai/examples/create-request.json")
    if task["operation"] not in {"create", "edit"}:
        raise ValueError("operation must be create or edit")
    if not isinstance(task["prompt"], str) or not task["prompt"].strip():
        raise ValueError("prompt must be non-empty text")
    if len(task["prompt"].encode()) > config["limits"]["max_user_prompt_bytes"]:
        raise ValueError("prompt exceeds byte limit")
    if task["operation"] == "create" and (task["current_spec"] is not None or task["base_revision"] is not None):
        raise ValueError("create requires null current_spec and base_revision")
    if task["operation"] == "edit" and (not isinstance(task["current_spec"], dict) or type(task["base_revision"]) is not int or task["base_revision"] < 1):
        raise ValueError("edit requires current_spec and a positive base_revision")
    if len(json.dumps(task).encode()) > config["limits"]["max_request_bytes"]:
        raise ValueError("task exceeds request byte limit")
    mode = "repair" if invalid_candidate is not None else task["operation"]
    if mode == "repair" and not isinstance(validation_errors, list):
        raise ValueError("repair requires a JSON array of validation errors")
    system = (ROOT / config["system_prompt"]).read_text()
    operation_prompt = (ROOT / config["task_prompts"][task["operation"]]).read_text()
    if mode == "repair":
        operation_prompt += "\n\n" + (ROOT / config["task_prompts"]["repair"]).read_text()
    manifest = json.loads((ROOT / config["capabilities"]).read_text())
    instructions = system + "\n\n" + operation_prompt + "\n\nCapability manifest:\n" + json.dumps(manifest)
    # Identity/revision metadata is host-owned and is not passed to the model.
    data = {key: task[key] for key in ("operation", "prompt", "locale", "current_spec")}
    if mode == "repair":
        data.update(invalid_candidate=invalid_candidate, validation_errors=validation_errors)
    schema = json.loads((ROOT / config["response_schema"]).read_text())
    generation = dict(config["primary"]["generation_config"])
    generation.update(responseMimeType="application/json", responseJsonSchema=provider_schema(schema))
    return {
        "systemInstruction": {"parts": [{"text": instructions}]},
        "contents": [{"role": "user", "parts": [{"text": json.dumps(data, ensure_ascii=False)}]}],
        "generationConfig": generation,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--invalid-candidate", type=Path)
    parser.add_argument("--validation-errors", type=Path)
    args = parser.parse_args()
    if bool(args.invalid_candidate) != bool(args.validation_errors):
        parser.error("repair needs both --invalid-candidate and --validation-errors")
    task = json.loads(args.input.read_text())
    # Read as text to support repair of malformed provider JSON.
    candidate = args.invalid_candidate.read_text() if args.invalid_candidate else None
    errors = json.loads(args.validation_errors.read_text()) if args.validation_errors else None
    print(json.dumps(build(task, candidate, errors), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
