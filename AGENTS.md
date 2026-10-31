# Room Records Agent Specification

Repository status: this GitHub starter includes code and synthetic demo CSVs only. Historical records and reference PDFs described below remain in the original local folder and have not been uploaded. Never treat demo data as real or approve it for billing. Request the references when implementing the final print templates.

## Purpose

Govern agent work on the room electricity and water records in this directory. The agent may prepare monthly readings and print files, but must preserve source records, make every derived value traceable, and leave uncertain data for human review.

## Scope and authority

- Treat the monthly CSV files in this directory and `archived/` as historical source records. Treat the PDFs in `t6-pdf/` through `t10-pdf/` as visual print references only. Resolve actual paths before use; the October reference folder is currently `t10-pdf/`.
- The final user deliverable is PDF. Build HTML with print CSS as the rendering template, then print it to PDF. HTML is an implementation/preview artifact, not the final deliverable.
- Do not assume that a PDF total is correct or that the method used to calculate it is known.
- No meter photos, HTML templates, scripts, spreadsheets, tests, rates, fees, or special billing rules were present in the audited source folder. Do not claim to have verified any of these.
- The `*-current.csv` file is the current-reading side of its month; the same-month CSV is its matching previous-reading side. Confirm actual headers and row mapping from the files before processing. Do not infer columns from filename alone.
- Preserve the existing CSV schema and encoding when exporting compatible CSVs. If the schema cannot be established safely, stop and report the issue rather than silently changing it.

## File safety

- Read historical files without modifying, renaming, moving, or deleting them.
- Never overwrite an existing source CSV, PDF, photo, or prior approved output. Before writing, check whether the destination exists; use a new versioned path or stop for review.
- Keep generated working files and previews in `work/` and final deliverables in `outputs/` when those directories are available. Do not mix generated files into the historical source folders.
- Do not install dependencies, access external services, or send/share records unless the user explicitly requests it.
- Before any write, state the intended files and purpose in the task report. A user’s request to create or update a deliverable authorizes that scoped write; it does not authorize editing historical source data.

## Required data model and provenance

For processing, normalize records internally by `(month, room_code, meter_type)` while retaining the original rows and source paths. Keep electricity and water separate. Preserve leading zeros in room codes and reading strings unless the source format establishes that they are not meaningful; never strip zeros from meter readings.

The monthly input is a new photo set of electricity and water meters. Treat readings extracted from those photos as proposed current readings for the target month. Compare each proposed reading with that room and meter's approved reading from the previous month. Use the previous month's approved current reading as the baseline when available. If only a previous-reading CSV is available, first verify that it represents the same room and meter baseline; report ambiguity instead of guessing.

Every proposed or approved reading must retain:

- month, room code, meter type, reading value, and source file or photo reference;
- whether it is a previous or current reading;
- extraction method (transcribed, OCR/vision, or imported), review status, and any correction history;
- comparison result against the prior month and any warning or reviewer note.

Do not replace a corrected value without recording the earlier value, correction, and reason. If no durable audit-log format has been approved, keep the correction log with the generated monthly deliverables and ask before introducing a new permanent data format.

## Monthly processing workflow

1. **Identify the target month and inventory the photo set:** Confirm the month, image count, and intended room and meter for each image. Do not assume photo order implies room or meter identity.
2. **Establish the comparison baseline:** Load the previous month's approved readings, keyed by exact room code and meter type. Verify the baseline source and identify missing, duplicate, or ambiguous keys before extracting or comparing.
3. **Extract proposed readings:** For every photo, record the source image reference, target month, room code, meter type, proposed digits, and confidence/legibility note. Do not guess unreadable digits. Where image identity is unclear, ask for mapping or leave it unresolved.
4. **Validate coverage and uniqueness:** Check that each expected room has one electricity and one water reading, as applicable. Flag missing photos, duplicate room/meter entries, unrecognized rooms, and unreadable or conflicting values. Do not silently discard or coerce entries.
5. **Compare with the previous month:** Show each proposed current reading beside its approved previous reading and the difference. Flag decreases, implausible jumps, and any anomalous difference for human review. A mismatch is evidence to inspect the photo/source, not permission to change either reading automatically. Apply a threshold only if the user has defined one; otherwise report the differences without inventing a threshold.
6. **Human review gate:** Present proposed readings, photo references, previous readings, differences, and flags in a reviewable table. Do not save them as approved current readings, carry them forward, or use them in final print totals until the user confirms or corrects them. Record corrections and their reasons.
7. **Calculate usage only after approval:** For each room and meter, usage is `approved current reading - approved previous reading`. A negative result remains blocked for review unless the user confirms a meter reset/rollover rule. Do not infer tariff, taxes, fixed fees, rounding, allocation, or payment totals.
8. **Prepare next-month opening values:** Carry forward only the approved current readings. Keep unresolved rooms visible; do not fill them by guesswork.
9. **Generate PDFs from HTML:** Inspect the existing PDFs for layout, implement that layout in HTML with print CSS, and print the HTML to PDF. Follow the print contract below. Layout inspection does not authorize importing historical tenant information, dates, tariffs, fees, or totals as current business rules. Check rendered final PDF pages before delivery.
10. **Report:** Summarize the photo set, baseline source, coverage and comparison results, unresolved exceptions, calculations/rules applied, output paths, and any human decisions still required.

