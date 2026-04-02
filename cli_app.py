from app import main
import logging

logger = logging.getLogger(__name__)


def interactive_shell():

    print("\nClio")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:

        query = input("Enter your query:\n> ").strip()

        if query.lower() in ["exit", "quit"]:
            print("\nExiting system...\n")
            break

        if query == "":
            print("Empty query. Try again.\n")
            continue

        print("\nRunning pipeline...\n")

        try:

            answer = main(query)

            print("\n" + "="*60)
            print("ANSWER")
            print("="*60)
            print(answer)
            print("="*60 + "\n")

        except Exception as e:

            logger.error(f"Pipeline error: {e}")
            print("Something went wrong.\n")


def main():
    interactive_shell()


if __name__ == "__main__":
    main()