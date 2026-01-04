# import json
# import os

# def merge_datasets():
#     # Define file paths
#     # Using absolute paths based on the context provided or relative to the workspace root if run from root
#     # Adjusting to use relative paths for flexibility assuming the script is run from project root or subfolder
    
#     # Base paths
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     dataset_dir = os.path.join(base_dir, "datasets")
#     synthetic_dir = os.path.join(base_dir, "synthetic_datasets")
    
#     file1_path = os.path.join(dataset_dir, "lengthen.jsonl")
#     file2_path = os.path.join(synthetic_dir, "synthetic_length.jsonl")
#     output_path = os.path.join(dataset_dir, "mix_lengthen.jsonl")

#     print(f"Reading from: {file1_path}")
#     print(f"Reading from: {file2_path}")
#     print(f"Writing to: {output_path}")

#     all_data = []
#     last_id = 0

#     # Read first file
#     try:
#         with open(file1_path, 'r', encoding='utf-8') as f1:
#             for line in f1:
#                 if line.strip():
#                     data = json.loads(line)
#                     if data is None:
#                         continue
#                     all_data.append(data)
#                     if data.get('id') is not None:
#                         last_id = max(last_id, data['id'])
#     except FileNotFoundError:
#         print(f"Error: Could not find {file1_path}")
#         return

#     print(f"Loaded {len(all_data)} records from first file. Last ID: {last_id}")

#     # Read second file and update IDs
#     count_second_file = 0
#     try:
#         with open(file2_path, 'r', encoding='utf-8') as f2:
#             for line in f2:
#                 if line.strip():
#                     data = json.loads(line)
#                     if data is None:
#                         continue
#                     # Update ID
#                     last_id += 1
#                     data['id'] = last_id
#                     all_data.append(data)
#                     count_second_file += 1
#     except FileNotFoundError:
#         print(f"Error: Could not find {file2_path}")
#         return

#     print(f"Loaded and updated {count_second_file} records from second file.")
#     print(f"Total records to write: {len(all_data)}")

#     # Write to output file
#     with open(output_path, 'w', encoding='utf-8') as f_out:
#         for entry in all_data:
#             f_out.write(json.dumps(entry) + '\n')

#     print("Success! Mix dataset created.")

# if __name__ == "__main__":
#     merge_datasets()
import json
import os

def merge_datasets():
    # --- 1. SETUP PATHS ---
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(base_dir, "datasets")
    synthetic_dir = os.path.join(base_dir, "synthetic_datasets")
    
    file1_path = os.path.join(dataset_dir, "lengthen.jsonl")
    file2_path = os.path.join(synthetic_dir, "synthetic_length.jsonl")
    output_path = os.path.join(dataset_dir, "mix_lengthen.jsonl")

    print(f"Reading from: {file1_path}")
    print(f"Reading from: {file2_path}")
    print(f"Writing to: {output_path}")

    all_data = []
    last_id = 0

    # --- 2. PROCESS FILE 1 (Source Data) ---
    try:
        with open(file1_path, 'r', encoding='utf-8') as f1:
            for line in f1:
                if line.strip():
                    try:
                        data = json.loads(line)
                        
                        # Handle NULLs in first file if any exist
                        if data is None:
                            data = {
                                "id": 0, # Will be updated if logic requires, but usually file 1 has IDs
                                "sender": "recovered.entry@system.com",
                                "subject": "Recovered Entry",
                                "content": "[Content recovered from null line]"
                            }

                        all_data.append(data)
                        
                        # Track the highest ID found so far
                        if data.get('id') is not None:
                            last_id = max(last_id, data['id'])
                            
                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON in file 1.")
    except FileNotFoundError:
        print(f"Error: Could not find {file1_path}")
        return

    print(f"Loaded {len(all_data)} records from first file. Last ID: {last_id}")

    # --- 3. PROCESS FILE 2 (Synthetic Data - The one with NULLs) ---
    count_second_file = 0
    try:
        with open(file2_path, 'r', encoding='utf-8') as f2:
            for line in f2:
                if line.strip():
                    try:
                        data = json.loads(line)

                        # *** THE FIX: Handle NULL values ***
                        if data is None:
                            print(" -> Found a NULL record. Replacing with placeholder.")
                            data = {
                                "sender": "unknown@placeholder.com",
                                "subject": "Data Error Placeholder",
                                "content": "This row was originally null in the source dataset."
                            }

                        # Update ID sequence
                        last_id += 1
                        data['id'] = last_id
                        
                        all_data.append(data)
                        count_second_file += 1
                        
                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON in file 2.")
    except FileNotFoundError:
        print(f"Error: Could not find {file2_path}")
        return

    print(f"Loaded and updated {count_second_file} records from second file.")
    print(f"Total records to write: {len(all_data)}")

    # --- 4. WRITE OUTPUT ---
    with open(output_path, 'w', encoding='utf-8') as f_out:
        for entry in all_data:
            f_out.write(json.dumps(entry) + '\n')

    print("Success! Mix dataset created.")

if __name__ == "__main__":
    merge_datasets()