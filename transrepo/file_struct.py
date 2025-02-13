import os
import json
import argparse

def get_file_structure(root_dir):
    def build_tree(dir_path):
        tree = {
            "name": os.path.basename(dir_path),
            "type": "folder",
            "children": []
        }

        for entry in os.listdir(dir_path):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                tree["children"].append(build_tree(full_path))
            else:
                tree["children"].append({
                    "name": entry,
                    "type": "file"
                })
        return tree
    
    return build_tree(root_dir)

def process_jsonl(input_jsonl, cache_dir, output_jsonl):
    suc_count = 0
    total_count = 0

    with open(input_jsonl, "r") as f:
        instances = [json.loads(line) for line in f]
    
    print(f"Total instances: {len(instances)}")

    for idx, instance in enumerate(instances, start=1):
        total_count += 1
        instance_id = instance.get("instance_id")
        instance_folder = os.path.join(cache_dir, instance_id)

        if os.path.exists(instance_folder) and os.path.isdir(instance_folder):
            file_struct = get_file_structure(instance_folder)
            instance["file_struct"] = file_struct
            suc_count += 1
        else:
            print(f"Warning: Folder for instance_id '{instance_id}' not found in {cache_dir}")

        if idx % 100 == 0:
            print(f"Processed {idx}/{len(instances)} instances...")

    with open(output_jsonl, "w") as outfile:
        for instance in instances:
            outfile.write(json.dumps(instance) + "\n")

    print(f"Processed {total_count} instances, successfully found {suc_count} folders.")

def main():
    parser = argparse.ArgumentParser(description="Process a JSONL file to add file structure information.")
    parser.add_argument("input_jsonl", help="Path to the input JSONL file")
    parser.add_argument("cache_dir", help="Directory containing cached Java project folders")
    parser.add_argument("output_jsonl", help="Path to save the output JSONL file with added file structure")

    args = parser.parse_args()

    process_jsonl(args.input_jsonl, args.cache_dir, args.output_jsonl)

if __name__ == "__main__":
    main()
