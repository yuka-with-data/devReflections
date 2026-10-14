"""
Generate reflection questions with Ollama and save journal entries as Markdown.
"""

from datetime import datetime
from pathlib import Path

import ollama

# Resolve paths from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROMPT_PATH = PROJECT_ROOT / "prompts" / "reflection_system.txt"
ENTRIES_DIR = PROJECT_ROOT / "entries"

# Set this to your preferred model name from `ollama list`.
MODEL = "gemma4:e4b"

# Optional starter prompts for journal entries.
JOURNAL_PROMPTS = [
    "What did I learn today?",
    "What did I work on today?",
    "What challenged me today?",
    "What decision did I make, and why?",
    "What am I curious about or want to explore next?",
]

def choose_starter_prompt() -> str | None:
    """Let the user choose a starter prompt or write freely."""
    print("Choose a journal prompt:")
    for index, prompt in enumerate(JOURNAL_PROMPTS, start=1):
        print(f"{index}. {prompt}")
    print("0. Write freely")

    choice = input("\nYour choice (0-5): ").strip()

    if choice == "0":
        return None

    if choice.isdigit() and 1 <= int(choice) <= len(JOURNAL_PROMPTS):
        return JOURNAL_PROMPTS[int(choice) - 1]

    print("Invalid choice. Please run the program again and choose 0-5.")
    return ""

def load_system_prompt() -> str:
    """Load the system prompt from a text file."""
    if not PROMPT_PATH.is_file():
        raise FileNotFoundError(f"System prompt file not found: {PROMPT_PATH}")

    prompt = PROMPT_PATH.read_text(encoding="utf-8").strip()
    if not prompt:
        raise ValueError("System prompt file is empty")

    return prompt


def generate_question(entry: str) -> str:
    """Ask Ollama to generate one concise follow-up question."""
    if not entry.strip():
        raise ValueError("Entry cannot be empty or whitespace")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": load_system_prompt()},
            {"role": "user", "content": entry},
        ],
    )

    question = response.message.content.strip()
    if not question:
        raise ValueError("Ollama returned an empty question")

    return question


def save_entry(entry: str,
               question: str,
               answer: str,
               starter_prompt: str | None = None,
               ) -> Path:
    """Save the entry, AI question, and user's answer as a Markdown file."""
    timestamp = datetime.now().astimezone()
    year = timestamp.strftime("%Y")
    month = timestamp.strftime("%m")
    filename = timestamp.strftime("%Y-%m-%d_%H-%M-%S.md")
    file_path = ENTRIES_DIR / year / month / filename

    # Include the starter prompt only when the user selected one
    starter_section = ""
    if starter_prompt:
        starter_section = f"## Starter Prompt\n\n{starter_prompt.strip()}\n\n"

    content = f'''# Reflection - {timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")}

{starter_section}## Journal Entry

{entry.strip()}

## Reflection Question

{question.strip()}

## My Reflection

{answer.strip()}
'''

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    return file_path
