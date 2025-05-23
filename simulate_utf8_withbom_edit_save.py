# -*- coding: utf-8 -*-
import codecs
import sys

original_content = "BOMありUTF-8テスト。\n"
edited_suffix = "編集。\n"
final_content_expected = original_content + edited_suffix

file_path_original_with_bom = "test_utf8_withbom.txt"
file_path_edited_no_bom = "test_utf8_withbom_edited.txt"

try:
    # Create original UTF-8 with BOM file
    with open(file_path_original_with_bom, "w", encoding="utf-8-sig", newline='\n') as f:
        f.write(original_content)
    print(f"File '{file_path_original_with_bom}' created successfully with UTF-8 BOM.")

    # Simulate editing and saving (TextBuffer saves as UTF-8 no BOM by default)
    with open(file_path_edited_no_bom, "w", encoding="utf-8", newline='\n') as f:
        f.write(final_content_expected)
    print(f"File '{file_path_edited_no_bom}' created successfully (simulated edit and save, no BOM).")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