## HTML-to-PDF print contract

The PDFs are the visual references; there is no existing HTML template to reuse. The following observations come from October PDF page metadata and visual inspection of the first page of each representative layout (`day-a.pdf` and `tong-cong.pdf`). Inspect remaining pages during implementation to establish continuation and final-page behavior.

### Room sheets: `t10-pdf/day-a.pdf` through `day-d.pdf`

- Use A4 portrait (210 × 297 mm). Reference page counts are A: 5, B: 5, C: 5, D: 3; these are reference facts, not fixed limits for future months.
- Use a two-column, three-row grid of bordered cards. The first slot contains a large centered block title and room count, for example `Dãy A` and `26 phòng`; room cards follow in reading order. Preserve room order from the verified room roster.
- Each room card has a bold header with room code, occupant name, and date. Below it, use a bordered table with `Số mới`, `Số cũ`, `Sử dụng`, `Đơn giá`, and `Thành tiền`, with rows for `Tiền điện`, `Tiền nước`, and `Tiền rác`.
- Below a divider, show `Tiền phòng` and `Tiền điện + nước + rác` as separate labeled amounts. Preserve Vietnamese accents, readable numbers, black rules, generous card spacing, and the visible left inset/guide used in the reference.
- Obtain occupant names, applicable dates, room rents, tariffs, and fees from an explicitly established current source when required. Do not fabricate values to fill the visual fields. If these inputs are missing, prepare a clearly marked draft and report the missing fields; do not issue a complete billing PDF with guessed amounts.

### Total sheet: `t10-pdf/tong-cong.pdf`

- Use A4 landscape (297 × 210 mm). The October reference has four pages, one per block.
- Use a centered block/month heading, an orange header row, thin table rules, compact rows, and a bold totals row.
- Preserve the reference column order: `Trả tiền`, `P`, `Người ở`, `Ngày đến`, `Ngày đóng`, `Ở đến`, `Tiền đóng`, `Điện mới`, `Điện cũ`, `Sử dụng`, `Thành tiền`, `Nước mới`, `Nước cũ`, `Sử dụng`, `Thành tiền`, `Giá phòng`.
- Keep all columns within the printable width. Match the reference structure while preventing clipping, unreadable scaling, or unintended duplicate headings.

### Rendering and acceptance

- Use explicit A4 sizes, orientation, and margins in `@page`, with separate print documents or named pages for portrait and landscape outputs. Use physical units for page geometry.
- Print at 100% scale with browser URL/date headers and footers disabled. Enable print backgrounds so the summary header color is preserved. Wait for fonts and layout before PDF generation; use fonts supporting Vietnamese.
- Keep each room card intact with controlled page breaks. Repeat table headers on any necessary continuation page. Avoid extra blank pages, missing rooms, clipped columns, overlapping text, and split digits.
- Render and visually inspect the generated PDFs, including continuation and final pages. Check room coverage and values against the approved dataset independently of layout checks.
- Deliver the portrait block PDFs and landscape total PDF. Keep HTML/CSS and preview images as supporting work artifacts. This specification update defines the workflow; it does not itself implement the templates or generate a new month's PDFs.

## Known audit findings to retain

- January–October 2026 CSV records were identified, with archived files through August and September/October files at the top level.
- Each audited CSV contained 94 unique room codes with no blank rows or duplicate codes.
- Nine month-to-month handoffs matched exactly; June→July and August→September had reading differences and must remain flagged until reviewed.
- Existing A4 PDF references include `t6-pdf/` through `t10-pdf/`. October has four portrait block PDFs and one landscape total PDF.
- The CSVs contain readings, not validated usage or charges. The subtraction formula is a proposed usage calculation; billing rules and PDF total calculations remain unverified.
- The expected routine is to extract the new month's current readings from meter photos and compare them against the previous month's approved readings to validate plausibility before approval.

These findings are an initial audit baseline, not a substitute for rechecking files when a task depends on them. If files change or a new month is added, rerun the relevant checks.

## Completion criteria

A monthly task is complete only when:

- inputs and source-to-output mapping are documented;
- validation results and all exceptions are reported;
- every new photo-derived reading is traceable to its image and compared with the correct previous-month room/meter baseline;
- no unresolved or unreviewed reading is presented as approved;
- calculated usage is traceable to approved current and previous readings;
- no unsupported charge or billing rule is used;
- outputs do not overwrite source records or previous deliverables;
- print pages have been rendered and visually checked when PDFs are produced.

If any condition cannot be met, stop before approval-dependent writes and report what is blocked and what evidence or decision is needed.
