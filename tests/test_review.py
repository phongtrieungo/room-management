import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('review', Path(__file__).resolve().parents[1]/'scripts/review.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)

class ReviewTests(unittest.TestCase):
    def test_decrease_and_handoff_are_independent(self):
        current = {'A-1': {'electricity': 10, 'water': 20}}
        previous = {'A-1': {'electricity': 12, 'water': 18}}
        prior = {'A-1': {'electricity': 11, 'water': 18}}
        rows = review.compare(current, previous, prior)
        self.assertEqual(rows[0]['difference'], -2)
        self.assertEqual(len(rows[0]['flags']), 2)
        self.assertEqual(rows[1]['flags'], [])
        self.assertTrue(all(r['status']=='pending_review' for r in rows))

    def test_missing_room_is_reported(self):
        rows = review.compare({'A-1': {'electricity': 0, 'water': 0}}, {})
        self.assertIsNone(rows[0]['difference'])
        self.assertIn('Missing room in monthly pair', rows[0]['flags'])

    def test_invalid_month_rejected(self):
        for value in ('2026-13', '../foo', '2026-1'):
            with self.assertRaises(ValueError): review.parse_month(value)

    def test_duplicate_and_unreadable_values_rejected(self):
        header='room_code,electric_current,water_current\n'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'sample.csv'
            for body in ('A-1,1,2\nA-1,3,4\n', 'A-1,?,4\n', '\n'):
                path.write_text(header+body)
                with self.assertRaises(ValueError): review.load(path, 'current')

    def test_html_escapes_source_values(self):
        report={'month':'2026-10','sources':['<script>'], 'rows':[]}
        self.assertIn('&lt;script&gt;', review.render(report))

if __name__ == '__main__': unittest.main()
