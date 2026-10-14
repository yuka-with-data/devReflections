"""Run the devReflections CLI journaling workflow."""

from ollama import ResponseError

from dev_reflections.journal import (
    choose_starter_prompt,
    generate_question,
    save_entry,
)


def main():
    """Collect a journal entry, reflect with AI, and save the result."""
    print("Welcome to devReflections!\n")

    starter_prompt = choose_starter_prompt()
    if starter_prompt == "":
        return

    if starter_prompt:
        print(f"\nStarter prompt: {starter_prompt}")

    entry = input("\nWrite your journal entry:\n").strip()
    if not entry:
        print("Journal entry cannot be empty. Please try again.")
        return

    try:
        print("\nThinking...\n")
        question = generate_question(entry)
    except ResponseError as error:
        print(f"Could not generate a reflection question: {error}")
        return
    except ConnectionError:
        print("Could not connect to Ollama. Make sure Ollama is running.")
        return
    except (FileNotFoundError, ValueError) as error:
        print(f"An error occurred: {error}")
        return

    print(f"Reflection question: {question}\n")
    answer = input("Your answer:\n").strip()
    if not answer:
        print("Answer cannot be empty. Please try again.")
        return

    try:
        file_path = save_entry(
            entry,
            question,
            answer,
            starter_prompt=starter_prompt,
        )
        print(f"\nYour reflection has been saved to {file_path}.")
    except OSError as error:
        print(f"Could not save your entry: {error}")
        return

    print("Thank you for reflecting and growing.")


if __name__ == "__main__":
    main()
