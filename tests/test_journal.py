""" Testing the journal module. """
import re
from datetime import datetime

from dev_reflections import journal

def test_save_entry_creates_markdown(tmp_path, monkeypatch):
    """ Test that save_entry creates a Markdown file with the correct content."""
    monkeypatch.setattr(journal, "ENTRIES_DIR", tmp_path)

    path = journal.save_entry(
        "Worked on documentation.",
        "What did you learn?",
        "I learned how to structure a README.",
    )

    now = datetime.now().astimezone()

    assert path.is_file()
    assert path.suffix == ".md"
    assert path.parent.name == now.strftime("%m")
    assert path.parent.parent.name == now.strftime("%Y")
    assert re.fullmatch(
        r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.md",
        path.name,
    )

def test_save_entry_contains_all_sections(tmp_path, monkeypatch):
    """ Test that the saved Markdown file contains all sections. """
    monkeypatch.setattr(journal, "ENTRIES_DIR", tmp_path)

    entry = "Worked on documentation."
    question = "What did you learn?"
    answer = "I learned how to structure a README."

    path = journal.save_entry(entry, question, answer)
    content = path.read_text(encoding="utf-8")

    assert '## Journal Entry' in content
    assert entry in content
    assert '## Reflection Question' in content
    assert question in content
    assert '## My Reflection' in content
    assert answer in content

def test_save_entry_strips_surrounding_whitespace(tmp_path, monkeypatch):
    """ Test that save_entry strips surrounding whitespace from the entry, question, and answer. """
    monkeypatch.setattr(journal, "ENTRIES_DIR", tmp_path)

    path = journal.save_entry(
        "  My journal entry.  ",
        "  What did I learn?  ",
        "  I learned something.  ",
    )

    content = path.read_text(encoding="utf-8")

    assert "My journal entry." in content
    assert "What did I learn?" in content
    assert "I learned something." in content
    assert "  My journal entry.  " not in content
