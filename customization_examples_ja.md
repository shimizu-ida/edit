# カスタマイズ例

## はじめに (Introduction)

このエディタはシンプルさを重視して設計されており、多くのカスタマイズオプションは提供していません。より高度なカスタマイズの多くは、ソースコードを直接変更し、エディタを再コンパイルする必要があります。

しかし、いくつかの方法でエディタの基本的な動作や外観に影響を与えることができます。このドキュメントでは、それらの方法について説明します。

## 起動オプションによるカスタマイズ (Customization via Launch Options)

エディタの起動時にコマンドライン引数を使用することで、いくつかの動作を制御できます。

### 特定の行番号・桁番号でファイルを開く (Opening files at specific line/column numbers)

特定のファイルを開く際に、カーソル位置の行番号や桁番号を指定できます。これは `edit FILE[:LINE[:COLUMN]]` という形式の引数を使用します。

*   `FILE`: 開きたいファイルへのパス。
*   `LINE` (オプション): 開いたときにカーソルを配置する行番号。
*   `COLUMN` (オプション): 開いたときにカーソルを配置する桁番号。

**例:**

```bash
edit myfile.txt:10:5
```

このコマンドは `myfile.txt` を開き、カーソルを10行目の5桁目に配置します。

### 標準入力からの読み込み (Reading from Standard Input)

他のコマンドの出力をエディタに直接読み込ませることができます。これには `edit -` コマンドを使用します。

**例:**

```bash
cat myfile.txt | edit -
```

このコマンドは `cat myfile.txt` の内容を標準入力経由でエディタに渡し、新しい無題のドキュメントとして開きます。

## ターミナルのテーマ設定 (Terminal Theme Settings)

エディタは、起動時に使用しているターミナルエミュレータの基本的な色の設定（背景色、前景色、ANSIカラーなど）を検出し、それをUIに反映しようとします。

したがって、エディタの見た目を変更する主な方法は、お使いのターミナルエミュレータのテーマ設定を変更することです。

*   **Windows Terminal**: 「設定」 > 「配色」からテーマを編集または新しいテーマを作成できます。
*   **GNOME Terminal**: 「設定」 > 「プロファイル」 > （選択中のプロファイル） > 「色」タブから色を調整できます。
*   **iTerm2 (macOS)**: 「Preferences」 > 「Profiles」 > 「Colors」タブでカラープリセットを選択したり、個別の色をカスタマイズしたりできます。

具体的な手順はターミナルエミュレータによって異なりますが、通常は設定メニュー内にテーマや色のカスタマイズオプションがあります。

## 高度なカスタマイズ (ソースコードの変更) (Advanced Customization - Modifying Source Code)

**注意:** ここで説明する変更は、Rustプログラミング言語の知識があり、エディタを自身でソースコードから再コンパイルできるユーザー向けです。

より詳細なカスタマイズを行いたい場合は、ソースコードを直接変更し、エディタを再コンパイルする必要があります。

### キーボードショートカットの変更 (Modifying Keyboard Shortcuts)

キーボードショートカットは、主に `src/bin/edit/main.rs` ファイル内の `draw` 関数で処理されています。この関数内には、特定のキー入力（例: `kbmod::CTRL | vk::N` でCtrl+N）に応じて特定のアクションを呼び出すロジックが含まれています。

この部分のコードを変更し、エディタを再コンパイルすることで、キーボードショートカットをカスタマイズできます。

**例: 新規ファイル作成のショートカットを `Ctrl+N` から `Ctrl+Shift+N` に変更する**

```rust
// src/bin/edit/main.rs の draw 関数内

// 変更前 (Ctrl+N で新規ファイル)
// if key == kbmod::CTRL | vk::N {
//     draw_add_untitled_document(ctx, state);
// }

// 変更後 (Ctrl+Shift+N で新規ファイル)
if key == kbmod::CTRL_SHIFT | vk::N { // kbmod::CTRL を kbmod::CTRL_SHIFT に変更
    draw_add_untitled_document(ctx, state);
}
```

変更後、プロジェクトのルートディレクトリで `cargo build --release` を実行してエディタを再コンパイルする必要があります。

### UIカラーの変更 (Modifying UI Colors)

エディタの一部のUI要素の色（メニューバーの背景色、フローティングウィンドウの背景色など）は、ソースコード内で定義されています。これらの値を変更することで、UIの配色をカスタマイズできます。

色の設定は、主に `src/bin/edit/main.rs` ファイル内の `run` 関数で行われています。例えば、`state.menubar_color_bg` や `floater_bg` といった変数に色が割り当てられています。

**例: メニューバーの背景色を青系から赤系に変更する**

```rust
// src/bin/edit/main.rs の run 関数内

// 変更前 (メニューバーの背景に青系の色を使用)
// state.menubar_color_bg = oklab_blend(
//     tui.indexed(IndexedColor::Background),
//     tui.indexed_alpha(IndexedColor::BrightBlue, 1, 2), // この行の BrightBlue
// );

// 変更後 (メニューバーの背景に赤系の色を使用)
state.menubar_color_bg = oklab_blend(
    tui.indexed(IndexedColor::Background),
    tui.indexed_alpha(IndexedColor::BrightRed, 1, 2), // BrightBlue を BrightRed に変更
);
```

`IndexedColor` enum (`src/framebuffer.rs` で定義) には、他の基本色も定義されています。これらの値を試すことで、異なる配色に変更できます。

変更後は、同様に `cargo build --release` を実行してエディタを再コンパイルしてください。

### 再コンパイルの手順

ソースコードを変更した後は、プロジェクトのルートディレクトリで以下のコマンドを実行してエディタを再コンパイルします。

```bash
cargo build --release
```

コンパイルが成功すると、`target/release/` ディレクトリ内に新しい `edit` バイナリが生成されます。

## まとめ (Conclusion)

このエディタは設定ファイルによる詳細なカスタマイズ機能は持っていませんが、起動オプションやターミナルのテーマ設定、そして上級者向けにはソースコードの変更を通じて、ある程度の動作や外観の調整が可能です。

さらなる詳細な情報や、プロジェクトへの貢献に興味がある場合は、`CONTRIBUTING.md` も参照してください。
