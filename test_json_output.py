import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "search_notes.py"


def report(subject):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), subject, "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


class JsonOutputTests(unittest.TestCase):
    def test_single_candidate(self):
        result = report("beacon")
        self.assertEqual(result["status"], "candidate_found")
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual(
            result["candidates"][0]["source"],
            "Projects/Project Beacon.md",
        )
        self.assertEqual(
            result["candidates"][0]["contents"],
            "Monday at 10:30.",
        )

    def test_multiple_candidates(self):
        result = report("lantern")
        self.assertEqual(result["status"], "review_required")
        self.assertEqual(len(result["candidates"]), 2)
        self.assertEqual(
            {item["contents"] for item in result["candidates"]},
            {"Friday at 16:00.", "Wednesday at 14:20."},
        )

    def test_no_match(self):
        result = report("nebulon")
        self.assertEqual(result["status"], "no_match")
        self.assertEqual(result["candidates"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
