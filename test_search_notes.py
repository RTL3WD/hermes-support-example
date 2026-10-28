import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "search_notes.py"


def search(subject):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), subject],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


class SearchTests(unittest.TestCase):

    def test_multiple_candidates_require_review(self):
        output = search("lantern")
        self.assertIn("REVIEW REQUIRED", output)
        self.assertIn("Candidate: Archive/Project Lantern.md", output)
        self.assertIn(
            "Candidate: Project Lantern’s maintenance window.md", output
        )
        self.assertIn("Friday at 16:00.", output)
        self.assertIn("Wednesday at 14:20.", output)


    def test_nested_project(self):
        output = search("beacon")
        self.assertIn("Candidate: Projects/Project Beacon.md", output)
        self.assertIn("Monday at 10:30.", output)

    def test_exact_project_name(self):
        output = search("lantern")
        self.assertIn("Project Lantern’s maintenance window.md", output)
        self.assertIn("Wednesday at 14:20.", output)
        self.assertNotIn("Candidate: Scheduled Support Process.md", output)

    def test_misspelled_project_name(self):
        output = search("latern")
        self.assertIn("Project Lantern’s maintenance window.md", output)
        self.assertIn("Wednesday at 14:20.", output)

    def test_different_project(self):
        output = search("harbor")
        self.assertIn("Project Harbor.md", output)
        self.assertIn("Friday at 09:00.", output)
        self.assertNotIn("Candidate: Project Lantern", output)

    def test_nonexistent_project(self):
        output = search("nebulon")
        self.assertIn("No matching filename found", output)
        self.assertNotIn("Contents:", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
