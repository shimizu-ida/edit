# -*- coding: utf-8 -*-
import sys

original_content = "BOMなしUTF-8テスト。\n"
edited_suffix = "編集。\n"
final_content = original_content + edited_suffix

file_path_original = "test_utf8_nobom.txt"
file_path_edited = "test_utf8_nobom_edited.txt"

try:
    # Create original UTF-8 no BOM file
    with open(file_path_original, "w", encoding="utf-8", newline='\n') as f:
        f.write(original_content)
    print(f"File '{file_path_original}' created successfully.")

    # Simulate editing and saving
    # TextBuffer would save as UTF-8 (no BOM) by default if override is None
    with open(file_path_edited, "w", encoding="utf-8", newline='\n') as f:
        f.write(final_content)
    print(f"File '{file_path_edited}' created successfully (simulated edit and save).")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
