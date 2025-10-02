Write a Python script called `excel-converter.py` that take the excel files located in the same folder and convert them to csv files.

on-adk-training(.venv) > uv run 04_agent\agent.py
Chat iniziata. Scrivi 'bye', 'quit' o 'exit' per terminare.
Prompt: Write a Python script called `excel-converter.py` that take the excel files located in the same folder and convert them to csv files.
Gemini: ```python
import pandas as pd
import pathlib
import os

def convert_excel_to_csv():
    """
    Finds all Excel files (.xls, .xlsx) in the current directory
    and converts them to CSV files. Each Excel file's first sheet
    will be converted to a single CSV file, named
    'original_filename.csv'.
    """
    current_directory = pathlib.Path('.')

    excel_files = []
    # Find all Excel files in the current directory
    for file_path in current_directory.iterdir():
        # Check for both .xls and .xlsx extensions, case-insensitively
        if file_path.suffix.lower() in ['.xls', '.xlsx']:
            excel_files.append(file_path)

    if not excel_files:
        print("No Excel files (.xls or .xlsx) found in the current directory.")
        return

    print(f"Found {len(excel_files)} Excel file(s). Starting conversion...")

    for excel_file in excel_files:
        print(f"\nProcessing '{excel_file.name}'...")
        try:
            # Read the Excel file. By default, pandas reads the first sheet.
            df = pd.read_excel(excel_file)

            # Create the CSV filename: original_filename_without_extension.csv
            csv_filename = f"{excel_file.stem}.csv"
            csv_path = current_directory / csv_filename

            # Save the DataFrame to a CSV file.
            # index=False prevents pandas from writing the DataFrame index as a column.
            # encoding='utf-8' is a good default for wide character support.
            df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"  Successfully converted '{excel_file.name}' to '{csv_path.name}'")

        except FileNotFoundError:
            print(f"  Error: Excel file '{excel_file.name}' not found. Skipping.")
        except pd.errors.EmptyDataError:
            print(f"  Error: Excel file '{excel_file.name}' is empty or malformed. Skipping.")
        except Exception as e:
            # Catch any other unexpected errors during conversion
            print(f"  An unexpected error occurred while converting '{excel_file.name}': {e}")
            print(f"  Skipping '{excel_file.name}'.")

if __name__ == "__main__":
    convert_excel_to_csv()
```

*   No major issues found.

```python
import pandas as pd
import pathlib
import os

def convert_excel_to_csv():
    """
    Finds all Excel files (.xls, .xlsx) in the current directory
    and converts them to CSV files. Each Excel file's first sheet
    will be converted to a single CSV file, named
    'original_filename.csv'.
    """
    current_directory = pathlib.Path('.')

    excel_files = []
    # Find all Excel files in the current directory
    for file_path in current_directory.iterdir():
        # Check for both .xls and .xlsx extensions, case-insensitively
        if file_path.suffix.lower() in ['.xls', '.xlsx']:
            excel_files.append(file_path)

    if not excel_files:
        print("No Excel files (.xls or .xlsx) found in the current directory.")
        return

    print(f"Found {len(excel_files)} Excel file(s). Starting conversion...")

    for excel_file in excel_files:
        print(f"\nProcessing '{excel_file.name}'...")
        try:
            # Read the Excel file. By default, pandas reads the first sheet.
            df = pd.read_excel(excel_file)

            # Create the CSV filename: original_filename_without_extension.csv
            csv_filename = f"{excel_file.stem}.csv"
            csv_path = current_directory / csv_filename

            # Save the DataFrame to a CSV file.
            # index=False prevents pandas from writing the DataFrame index as a column.
            # encoding='utf-8' is a good default for wide character support.
            df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"  Successfully converted '{excel_file.name}' to '{csv_path.name}'")

        except FileNotFoundError:
            print(f"  Error: Excel file '{excel_file.name}' not found. Skipping.")
        except pd.errors.EmptyDataError:
            print(f"  Error: Excel file '{excel_file.name}' is empty or malformed. Skipping.")
        except Exception as e:
            # Catch any other unexpected errors during conversion
            print(f"  An unexpected error occurred while converting '{excel_file.name}': {e}")
            print(f"  Skipping '{excel_file.name}'.")

if __name__ == "__main__":
    convert_excel_to_csv()
```