import json
import os
from pathlib import Path

def split_featurecollection(input_dir: str, output_dir: str):
    """
    Splits all FeatureCollection GeoJSON files in an input directory 
    into individual Feature GeoJSON files in an output directory.

    Args:
        input_dir: Path to the folder containing the input GeoJSON files.
        output_dir: Path to the folder where the split files will be saved.
    """
    # Convert string paths to Path objects for robust handling
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create the output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Ensuring output directory exists: {output_path}")

    # Process all files with a .json or .geojson extension in the input directory
    geojson_files = list(input_path.glob('*.json')) + list(input_path.glob('*.geojson'))
    
    if not geojson_files:
        print(f"No GeoJSON files found in {input_path}. Exiting.")
        return

    print(f"Found {len(geojson_files)} potential GeoJSON files to process.")

    for file_path in geojson_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if it's a FeatureCollection
            if data.get('type') == 'FeatureCollection' and 'features' in data:
                
                features = data['features']
                num_features = len(features)
                print(f"\nProcessing FeatureCollection: {file_path.name} with {num_features} features.")
                
                # Get the base name without extension (e.g., '1' from '1.json')
                base_name = file_path.stem
                
                # Iterate through features and save each one
                for i, feature in enumerate(features):
                    # Create the new file name (e.g., '1-0.json', '1-1.json')
                    new_file_name = f"{base_name}-{i}.json"
                    new_file_path = output_path / new_file_name
                    
                    # Write the single feature to the new file
                    with open(new_file_path, 'w', encoding='utf-8') as outfile:
                        json.dump(feature, outfile, indent=2) # Use indent=2 for readability

                    print(f"  -> Saved feature {i} to {new_file_name}")

            else:
                print(f"Skipping file {file_path.name}: Not a FeatureCollection or missing 'features'.")

        except json.JSONDecodeError:
            print(f"Error reading {file_path.name}: File is not valid JSON. Skipping.")
        except Exception as e:
            print(f"An unexpected error occurred with {file_path.name}: {e}")

# ----------------------------------------------------------------------
# --- SCRIPT EXECUTION SETUP ---
# ----------------------------------------------------------------------

# --- ⚠️ USER CONFIGURATION REQUIRED ⚠️ ---
# 1. Specify the folder containing your GeoJSON FeatureCollection files.
INPUT_FOLDER = 'shukran_test/loc_1/cells/cells' 
# 2. Specify the folder where the individual feature files will be saved.
OUTPUT_FOLDER = 'cell' 
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Ensure the input directory exists for the script to run
    if not Path(INPUT_FOLDER).is_dir():
        print(f"Input directory '{INPUT_FOLDER}' not found. Please create it and place your GeoJSON files inside.")
    else:
        split_featurecollection(INPUT_FOLDER, OUTPUT_FOLDER)
        print("\n--- Script finished. ---")