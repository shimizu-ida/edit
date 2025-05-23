# -*- coding: utf-8 -*-
import codecs
import sys

text_content = """これはShift_JISエンコーディングのテストファイルです。
ｶﾀｶﾅABCDEFG
┌─┐
│Ａ│
└─┘
"""
file_path = "test_sjis.txt" # Write to current directory (should be /app/)

try:
    # Encode the text to Shift_JIS (CP932)
    encoded_bytes = text_content.encode('cp932')

    # Write the encoded bytes to a file in binary mode
    with open(file_path, "wb") as f:
        f.write(encoded_bytes)
    print(f"File '{file_path}' created successfully with Shift_JIS (CP932) encoding (direct binary write).")
except Exception as e:
    print(f"Error creating SJIS file '{file_path}': {e}", file=sys.stderr)
    sys.exit(1)
