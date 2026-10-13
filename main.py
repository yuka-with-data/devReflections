""" Run the devReflections CLI journal workflow. """

from ollama import ResponseError

from dev_reflections.journal import generate_question, save_entry

def main():
    """ Collect a journal entry, ask a reflection question, and save the result. """
    print("Welcome to devReflections!\n")

    entry = input("What did you work on or learn today?\n").strip()
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
        file_path = save_entry(entry, question, answer)
        print(f"\nYour reflection has been saved to {file_path}.")
    except OSError as error:
        print(f"Could not save your entry: {error}")
        return

    print(f"\nSaved: {file_path}")
    print("Thank you for reflecting and growing.")

if __name__ == "__main__":
    main()
