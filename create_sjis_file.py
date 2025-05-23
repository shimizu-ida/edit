# -*- coding: utf-8 -*-
import codecs

text_content = """これはShift_JISエンコーディングのテストファイルです。
ｶﾀｶﾅABCDEFG
┌─┐
│Ａ│
└─┘
"""

# Encode the text to Shift_JIS (CP932)
# Python's 'shift_jis' codec often maps to 'cp932' which is a more complete superset.
encoded_bytes = text_content.encode('cp932')

# Write the encoded bytes to a file
file_path = "/app/test_sjis.txt"
with open(file_path, "wb") as f:
    f.write(encoded_bytes)

print(f"File '{file_path}' created successfully with Shift_JIS (CP932) encoding.")
