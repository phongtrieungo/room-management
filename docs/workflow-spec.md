# Monthly photo-to-bill specification

## Scope

Use a small file-based application. CSV is sufficient for this property; add one JSON review record per run for evidence and approval. A database or dashboard is not required initially. Currently implemented: synthetic monthly snapshots, deterministic comparison, draft review HTML/JSON and PDF rendering code. Photo extraction, approvals, billed templates and email are future work.

## Files and monthly lifecycle

| Path | Meaning |
| --- | --- |
| references/layout/ | One selected room-sheet and summary PDF; development references only |
| templates/bill.html, summary.html, print.css | Reusable source of the printed layouts; to implement |
| config/YYYY-MM/rooms.csv | Effective room roster, occupant/rent/date details |
| config/YYYY-MM/billing.json | Effective rates, fees, units, rounding and optional anomaly thresholds |
| config/delivery.json | Authorized email recipient/sender/preferences, no credentials |
| months/YYYY-MM/photos/A-01.jpg | Block-labelled original images; multiple images per block allowed |
| months/YYYY-MM/runs/RUN_ID/draft.csv | Proposed current readings |
| months/YYYY-MM/runs/RUN_ID/review.json | Evidence, extraction attempts, flags, corrections, approval and delivery records |
| months/YYYY-MM/readings.csv | Approved cumulative readings for this month |
| outputs/YYYY-MM/RUN_ID/ | Frozen generated HTML/CSS and final PDFs |

Unimplemented paths define the target contract, not existing functionality. Keep raw photos, run evidence and outputs in durable private storage. Ignored local files and expiring GitHub artifacts alone do not provide cloud storage. Approved CSVs can be versioned in a private repository after explicit upload authorization. Keep large photo/PDF archives outside Git. Initially accept task attachments or an input bundle; choose an authorized durable upload destination before claiming hands-free phone operation.

The approved CSV schema is room_code,electricity,water, with one row per expected active room. Month comes from its directory. Values contain cumulative numeric readings without display separators. Preserve the original transcription, including leading zeros, in evidence; numeric normalization may remove insignificant leading zeros while preserving magnitude. Room aliases such as 1A map to A-1 only through a verified explicit mapping.

November's draft compares against approved October readings. After correction and approval, publish November readings; December uses that exact snapshot. Do not duplicate previous readings or make usage/charges another authoritative input. Keep derived values in review/billing outputs.

Approved history revisions require old/new values, reason, reviewer and file hash, with prior bytes retained. Bind later bills to the revision actually used and prevent simultaneous promotion of competing runs. Preserve all legacy input files. During migration, reconcile disagreements between a month's previous side and the prior month's current side before promoting a canonical snapshot. January usage also needs its original opening baseline.

## Extraction harness

1. Register target month, block and original image SHA-256. A filename such as A-01.jpg identifies a block only. Support handwritten multi-room sheets and individual meter photos; never assume image order establishes room identity.
2. Extract every visible room and meter value without showing the extractor last month's values. Record raw digits, normalized value, image/row/crop reference and legibility. Leave unreadable digits null; do not guess.
3. Perform a second image-based pass, then compare room identity, meter type and digits. Resolve disagreements through crop inspection or human review/a clearer photo. Two passes can share errors; agreement and self-reported confidence cannot prove accuracy.
4. Consolidate against the effective room roster. Detect shifted rows/columns, duplicate photos, unknown/missing rooms and overlapping/conflicting observations. Retain provenance when merging matching observations; conflicting duplicates remain errors.
5. Save draft.csv and review.json with extraction method/model/version, attempts and corrections/reasons. Deterministic code then compares against approved history. The model must not calculate or repair bill usage.

## Validation and approval

| Condition | Required action |
| --- | --- |
| Missing/duplicate/unknown room, absent meter, unclear room identity or unreadable digits | Blocking review error; no zero fill or skipped row |
| Missing/unapproved baseline, changed meter or unit | Establish correct baseline before billing |
| Non-numeric or invalid-scale value | Preserve raw input; resolve from evidence |
| Current below previous | Blocking error; investigate transcription or documented meter event |
| Current equals previous | Valid zero usage; warn only under a configured inactivity rule |
| Large or unusual usage | Flag under explicit configured thresholds; require a recorded decision |
| Extraction disagreement | Review even when subtraction looks plausible |
| Missing effective rent/rate/fee/room data | Block billing; draft reading review may continue |

