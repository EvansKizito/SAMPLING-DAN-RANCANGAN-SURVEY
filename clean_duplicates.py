import argparse
import pandas as pd


def remove_duplicates(input_path: str, output_path: str) -> None:
    """Read CSV, drop duplicate rows, and save to output."""
    df = pd.read_csv(input_path)
    df.drop_duplicates(inplace=True)
    df.to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser(description="Remove duplicate rows from a CSV file.")
    parser.add_argument("input", help="Path to the input CSV file")
    parser.add_argument("output", help="Path to save the cleaned CSV file")
    args = parser.parse_args()

    remove_duplicates(args.input, args.output)


if __name__ == "__main__":
    main()
