import json
import argparse
import re
from difflib import SequenceMatcher
from pathlib import Path

parser = argparse.ArgumentParser(description="Find test notes by project name.")
parser.add_argument("subject", help="One project-name word, such as lantern")
parser.add_argument("--json", action="store_true", help="Print a structured report")
args = parser.parse_args()

query = args.subject.casefold().strip()
if not re.fullmatch(r"[a-z0-9]+", query):
    parser.error("Enter one project-name word using letters or numbers.")

vault = Path(__file__).resolve().parent / "sample_vault"
if not vault.is_dir():
    parser.error(f"Test folder is missing: {vault}")

candidates = []

for path in sorted(vault.rglob("*.md")):
    title = re.sub(r"['’]s\b", "", path.stem.casefold())
    words = re.findall(r"[a-z0-9]+", title)
    similarity = max(
        (SequenceMatcher(None, query, word).ratio() for word in words),
        default=0,
    )

    if similarity >= 0.80:
        candidates.append((similarity, path))

candidates.sort(key=lambda item: (-item[0], item[1].name))


if args.json:
    status = (
        "no_match" if not candidates
        else "review_required" if len(candidates) > 1
        else "candidate_found"
    )
    report = {
        "query": query,
        "status": status,
        "search_scope": "synthetic sample_vault",
        "candidates": [
            {
                "source": path.relative_to(vault).as_posix(),
                "spelling_similarity": round(similarity, 4),
                "contents": path.read_text(encoding="utf-8").strip(),
            }
            for similarity, path in candidates
        ],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0)

if not candidates:
    print("No matching filename found in the test folder.")
else:
    if len(candidates) > 1:
        print("REVIEW REQUIRED: Multiple candidate notes found.")
        print("Filename similarity alone cannot establish the correct answer.")
    for similarity, path in candidates:
        print(f"\nCandidate: {path.relative_to(vault).as_posix()}")
        print(f"Spelling similarity: {similarity:.0%}")
        print(f"Contents: {path.read_text(encoding='utf-8').strip()}")
