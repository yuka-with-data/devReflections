""" Testing the journal module. """
import re
from datetime import datetime
from dev_reflections import journal
from dev_reflections.journal import JOURNAL_PROMPTS, choose_starter_prompt

def test_journal_prompts_contains_five_prompts():
    """Verify that all five expected starter prompts are available."""
    assert len(JOURNAL_PROMPTS) == 5
    assert "What did you learn today?" in JOURNAL_PROMPTS
    assert "What did you work on today?" in JOURNAL_PROMPTS
    assert "What challenged you today?" in JOURNAL_PROMPTS
    assert "What decision did you make, and why?" in JOURNAL_PROMPTS
    assert (
        "What are you curious about or want to explore next?"
        in JOURNAL_PROMPTS
    )


def test_choose_starter_prompt(monkeypatch):
    """Verify that choosing a number returns the matching prompt."""
    monkeypatch.setattr("builtins.input", lambda _: "2")

    assert choose_starter_prompt() == "What did you work on today?"


def test_choose_free_writing(monkeypatch):
    """Verify that choosing zero skips the starter prompt."""
    monkeypatch.setattr("builtins.input", lambda _: "0")

    assert choose_starter_prompt() is None


def test_choose_invalid_prompt(monkeypatch):
    """Verify that an invalid choice returns an empty string."""
    monkeypatch.setattr("builtins.input", lambda _: "9")

    assert choose_starter_prompt() == ""


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

def test_save_entry_includes_starter_prompt(tmp_path, monkeypatch):
    """Verify that a selected starter prompt is saved in Markdown."""
    monkeypatch.setattr(journal, "ENTRIES_DIR", tmp_path)

    starter_prompt = "What did I learn today?"
    path = journal.save_entry(
        "I learned pytest fixtures.",
        "What was most useful?",
        "The fixtures made testing easier.",
        starter_prompt=starter_prompt,
    )

    content = path.read_text(encoding="utf-8")

    assert "## Starter Prompt" in content
    assert starter_prompt in content


def test_save_entry_omits_starter_prompt_when_not_selected(
    tmp_path, monkeypatch
):
    """Verify that free-writing entries omit the starter prompt section."""
    monkeypatch.setattr(journal, "ENTRIES_DIR", tmp_path)

    path = journal.save_entry(
        "I wrote freely today.",
        "What stood out?",
        "I enjoyed exploring an idea.",
    )

    content = path.read_text(encoding="utf-8")

    assert "## Starter Prompt" not in content
    assert "## Journal Entry" in content
