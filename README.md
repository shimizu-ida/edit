# ![Application Icon for Edit](./assets/edit.svg) Edit

A simple editor for simple needs.
シンプルなニーズに応えるシンプルなエディタです。

This editor pays homage to the classic [MS-DOS Editor](https://en.wikipedia.org/wiki/MS-DOS_Editor), but with a modern interface and input controls similar to VS Code. The goal is to provide an accessible editor that even users largely unfamiliar with terminals can easily use.
このエディタは、クラシックな[MS-DOS Editor](https://en.wikipedia.org/wiki/MS-DOS_Editor)に敬意を表しつつ、VS Codeに似た最新のインターフェースと入力コントロールを備えています。目標は、ターミナルにあまり慣れていないユーザーでも簡単に使用できる、アクセシブルなエディタを提供することです。

![Screenshot of Edit with the About dialog in the foreground](./assets/edit_hero_image.png)

## Installation
## インストール

* Download the latest release from our [releases page](https://github.com/microsoft/edit/releases/latest)
* 最新リリースを[リリースパージ](https://github.com/microsoft/edit/releases/latest)からダウンロードします。
* Extract the archive
* アーカイブを展開します。
* Copy the `edit` binary to a directory in your `PATH`
* `edit`バイナリを`PATH`内のディレクトリにコピーします。
* You may delete any other files in the archive if you don't need them
* 必要なければ、アーカイブ内の他のファイルは削除してもかまいません。

### WinGet (Windows)
### WinGet (ウィンドウズ)

* Open up a terminal of your choice and run the following command:
* 任意のターミナルを開き、次のコマンドを実行します:
  ```powershell
  winget install Microsoft.Edit
  ```
* `edit` will be automatically added to your `PATH`. If typing `edit` doesn't work, open a new terminal.
* `edit`は自動的に`PATH`に追加されます。`edit`と入力しても動作しない場合は、新しいターミナルを開いてください。

## Build Instructions
## ビルド手順

* [Install Rust](https://www.rust-lang.org/tools/install)
* [Rustをインストールします](https://www.rust-lang.org/tools/install)
* Install the nightly toolchain: `rustup install nightly`
* nightlyツールチェーンをインストールします: `rustup install nightly`
  * Alternatively, set the environment variable `RUSTC_BOOTSTRAP=1`
  * または、環境変数 `RUSTC_BOOTSTRAP=1` を設定します。
* Clone the repository
* リポジトリをクローンします。
* For a release build, run: `cargo build --config .cargo/release.toml --release`
* リリースビルドの場合は、次のコマンドを実行します: `cargo build --config .cargo/release.toml --release`

## 文字エンコーディングの取り扱いについて

本エディタは、さまざまな文字エンコーディングのファイルを扱えるように設計されていますが、内部処理と保存時の挙動には以下の特徴があります。

### ファイル読み込み時のエンコーディング検出

ファイルを開く際、以下の順序で文字エンコーディングが判別されます。

1.  **BOM (Byte Order Mark) による判別**:
    *   ファイル先頭にBOMが存在する場合、BOMが示すエンコーディング（例: UTF-8 BOM, UTF-16LE, UTF-16BEなど）としてファイルを読み込みます。
2.  **BOMなしファイルの場合**:
    *   **UTF-8検証**: まず、ファイルがUTF-8エンコーディングとして有効かどうかが検証されます。有効なUTF-8であれば、UTF-8として読み込まれます。
    *   **Shift_JIS (CP932) 自動判別**: UTF-8として無効な場合、次にファイル内容がShift_JIS (CP932) である可能性が簡易的に検査されます。Shift_JIS特有のバイトパターンが多く見られるなど、Shift_JISの可能性が高いと判断された場合、ファイルはCP932として解釈され、内部的にUTF-8に変換されて読み込まれます。
        *   **注意**: この自動判別はヒューリスティック（経験則）に基づくものであり、100%の正確性を保証するものではありません。特定の短いファイルや、他の日本語エンコーディング（EUC-JPなど）との区別が難しい場合があります。
    *   **フォールバック (UTF-8として読み込み)**: 上記のいずれにも該当しない場合（BOMなし、無効なUTF-8、かつShift_JISの可能性も低いと判断された場合）、ファイルは最終的にUTF-8として読み込みが試みられます。この際、不正なUTF-8シーケンスはUnicodeの置換文字（U+FFFD �）に置き換えられます。

読み込まれたテキストは、エディタ内部では一貫してUTF-8として扱われます。

### ファイル保存時のエンコーディング

*   **デフォルトの保存エンコーディング**: ファイルを「上書き保存」する際（ユーザーが保存時にエンコーディングを明示的に指定しない場合）、ファイルは**常にUTF-8（BOMなし）**で保存されます。
*   これにより、例えばShift_JISとして読み込まれたファイルも、上書き保存するとUTF-8エンコーディングに変換されます。
*   将来的に「エンコーディングを指定して保存」のような機能が追加された場合は、その指定が優先される可能性があります。

### ステータスバーのエンコーディング表示

*   エディタ下部のステータスバーには、現在アクティブなファイルについて、読み込み時に判別された（またはユーザーによって再解釈された後の）文字エンコーディングが表示されます。
*   表示されるエンコーディング名は、ICUライブラリに基づいた標準的な名称となります（例: "UTF-8", "UTF-8 BOM", "CP932" など）。"CP932" は Shift_JIS を指す一般的なICU名です。

このエンコーディング処理により、多くの一般的なテキストファイルとの互換性を保ちつつ、内部処理およびデフォルト保存形式をUTF-8に統一することで、シンプルさと予測可能性を提供することを目指しています。

## コードリーディングのヒント

このセクションでは、プロジェクトのコードベースを理解しやすくするためのヒントを提供します。

### プロジェクト構造の概要

プロジェクトの主要なコードは `src` ディレクトリにあります。以下は主要なディレクトリとファイルの簡単な説明です。

*   `src/`: ライブラリクレートのルートです。コアとなるデータ構造やユーティリティが含まれます。
    *   `src/arena.rs`: カスタムアリーナアロケータの実装。メモリ管理の効率化を図ります。
    *   `src/buffer.rs`: テキストバッファのデータ構造と操作ロジック。
    *   `src/document.rs`: ドキュメントの表現と操作のためのトレイトと構造体。
    *   `src/sys/`: システム固有の対話（ターミナルI/Oなど）を扱います。プラットフォーム間の差異を吸収する役割があります。
    *   `src/tui.rs`: ターミナルユーザーインターフェース（TUI）の管理、レンダリング、入力処理。
    *   `src/vt.rs`: VT端末コマンドのパーサー。端末エミュレーションの基盤となります。
*   `src/bin/edit/`: メインのバイナリクレートです。
    *   `main.rs`: アプリケーションのエントリーポイント、メインループ、イベント処理、描画ロジックの起点。
    *   `draw_*.rs`: 各UIコンポーネント（メニューバー、ステータスバー、エディタ本体など）の描画ロジック。

### 主要コンポーネントの連携

*   **`src/bin/edit/main.rs`**: アプリケーションの心臓部です。ユーザー入力（キーボード、マウス）をイベントとして受け取り、状態を更新し、UIの再描画をトリガーします。
*   **`src/document.rs`** と **`src/buffer.rs`**: テキストデータの保持と変更を担当します。`document.rs` はドキュメント操作のための一般的なインターフェースを提供し、`buffer.rs` は具体的なテキストバッファの実装を提供します。
*   **`src/tui.rs`**: 端末上でのUI要素の配置、スタイリング、レンダリングを行います。また、低レベルの端末入力を解釈し、アプリケーションが理解できるイベントに変換します。
*   **`src/vt.rs`**: 端末からのエスケープシーケンスを解析し、意味のあるコマンドとして解釈します。これにより、カーソル位置の取得や色の変更などが可能になります。
*   **`src/sys/`**: OS固有の機能（ファイルの読み書き、端末モードの設定など）を抽象化し、他のモジュールがプラットフォームに依存しない形でこれらの機能を利用できるようにします。

### コードリーディングの進め方

1.  **`src/bin/edit/main.rs`**: まず `main` 関数と `run` 関数を読み、アプリケーションの全体的な構造とメインループを理解します。イベント処理と描画の呼び出し方に注目してください。
2.  **`src/tui.rs`**: 次に、TUIがどのように初期化され、入力イベントがどのように処理され、UIがどのようにレンダリングされるかを確認します。`Context` 構造体と `draw` 関数の役割が重要です。
3.  **`src/document.rs`** と **`src/buffer.rs`**: テキストがどのように格納され、変更されるかを理解するためにこれらのファイルを確認します。`ReadableDocument` および `WriteableDocument` トレイトがキーとなります。
4.  **`src/bin/edit/draw_*.rs`**: 特定のUIコンポーネント（例: `draw_editor.rs`、`draw_menubar.rs`）がどのように描画されるかを確認します。これにより、UIの具体的な実装方法がわかります。
5.  **`src/vt.rs`** と **`src/sys/`**: より低レベルな端末制御やシステムコールに興味がある場合は、これらのディレクトリのコードを読み進めてください。

この順序でコードを読んでいくことで、アプリケーションの主要な機能とコンポーネント間の連携を段階的に理解できるはずです。
