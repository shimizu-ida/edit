import codecs
import sys

hex_string = "82b182ea82cd53686966745f4a4953834783938352815b836683428393834f82cc836583588367837483408343838b82c582b781420ab6c0b6c5414243444546470a84a1849f84a20a84a0826084a00a84a4849f84a30a"
file_path = "test_sjis.txt" # No /app/ prefix

try:
    sjis_bytes = bytes.fromhex(hex_string)
    with open(file_path, "wb") as f:
        f.write(sjis_bytes)
    print(f"File '{file_path}' created successfully from hex string.")
except ValueError as e:
    print(f"Error decoding hex string: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error writing file '{file_path}': {e}")
    sys.exit(1)
