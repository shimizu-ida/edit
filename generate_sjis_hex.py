# -*- coding: utf-8 -*-
import codecs

text_content = """これはShift_JISエンコーディングのテストファイルです。
ｶﾀｶﾅABCDEFG
┌─┐
│Ａ│
└─┘
"""

# Encode the text to Shift_JIS (CP932)
expected_sjis_bytes = text_content.encode('cp932')

# Print the bytes as a hex string
print(expected_sjis_bytes.hex())
