# -*- coding: utf-8 -*-
import codecs
import sys

text_content = """これはShift_JISエンコーディングのテストファイルです。
ｶﾀｶﾅABCDEFG
┌─┐
│Ａ│
└─┘
"""

file_to_check = "test_sjis.txt" 

try:
    # Encode the reference text to Shift_JIS (CP932) to get expected bytes
    expected_bytes = text_content.encode('cp932')
except Exception as e:
    print(f"Error encoding reference text: {e}")
    sys.exit(1)

try:
    with open(file_to_check, "rb") as f:
        actual_bytes = f.read()
except FileNotFoundError:
    print(f"Error: File '{file_to_check}' not found.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file '{file_to_check}': {e}")
    sys.exit(1)

if actual_bytes == expected_bytes:
    print(f"Success: Content of '{file_to_check}' matches expected Shift_JIS (CP932) bytes.")
else:
    print(f"Error: Content of '{file_to_check}' does not match expected Shift_JIS (CP932) bytes.")
    # Limit the output for very long differing files for brevity in logs
    max_bytes_to_show = 200
    expected_hex = expected_bytes.hex()
    actual_hex = actual_bytes.hex()
    if len(expected_hex) > max_bytes_to_show * 2 or len(actual_hex) > max_bytes_to_show * 2 :
        print(f"Expected (hex, first {max_bytes_to_show} bytes): {expected_hex[:max_bytes_to_show*2]}...")
        print(f"Actual (hex, first {max_bytes_to_show} bytes):   {actual_hex[:max_bytes_to_show*2]}...")
    else:
        print(f"Expected (hex): {expected_hex}")
        print(f"Actual (hex):   {actual_hex}")
    sys.exit(1)
