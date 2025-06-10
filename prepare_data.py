import pandas as pd
import argparse
from pathlib import Path

def prepare(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    # drop duplicate rows
    df.drop_duplicates(inplace=True)

    # normalize timestamp
    if 'Timestamp' in df.columns:
        # convert to datetime using day-first format
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)

    course_col = 'Saya sudah pernah mengambil mata kuliah di bawah ini.'
    if course_col in df.columns:
        # split courses and create boolean columns
        courses = ['Fisika', 'Kimia', 'Biologi']
        for course in courses:
            df[f'Pernah_{course}'] = df[course_col].str.contains(course, na=False).astype(int)
        df.drop(columns=[course_col], inplace=True)

    df.to_csv(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare survey CSV for analysis")
    parser.add_argument("input", help="Path to raw CSV file")
    parser.add_argument("output", help="Path for cleaned CSV")
    args = parser.parse_args()
    prepare(args.input, args.output)

if __name__ == "__main__":
    main()
