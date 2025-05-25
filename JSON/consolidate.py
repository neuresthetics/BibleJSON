import os
import json
from pathlib import Path

def consolidate_json_files(root_dir):
    # Initialize list to store all JSON data
    consolidated_data = []
    json_file_count = 0
    entry_count = 0
    
    print(f"Starting JSON consolidation in root directory: {root_dir}")
    
    # Get list of subfolders in root directory
    root_path = Path(root_dir)
    subfolders = [f for f in root_path.iterdir() if f.is_dir()]
    
    if not subfolders:
        print("No subfolders found in root directory.")
        return
    
    print(f"Found {len(subfolders)} subfolders: {[f.name for f in subfolders]}")
    
    # Process each subfolder
    for folder in subfolders:
        book_name = folder.name
        print(f"\nProcessing subfolder: {book_name}")
        
        # Find all JSON files in the subfolder
        json_files = list(folder.glob("*.json"))
        
        if not json_files:
            print(f"No JSON files found in {book_name}")
            continue
        
        print(f"Found {len(json_files)} JSON files in {book_name}: {[f.name for f in json_files]}")
        
        # Process each JSON file
        for json_file in json_files:
            print(f"Processing file: {json_file}")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    json_file_count += 1
                    # Add book field to indicate source folder
                    if isinstance(data, dict):
                        data['book'] = book_name
                        consolidated_data.append(data)
                        entry_count += 1
                        print(f"Added 1 entry from {json_file}")
                    elif isinstance(data, list):
                        # If JSON contains a list, add book field to each item
                        for item in data:
                            if isinstance(item, dict):
                                item['book'] = book_name
                                consolidated_data.append(item)
                                entry_count += 1
                            else:
                                print(f"Warning: Skipping non-dict item in {json_file}")
                        print(f"Added {len(data)} entries from {json_file}")
                    else:
                        print(f"Warning: Skipping invalid JSON structure in {json_file}")
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse JSON in {json_file}: {str(e)}")
            except UnicodeDecodeError as e:
                print(f"Error: Encoding issue in {json_file}: {str(e)}")
            except Exception as e:
                print(f"Error processing {json_file}: {str(e)}")
    
    # Write consolidated data to output file
    output_file = root_path / "consolidated.json"
    print(f"\nProcessed {json_file_count} JSON files with {entry_count} entries total")
    
    if not consolidated_data:
        print("No data to write to output file (empty consolidated data)")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2)
        print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"Error writing output file: {str(e)}")

if __name__ == "__main__":
    # Use current directory as root
    root_directory = "."
    consolidate_json_files(root_directory)