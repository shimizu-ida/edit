# -*- coding: utf-8 -*-
import codecs

# テスト1 ステップ3で期待されるUTF-8文字列
expected_utf8_content = """これはShift_JISエンコーディングのテストファイルです。
ｶﾀｶﾅABCDEFG
┌─┐
│Ａ│
└─┘
編集テスト。
""" # Pythonの文字列リテラルは\nをLFとして扱う

file_path = "test_sjis_saved_as_utf8.txt"

try:
    # UTF-8 (BOMなし) で保存
    with open(file_path, "w", encoding="utf-8", newline='\n') as f: # newline='\n' を指定
        f.write(expected_utf8_content)
    print(f"File '{file_path}' created successfully with UTF-8 encoding (expected final content).")
except Exception as e:
    print(f"Error creating file '{file_path}': {e}")
    import sys
    sys.exit(1)
