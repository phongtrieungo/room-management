# Room Management

A small workflow for monthly block photos, reviewed readings, reusable HTML/CSS, and printable PDF bills. Read AGENTS.md and docs/workflow-spec.md first.

This starter contains code and synthetic samples only. Actual records and PDF references remain local. The GitHub repository is private. Use the manual Actions workflow to run the synthetic example.

## Structure

| Path | Purpose |
| --- | --- |
| months/YYYY-MM/readings.csv | One approved readings snapshot per month; included examples are synthetic |
| months/YYYY-MM/photos/ | Block photos such as A-01.jpg; excluded from Git |
| months/YYYY-MM/runs/RUN_ID/ | Draft CSV, image evidence, checks, corrections and approval record |
| config/YYYY-MM/ | Effective room roster and billing rules, to implement |
| templates/ | Reusable room bill, summary and print CSS, to implement |
| references/layout/ | Selected PDF examples for template development, supplied separately |
| outputs/YYYY-MM/RUN_ID/ | Generated HTML and PDFs, excluded from Git |
| scripts/, tests/, .github/workflows/ | Application code, checks and GitHub execution |
| docs/ | Extraction, validation, approval, printing and delivery contract |

CSV columns: room_code,electricity,water. Store cumulative readings; load the previous month's file automatically. Do not keep a second editable previous-reading copy. See the spec before migrating legacy pairs or generating charges.

## Current capability

The starter reviews two monthly snapshots and creates draft comparison HTML/JSON. Its GitHub workflow can print that HTML to a draft review PDF after publication. It checks structure, numeric values, room matching and decreases. It never approves records or generates charges.

Photo extraction, persisted approval, configured anomaly thresholds, final bill templates, email delivery and a phone upload UI are not implemented. The target folders for those features are documented, not dummy working implementations. Running GitHub Actions alone does not provide a vision agent.

## Local review

Run python3 -m unittest discover -s tests -v.

Run python3 scripts/review.py --month 2026-10 --output outputs/2026-10/demo.

Use --current path/to/draft.csv to compare a new extracted draft instead of the target month's snapshot. The previous month's snapshot is required. Always use a fresh output directory. All review results remain pending human review.

For PDF rendering, create a Python virtual environment, install requirements.txt, run python -m playwright install chromium, then run python scripts/print_pdf.py outputs/2026-10/demo/review.html outputs/2026-10/demo/review.pdf.

Actions → Monthly reading review PDF → Run workflow can review the synthetic 2026-10 example. Download outputs before the 30-day artifact expiration. Ignored local images are not available on GitHub runners; cloud intake needs an explicit authorized upload/storage mechanism.

Implement extraction/evidence first, validation/approval second, confirmed billing configuration and matching print templates third, then PDF verification and optional email. Secrets must stay out of Git.
