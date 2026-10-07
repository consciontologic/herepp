# Edit an existing tool

Read the prompt, locale, and current_spec in the JSON task data. Return a complete proposed specification, not a textual diff or patch.

Preserve the kind, every existing field ID and type, and every existing calculation ID. Changing visible labels, descriptions, display units, colors, field ordering, numeric formulas, or optional summary selection is allowed when requested. Treat changing a display unit as a label change only; do not claim existing measurements were converted.

Allow new fields only when required=false. Preserve existing fields' required flags. Do not delete fields, repurpose their meaning, convert stored values, or introduce required inputs into an existing data schema. New calculations are allowed within limits.

If the user needs a destructive or incompatible change, return unsupported and describe creating a new copy or using a future explicit migration workflow. Existing records are not in the request and must never be requested just to perform an ordinary label or layout edit.

Keep all unrelated behavior intact. The host will compare the proposed specification against the current one before activating it.
