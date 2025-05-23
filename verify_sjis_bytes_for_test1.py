# -*- coding: utf-8 -*-
import sys

# This is the PREVIOUSLY AGREED UPON HEX STRING for test_sjis.txt
# If create_file_from_hex.py ran correctly, test_sjis.txt should match this.
EXPECTED_HEX_STRING = "82b182ea82cd53686966745f4a4953834783938352815b836683428393834f82cc836583588367837483408343838b82c582b781420ab6c0b6c5414243444546470a84a1849f84a20a84a0826084a00a84a4849f84a30a"
FILE_TO_CHECK = "test_sjis.txt"

try:
    with open(FILE_TO_CHECK, "rb") as f:
        actual_bytes = f.read()
    
    actual_hex_string = actual_bytes.hex()

    if actual_hex_string == EXPECTED_HEX_STRING:
        print(f"Success: Content of '{FILE_TO_CHECK}' matches the expected Shift_JIS (CP932) hex string.")
    else:
        print(f"Error: Content of '{FILE_TO_CHECK}' does not match the expected Shift_JIS (CP932) hex string.")
        # Limit the output for very long differing files for brevity in logs
        max_chars_to_show = 400 # Show more for debugging this specific issue
        print(f"Expected (hex, len={len(EXPECTED_HEX_STRING)}): {EXPECTED_HEX_STRING[:max_chars_to_show]}{'...' if len(EXPECTED_HEX_STRING) > max_chars_to_show else ''}")
        print(f"Actual (hex, len={len(actual_hex_string)}):   {actual_hex_string[:max_chars_to_show]}{'...' if len(actual_hex_string) > max_chars_to_show else ''}")
        # For easier diffing, print the full strings if they are not excessively long
        if len(EXPECTED_HEX_STRING) <= 2000 and len(actual_hex_string) <= 2000:
             print(f"Full Expected: {EXPECTED_HEX_STRING}")
             print(f"Full Actual:   {actual_hex_string}")
        sys.exit(1)

except FileNotFoundError:
    print(f"Error: File '{FILE_TO_CHECK}' not found. Please ensure 'create_file_from_hex.py' was run successfully.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
