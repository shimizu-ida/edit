# -*- coding: utf-8 -*-
import codecs

# テスト1 ステップ2で期待されるUTF-8文字列 (Shift_JISから変換されたもの)
original_sjis_text_as_utf8 = """これはShift_JISエンコーディングのテストファイルです。
ｶﾀｶﾅABCDEFG
┌─┐
│Ａ│
└─┘
"""

# テスト1 ステップ3で編集された内容
edited_text_as_utf8 = original_sjis_text_as_utf8 + "編集テスト。\n"

file_path = "test_sjis_saved_as_utf8.txt"

try:
    # TextBuffer::write_file(..., encoding_override=None) は UTF-8 (BOMなし) で保存する
    with open(file_path, "w", encoding="utf-8", newline='\n') as f:
        f.write(edited_text_as_utf8)
    print(f"File '{file_path}' created successfully with UTF-8 encoding.")
except Exception as e:
    print(f"Error creating file '{file_path}': {e}")
    import sys
    sys.exit(1)
