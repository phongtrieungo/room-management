import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('review', Path(__file__).resolve().parents[1]/'scripts/review.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)

class ReviewTests(unittest.TestCase):
    def test_decrease_is_flagged_without_approval(self):
        current = {'A-1': {'electricity': 10, 'water': 20}}
        previous = {'A-1': {'electricity': 12, 'water': 18}}
        rows = review.compare(current, previous)
        self.assertEqual(rows[0]['difference'], -2)
        self.assertEqual(rows[0]['flags'], ['Reading decreased'])
        self.assertEqual(rows[1]['flags'], [])
        self.assertTrue(all(r['status']=='pending_review' for r in rows))

    def test_missing_room_is_reported(self):
        rows = review.compare({'A-1': {'electricity': 0, 'water': 0}}, {})
        self.assertIsNone(rows[0]['difference'])
        self.assertIn('Missing room in current or previous month', rows[0]['flags'])

    def test_invalid_month_rejected(self):
        for value in ('2026-13', '../foo', '2026-1'):
            with self.assertRaises(ValueError): review.parse_month(value)

    def test_duplicate_and_unreadable_values_rejected(self):
        header='room_code,electricity,water\n'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'sample.csv'
            for body in ('A-1,1,2\nA-1,3,4\n', 'A-1,?,4\n', '\n'):
                path.write_text(header+body)
                with self.assertRaises(ValueError): review.load(path)

    def test_zero_usage_is_valid(self):
        data = {'A-1': {'electricity': 0, 'water': 10}}
        rows = review.compare(data, data)
        self.assertTrue(all(r['difference']==0 and not r['flags'] for r in rows))

    def test_missing_baseline_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                review.locate(Path(tmp), review.parse_month('2026-01'))

    def test_comparison_matches_room_keys_not_row_order(self):
        previous = {'A-2': {'electricity': 100, 'water': 20}, 'A-1': {'electricity': 500, 'water': 30}}
        current = {'A-1': {'electricity': 510, 'water': 31}, 'A-2': {'electricity': 120, 'water': 22}}
        rows = review.compare(current, previous)
        self.assertEqual([r['difference'] for r in rows], [10, 1, 20, 2])

    def test_html_escapes_source_values(self):
        report={'month':'2026-10','sources':['<script>'], 'rows':[]}
        self.assertIn('&lt;script&gt;', review.render(report))

if __name__ == '__main__': unittest.main()