Compute usage = current - previous with exact integers for whole-unit meters. If fractional readings exist, establish units/scale and use Decimal. Parse separators under an explicit convention; never silently remove a meaningful decimal point. Use exact integer/Decimal VND arithmetic and defined rounding for charges. Meter reset/replacement/rollover requires evidence and a documented consumption calculation; never charge negative usage or silently clamp it to zero.

Review must show room, meter, previous reading, proposed reading, difference, evidence and specific flags, plus block/property coverage counts. Thresholds are not assumed. Corrections must retain original values and reasons. Once errors are resolved and warnings acknowledged, record explicit user approval with reviewer, timestamp and hashes of current CSV, baseline, room/billing configuration and template/CSS version. Changes invalidate approval and require recalculation/review. No unresolved error or unapproved warning may enter final PDFs or email. Clearly marked draft review documents may be produced earlier.

## Printing

PDF references guide template development; never edit old PDFs each month or embed screenshots of old bills. Use reusable HTML and print CSS with a consistent Chromium renderer. The preview and PDF use identical populated HTML/data and print styling. Preserve the established portrait two-column/three-row cards and landscape orange-header total table, A4 geometry, complete cards, supported Vietnamese fonts, controlled page breaks and repeated table headers.

Reproduce layout/typography without invisible export artifacts. Prefer vector text/rules and plain CSS fills. Avoid full-page images, noise textures and decorative filters/shadows. Inspect every page and reconcile every room/amount against the approved dataset. Freeze rendered inputs/output hashes in the run record. Deliver day-a.pdf through day-d.pdf and tong-cong.pdf as applicable; define empty-block behavior from the effective roster. Flag abnormal PDF size relative to comparable page counts rather than shrinking text to meet an arbitrary limit.

## Optional printing email

Support an explicitly authorized printing recipient and selected approved PDF attachments. Store credentials in GitHub Actions secrets or environment variables, not committed JSON. Use authenticated TLS SMTP or a chosen mail API. Once the user authorizes the recipient, attachment scope and recurring behavior, delivery can follow approval automatically without repeated permission prompts. The current discussion authorizes no send.

Check provider attachment limits. Send compact PDFs only, not source photos/unrelated records. Bind delivery to month, approved run, recipient and attachment hashes. Log provider/message ID and status. Do not resend completed deliveries automatically. Ambiguous timeouts after submission need reconciliation; SMTP does not guarantee exactly-once delivery.

Implementation references: [GitHub Actions secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets), [Python SMTP](https://docs.python.org/3/library/smtplib.html).

## Implementation and verification

Implement extraction/evidence, then validation/approval, then effective billing configuration and matching HTML/CSS, then PDF verification and optional email. GitHub Actions orchestrates code, not an implicit AI model. Choose a Codex task with images or a configured vision API and explicitly transfer inputs to that environment.

Test human-checked multi-room photos, ambiguous digits, shifted rows, overlapping images, mixed blocks, missing/extra rooms, reordered CSV rows, zero usage, decreases, configured jumps, meter events, missing baselines, changes after approval, exact charge/rounding rules and delivery retries. Verify every page and printed value. Observe a successful remote run before claiming the workflow works on GitHub.

## Local investigation on 2026-10-31

August day-a.pdf is 167,106 bytes with no image objects found. October day-a.pdf is 14,817,494 bytes with 20 image objects; their compressed streams total 14,642,628 bytes, about 98.8% of its size. Repeated image objects and transparency masks contribute to the overhead. A decoded large RGB image is a noise-like texture; the original export process causing it is unknown. September has the same inflated image footprint. Clean HTML/CSS should avoid that overhead; measure actual generated output before promising a file size.

Rechecking the nine January–October transitions found seven exact handoffs and two conflicting handoffs. June→July affects C-20 and C-21; August→September affects A-7 water and D-8 electricity. A current water value below its previous value must be flagged and checked against the image rather than repaired by inferring a missing digit. These are local investigation findings; real files remain unchanged and are not included in the synthetic GitHub samples.
