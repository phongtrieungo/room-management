# Room Management

Monthly electricity/water photo extraction, comparison against previous readings, human review, and printable PDFs. Read `AGENTS.md` before implementing features or changing data. This repository is private. It contains code and synthetic demonstration records only; real tenant records and reference PDFs remain local.

## Run on GitHub

Open **Actions → Monthly reading review PDF → Run workflow** and choose a month such as `2026-10`. Its CSV pair must exist. Download the review artifact from the completed run: `review.pdf`, `review.html`, and `review.json`. Artifacts expire after 30 days; download anything you need to retain.

The workflow checks CSV structure and room coverage, compares current/previous readings, checks the previous-month handoff where available, and flags decreases and discrepancies. It never approves records, changes history, or calculates charges. Its repository permissions are read-only.

The PDF is currently a **draft review table**. Photo extraction, correction/approval persistence, and the final portrait room-card/landscape billing templates are not implemented yet. Historical PDFs are layout references that must be supplied separately. Do not use reference tariffs or tenant details as current billing configuration without confirming their source.

## Use with Codex Cloud

Grant your Codex GitHub connection access to this repository and select it when creating a cloud environment/task. Start with this prompt:

> Read AGENTS.md and README.md. Implement photo intake and extraction into proposed readings with image references. Compare with the previous month's approved readings, show a review table, and preserve the human approval gate. Then implement reusable HTML/CSS print templates using the layout contract in AGENTS.md and the reference PDFs once supplied. Do not infer missing billing configuration.

Connecting Codex is a separate account setup step. Running GitHub Actions does not start a Codex agent or provide a vision model. The current workflow needs no AI API key. Automated photo extraction will require a configured vision service; a ChatGPT subscription alone is not an API credential. Keep credentials out of Git.

## Local use

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m unittest discover -s tests -v
python scripts/review.py --month 2026-10 --output outputs
python scripts/print_pdf.py outputs/review.html outputs/review.pdf
```

Use a fresh output directory for every new run. Existing reports are never overwritten.

## Files

- Root: synthetic demo CSV pairs. Historical CSVs and `archived/` remain local. `MM-YYYY-current.csv` is current; `MM-YYYY.csv` is the previous side.
- `t6-pdf/` through `t10-pdf/`: historical PDF layout references described in the spec, not uploaded. Provide these separately when implementing the final layout.
- `scripts/`: CSV review and HTML-to-PDF rendering; `tests/`: data validation checks.
- `work/`, `outputs/`, `photos/`, and `.env` are ignored by Git. A future phone photo intake must explicitly transfer images into the chosen execution environment; ignored local photos are not available to a GitHub runner.

Comparing readings establishes plausibility, not transcription accuracy. Confirm digits against the original photos. A photo may contain multiple room readings; do not assume one photo equals one meter.
