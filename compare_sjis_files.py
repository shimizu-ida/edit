import sys

file_to_check = "/app/test_sjis.txt"
expected_bytes_file = "/tmp/expected_sjis.bin"

try:
    with open(file_to_check, "rb") as f:
        actual_bytes = f.read()
except FileNotFoundError:
    print(f"Error: File '{file_to_check}' not found.")
    sys.exit(1)

try:
    with open(expected_bytes_file, "rb") as f:
        expected_bytes = f.read()
except FileNotFoundError:
    print(f"Error: File '{expected_bytes_file}' not found (run generate_expected_sjis_bytes.py first).")
    sys.exit(1)

if actual_bytes == expected_bytes:
    print(f"Success: Content of '{file_to_check}' matches expected Shift_JIS (CP932) bytes.")
else:
    print(f"Error: Content of '{file_to_check}' does not match expected Shift_JIS (CP932) bytes.")
    print(f"Expected (hex): {expected_bytes.hex()}")
    print(f"Actual (hex):   {actual_bytes.hex()}")
    sys.exit(1)
