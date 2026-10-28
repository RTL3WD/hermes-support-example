# Hermes Support Engineering Lab

A support investigation and Python retrieval prototype inspired by a
real search failure in my personal Hermes Agent setup.

## Original symptom

Hermes did not find a project maintenance note until I supplied a
location hint. The project name appeared only in the filename; the
note body contained only the maintenance time.

Hermes's subsequent account of its tool calls suggested inadequate
filename matching. I have not independently verified the original logs.

## Prototype

The Python script:
- Searches Markdown filenames throughout a synthetic vault.
- Uses spelling similarity to identify possible typo matches.
- Reads matching notes and displays their contents.
- Returns no match when no filename meets the threshold.

## Run

Requires Python 3.12. No third-party packages are needed.

From this project folder:

    python search_notes.py lantern
    python search_notes.py latern
    python search_notes.py beacon
    python test_search_notes.py

## Validation

Five automated tests cover:
- Exact project name.
- Misspelled project name.
- A different project.
- A nonexistent project.
- A note inside a nested folder.

A controlled experiment reproduced the nested-folder failure before
recursive searching was added, then verified the correction.

## Current limitations

- Standalone prototype; not integrated with Hermes.
- Uses fictional notes, not my personal Obsidian vault.
- Accepts one project-name word, not a natural-language question.
- The similarity threshold is provisional.
- Spelling similarity does not establish answer correctness.
- Large-vault performance and ambiguous matches are not yet evaluated.

## Hermes end-to-end demonstration

I copied the prototype to the Mac mini running Hermes Agent and ran all
nine tests successfully there.

From Telegram, I asked Hermes to invoke the script against fictional
notes. For `beacon`, it returned one source-backed candidate. For the
misspelled `latern`, it returned two notes with conflicting schedules
and marked the result `review_required`. Hermes reported both times
without asserting which one was current.

These demonstrations required an explicit command in the Telegram
request. Automatic invocation during normal Obsidian searches has not
been implemented.
## Walkthrough

[Watch the 88-second project walkthrough](demo/hermes_support_lab_walkthrough_compatible.mp4)

The video uses reconstructed panels from the Telegram transcript and fictional test notes.
