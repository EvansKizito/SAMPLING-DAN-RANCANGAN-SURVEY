import pandas as pd
import argparse


def clean(input_path: str, output_path: str, subset=None) -> None:
    """Remove duplicate rows from a CSV file and save the result.

    Parameters
    ----------
    input_path : str
        Path to the original CSV file.
    output_path : str
        Path where the deduplicated CSV will be written.
    subset : list[str] or None
        Column names to consider when identifying duplicates. If ``None`` the
        entire row is compared.
    """
    df = pd.read_csv(input_path)

    before = len(df)
    df.drop_duplicates(subset=subset, inplace=True)
    after = len(df)
    df.to_csv(output_path, index=False)

    removed = before - after
    print(f"Removed {removed} duplicate row{'s' if removed != 1 else ''}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove duplicate rows from a CSV")
    parser.add_argument("input", help="Path to the original CSV")
    parser.add_argument("output", help="Path for the deduplicated CSV")
    parser.add_argument(
        "--subset",
        help="Comma-separated column names to identify duplicates. If omitted, the entire row is used.",
    )
    args = parser.parse_args()

    subset = [s.strip() for s in args.subset.split(",")] if args.subset else None
    clean(args.input, args.output, subset=subset)


if __name__ == "__main__":
    main()
