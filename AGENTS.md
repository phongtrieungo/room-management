# Agent instructions

Read docs/workflow-spec.md before implementing this application. User instructions take precedence. This private GitHub starter contains synthetic data only; historical records and reference PDFs remain local and require explicit authorization for upload.

## Monthly data and extraction

- Use one months/YYYY-MM/readings.csv with room_code,electricity,water per approved month. Values are cumulative readings, not usage. Load the previous month's approved file as the baseline; do not duplicate it into another editable CSV.
- Preserve legacy files and reconcile conflicting handoffs before migration. Never silently choose between conflicting historical values.
- Accept photos of handwritten multi-room reading sheets and individual meters. Block filenames narrow expected coverage but do not identify individual rooms.
- Preserve images, raw transcription, normalized digits, image/crop or row references, extraction attempts, corrections and reasons. Keep drafts and evidence under a unique run directory; never overwrite approved history.
- Extract from the image before revealing prior readings. Use a second image-based pass and compare room/meter keys and digits. Agreement and model confidence are not proof of correctness. Escalate unclear digits and unresolved mapping; do not repair digits to make consumption plausible.
- Match by canonical room/meter keys, not row order. Reject missing, duplicate or unknown rooms, absent meters, invalid values and missing baselines. Zero is valid; blank is not zero.
- Use exact integer subtraction for whole-unit readings. Establish units/scale and use Decimal if fractional readings are introduced. Never silently round meter values or use binary floats for monetary calculations.
- Surface decreases and configured unusual usage. Reset/replacement needs evidence and an explicit usage calculation, not a waived negative result.
- Final bills and delivery require all errors resolved, warnings acknowledged, and explicit human approval bound to hashes of current readings, baseline, room/billing configuration and templates. Changes invalidate approval.

## Printing and email

- Old PDFs are design references for reusable HTML/CSS; they are not monthly files to edit. Preview and PDF must use the same populated HTML and print CSS.
- Reproduce A4 portrait room sheets with two columns/three card slots and the block title in the first slot, plus A4 landscape summary tables with orange headers. Confirm occupant/date/rent/rate/fee information from effective monthly configuration, not inferred historical amounts.
- Use vector text, table rules, plain fills and Vietnamese-capable fonts. Avoid full-page raster backgrounds, noise textures and decorative effects. Apply explicit margins/page breaks, complete cards, and repeated summary headers. Disable browser headers/footers and enable print backgrounds.
- Inspect every final page and reconcile printed values with approved data. A visually similar layout does not validate calculations.
- Email is optional and requires an explicitly configured/authorized printing recipient and approved attachments. Store credentials in environment/GitHub secrets, log message IDs and attachment hashes, and avoid duplicate delivery on retries. A question about email is not authorization to send.
- A GitHub runner cannot read ignored local images. Implement explicit intake before claiming phone-to-cloud operation works. Distinguish working code from planned components.

## Local history findings

The local January–October dataset has 94 rooms per audited CSV. Of nine transitions, seven match exactly and two conflict: June→July and August→September. The earlier claim of nine exact handoffs was incorrect. Leave these conflicts for source review. Historical CSVs use separate current/previous files; that is an import compatibility concern, not the new data model.

Report actual inputs, room coverage, baseline, errors/warnings, review decisions, approval identity, outputs and verification performed. Do not claim a successful remote run until observed. Synthetic examples cannot be approved as real readings or used for billing.
