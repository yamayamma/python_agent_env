"""CLI entrypoint."""

from . import greet


def main() -> None:
    """Run a simple CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="Greeting CLI")
    parser.add_argument("name", help="Name to greet")
    args = parser.parse_args()

    print(greet(args.name))


if __name__ == "__main__":
    main()
