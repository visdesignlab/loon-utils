import pandas as pd
import argparse
import sys
import os

def add_column_to_parquet(input_file, output_file, column_name_to_add, column_value):
    """
    Reads a Parquet file, adds a specified column with a constant value to all rows, 
    and writes the result to a new Parquet file.
    
    Args:
        input_file (str): Path to the source Parquet file.
        output_file (str): Path for the new Parquet file.
        column_name_to_add (str): Name of the new column.
        column_value (str): The constant value to assign to all rows in the new column.
        
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    print(f"-> Reading file: {input_file}")
    
    # --- Input Validation ---
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        return False

    try:
        # 1. Read the Parquet file
        df = pd.read_parquet(input_file)
        
        # Check if the column already exists
        if column_name_to_add in df.columns:
            print(f"Warning: Column '{column_name_to_add}' already exists. The value will be overwritten.", file=sys.stderr)

        # 2. Add the new column with the constant value
        # Pandas uses broadcasting to assign the single value to all rows efficiently.
        df[column_name_to_add] = column_value

        # 3. Write the new Parquet file
        df.to_parquet(output_file, index=False) # index=False prevents writing the DataFrame index

        print(f"-> Column '{column_name_to_add}' successfully added with value '{column_value}'.")
        print(f"-> New file created at: {output_file}")
        
        # Optional: Print sizes for verification
        original_size = os.path.getsize(input_file) / (1024 * 1024)
        new_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"-> Size comparison: Original={original_size:.2f}MB, New={new_size:.2f}MB")
        
        return True

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A CLI tool to add a new column with a constant value to a Parquet file."
    )
    
    # Positional arguments for required inputs
    parser.add_argument(
        "input_file", 
        help="The path to the source Parquet file (e.g., data.parquet)"
    )
    parser.add_argument(
        "column_name_to_add", 
        help="The name of the new column to add (e.g., 'source_tag')"
    )
    parser.add_argument(
        "column_value", 
        help="The constant value to assign to every row in the new column (e.g., 'Processed_V2')"
    )
    
    # Optional argument for output file
    parser.add_argument(
        "-o", "--output", 
        dest="output_file", 
        default="modified.parquet",
        help="The path for the new Parquet file (default: modified.parquet)"
    )
    
    args = parser.parse_args()
    
    success = add_column_to_parquet(
        args.input_file, 
        args.output_file, 
        args.column_name_to_add,
        args.column_value
    )

    if not success:
        sys.exit(1)
