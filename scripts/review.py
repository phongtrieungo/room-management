"""Create draft comparison reports from historical CSV pairs without editing them."""
import argparse
import csv
import datetime as dt
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def parse_month(value):
    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}', value):
        raise ValueError('Month must be YYYY-MM')
    return dt.date.fromisoformat(value + '-01')

def locate(root, month, current, required=True):
    name = month.strftime('%m-%Y') + ('-current' if current else '') + '.csv'
    matches = [p for p in (root / name, root / 'archived' / name) if p.is_file()]
    if len(matches) > 1:
        raise ValueError(f'Ambiguous source: {name}')
    if not matches and required:
        raise ValueError(f'Missing source: {name}')
    return matches[0] if matches else None

def load(path, role):
    expected = ['room_code', f'electric_{role}', f'water_{role}']
    result = {}
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.reader(stream)
        if next(reader, None) != expected:
            raise ValueError(f'{path.name}: expected headers {expected}')
        for line, values in enumerate(reader, 2):
            if len(values) != 3:
                raise ValueError(f'{path.name}:{line}: expected three fields')
            room, electric, water = values
            if not room or room != room.strip() or room in result:
                raise ValueError(f'{path.name}:{line}: blank, padded or duplicate room')
            if not all(re.fullmatch(r'[0-9]+', n) for n in (electric, water)):
                raise ValueError(f'{path.name}:{line}: readings must be nonnegative integers')
            result[room] = {'electricity': int(electric), 'water': int(water)}
    if not result:
        raise ValueError(f'{path.name}: no readings')
    return result

def compare(current, previous, prior=None):
    rows = []
    for room in sorted(current.keys() | previous.keys()):
        for meter in ('electricity', 'water'):
            new = current.get(room, {}).get(meter)
            old = previous.get(room, {}).get(meter)
            baseline = prior.get(room, {}).get(meter) if prior is not None else None
            delta = new - old if new is not None and old is not None else None
            flags = []
            if new is None or old is None:
                flags.append('Missing room in monthly pair')
            if delta is not None and delta < 0:
                flags.append('Reading decreased')
            if prior is None:
                flags.append('Prior-month handoff unavailable')
            elif baseline is None:
                flags.append('Room missing from prior month')
            elif old != baseline:
                flags.append('Previous reading differs from prior month current')
            rows.append(dict(room=room, meter=meter, previous=old, current=new,
                             difference=delta, prior_month_current=baseline,
                             flags=flags, status='pending_review'))
    return rows

def render(report):
    esc = lambda v: html.escape('—' if v is None else str(v))
    cells = []
    for row in report['rows']:
        fields = [row['room'], row['meter'], row['prior_month_current'],
                  row['previous'], row['current'], row['difference'],
                  '; '.join(row['flags']) or 'No automatic flags; review required']
        cells.append('<tr>' + ''.join('<td>'+esc(v)+'</td>' for v in fields) + '</tr>')
    return '''<!doctype html><html lang="en"><meta charset="utf-8">
<title>Draft reading review</title><style>
@page{size:A4 landscape;margin:12mm}*{box-sizing:border-box}
body{font:9pt Arial,sans-serif;color:#111}h1{font-size:16pt}
table{width:100%;border-collapse:collapse;table-layout:fixed}
th,td{border:1px solid #555;padding:4px;overflow-wrap:anywhere}
th{background:#ff841f;text-align:left}thead{display:table-header-group}
tr{break-inside:avoid}td:nth-child(7){width:30%}
</style><h1>DRAFT — Reading review: '''+esc(report['month'])+'''</h1>
<p>Imported CSV readings; all values pending human review. This is not a bill.
Differences are review calculations, not approved usage. No jump threshold is configured.</p>
<p>Sources: '''+esc(', '.join(report['sources']))+'''</p>
<table><thead><tr><th>Room</th><th>Meter</th><th>Prior month current</th>
<th>Previous side</th><th>Current side</th><th>Difference</th><th>Review</th>
</tr></thead><tbody>'''+''.join(cells)+'''</tbody></table></html>'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--month', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    month = parse_month(args.month)
    cp = locate(ROOT, month, True)
    pp = locate(ROOT, month, False)
    prior_path = locate(ROOT, month - dt.timedelta(days=1), True, required=False)
    current, previous = load(cp, 'current'), load(pp, 'previous')
    prior = load(prior_path, 'current') if prior_path else None
    rows = compare(current, previous, prior)
    report = dict(month=args.month, status='draft',
                  sources=[str(p.relative_to(ROOT)) for p in (cp, pp, prior_path) if p],
                  current_rooms=len(current), previous_rooms=len(previous),
                  flagged_readings=sum(bool(r['flags']) for r in rows), rows=rows)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'review.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    (args.output/'review.html').write_text(render(report), encoding='utf-8')
    print(f'Draft report: {len(current)} rooms, {report["flagged_readings"]} flagged readings')

if __name__ == '__main__':
    main()
