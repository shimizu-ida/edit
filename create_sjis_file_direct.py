# -*- coding: utf-8 -*-
import codecs

text_content = """これはShift_JISエンコーディングのテストファイルです。
ｶﾀｶﾅABCDEFG
┌─┐
│Ａ│
└─┘
"""

file_path = "test_sjis.txt" # No /app/ prefix

try:
    # Encode the text to Shift_JIS (CP932)
    encoded_bytes = text_content.encode('cp932')

    # Write the encoded bytes to a file in binary mode
    with open(file_path, "wb") as f:
        f.write(encoded_bytes)
    print(f"File '{file_path}' created successfully with Shift_JIS (CP932) encoding (binary write).")
except Exception as e:
    print(f"Error creating SJIS file: {e}")
    import sys
    sys.exit(1)
