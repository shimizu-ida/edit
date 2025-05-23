# Grapheme Table Generator
# 書記素テーブルジェネレータ

This tool processes Unicode Character Database (UCD) XML files to generate efficient, multi-stage trie lookup tables for properties relevant to terminal applications:
このツールは、Unicode文字データベース（UCD）XMLファイルを処理して、ターミナルアプリケーションに関連するプロパティのための効率的な多段トライルックアップテーブルを生成します。
* Grapheme cluster breaking rules
* 書記素クラスタ分割ルール
* Line breaking rules (optional)
* 改行ルール（オプション）
* Character width properties
* 文字幅プロパティ

## Usage
## 使用法

* Download [ucd.nounihan.grouped.zip](https://www.unicode.org/Public/UCD/latest/ucdxml/ucd.nounihan.grouped.zip)
* [ucd.nounihan.grouped.zip](https://www.unicode.org/Public/UCD/latest/ucdxml/ucd.nounihan.grouped.zip) をダウンロードします。
* Run some equivalent of:
* 次のようなコマンドを実行します:
  ```sh
  grapheme-table-gen --lang=rust --extended --no-ambiguous --line-breaks path/to/ucd.nounihan.grouped.xml
  ```
* Place the result in `src/unicode/tables.rs`
* 結果を `src/unicode/tables.rs` に配置します。
