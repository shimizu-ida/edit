# Contributing
# 貢献

## Translation improvements
## 翻訳の改善

You can find our translations in [`src/bin/edit/localization.rs`](./src/bin/edit/localization.rs).
翻訳は [`src/bin/edit/localization.rs`](./src/bin/edit/localization.rs) にあります。
Please feel free to open a pull request with your changes at any time.
いつでも変更内容を含むプルリクエストを自由にオープンしてください。
If you'd like to discuss your changes first, please feel free to open an issue.
最初に変更内容について話し合いたい場合は、遠慮なくissueをオープンしてください。

## Bug reports
## バグ報告

If you find any bugs, we gladly accept pull requests without prior discussion.
バグを見つけた場合は、事前の話し合いなしにプルリクエストを喜んで受け付けます。
Otherwise, you can of course always open an issue for us to look into.
それ以外の場合は、もちろんいつでも調査のためのissueをオープンすることができます。

## Feature requests
## 機能リクエスト

Please open a new issue for any feature requests you have in mind.
ご希望の機能リクエストについては、新しいissueをオープンしてください。
Keeping the binary size of the editor small is a priority for us and so we may need to discuss any new features first until we have support for plugins.
エディタのバイナリサイズを小さく保つことが私たちの優先事項であるため、プラグインのサポートが得られるまでは、新しい機能について最初に話し合う必要があるかもしれません。

## Code changes
## コード変更

The project has a focus on a small binary size and sufficient (good) performance.
このプロジェクトは、小さなバイナリサイズと十分な（良好な）パフォーマンスに重点を置いています。
As such, we generally do not accept pull requests that introduce dependencies (there are always exceptions of course).
そのため、通常、依存関係を導入するプルリクエストは受け付けません（もちろん常に例外はあります）。
Otherwise, you can consider this project a playground for trying out any cool ideas you have.
それ以外の場合は、このプロジェクトを、あなたが持っているクールなアイデアを試すための遊び場と考えることができます。

The overall architecture of the project can be summarized as follows:
プロジェクト全体のアーキテクチャは次のように要約できます。
* The underlying text buffer in `src/buffer` doesn't keep track of line breaks in the document.
* `src/buffer` の基盤となるテキストバッファは、ドキュメント内の改行を追跡しません。
  This is a crucial design aspect that permeates throughout the entire codebase.
  これは、コードベース全体に浸透している重要な設計上の側面です。

  To oversimplify, the *only* state that is kept is the current cursor position.
  簡単に言うと、保持される *唯一の* 状態は現在のカーソル位置です。
  When the user asks to move to another line, the editor will `O(n)` seek through the underlying document until it found the corresponding number of line breaks.
  ユーザーが別の行への移動を要求すると、エディタは対応する数の改行が見つかるまで、基盤となるドキュメントを `O(n)` でシークします。
  * As a result, `src/simd` contains crucial `memchr2` functions to quickly find the next or previous line break (runs at up to >100GB/s).
  * その結果、`src/simd` には、次のまたは前の改行をすばやく見つけるための重要な `memchr2` 関数が含まれています（最大 >100GB/s で実行）。
  * Furthermore, `src/unicode` implements an `Utf8Chars` iterator which transparently inserts U+FFFD replacements during iteration (runs at up to 4GB/s).
  * さらに、`src/unicode` は、反復中に透過的にU+FFFD置換を挿入する `Utf8Chars` イテレータを実装しています（最大 4GB/s で実行）。
  * Furthermore, `src/unicode` also implements grapheme cluster segmentation and cluster width measurement via its `MeasurementConfig` (runs at up to 600MB/s).
  * さらに、`src/unicode` は、`MeasurementConfig` を介して書記素クラスタのセグメンテーションとクラスタ幅の測定も実装しています（最大 600MB/s で実行）。
  * If word wrap is disabled, `memchr2` is used for all navigation across lines, allowing us to breeze through 1GB large files as if they were 1MB.
  * ワードラップが無効になっている場合、行間のすべてのナビゲーションに `memchr2` が使用され、1GBの大きなファイルでも1MBであるかのように簡単に処理できます。
  * Even if word-wrap is enabled, it's still sufficiently smooth thanks to `MeasurementConfig`. This is only possible because these base functions are heavily optimized.
  * ワードラップが有効になっている場合でも、`MeasurementConfig` のおかげで十分にスムーズです。これは、これらの基本関数が高度に最適化されている場合にのみ可能です。
* `src/framebuffer.rs` implements a "framebuffer" like in video games.
* `src/framebuffer.rs` は、ビデオゲームのような「フレームバッファ」を実装しています。
  It allows us to draw the UI output into an intermediate buffer first, accumulating all changes and handling things like color blending.
  これにより、UI出力を最初に中間バッファに描画し、すべての変更を蓄積し、カラーブレンディングなどを処理できます。
  Then, it can compare the accumulated output with the previous frame and only send the necessary changes to the terminal.
  次に、蓄積された出力を前のフレームと比較し、必要な変更のみを端末に送信できます。
* `src/tui.rs` implements an immediate mode UI. Its module implementation gives an overview how it works and I recommend reading it.
* `src/tui.rs` はイミディエイトモードUIを実装しています。そのモジュール実装は、それがどのように機能するかの概要を示しており、読むことをお勧めします。
* `src/vt.rs` implements our VT parser.
* `src/vt.rs` は私たちのVTパーサーを実装しています。
* `src/sys` contains our platform abstractions.
* `src/sys` には私たちのプラットフォーム抽象化が含まれています。
* Finally, `src/bin/edit` ties everything together.
* 最後に、`src/bin/edit` がすべてを結び付けます。
  It's roughly 90% UI code and business logic.
  これはおおよそ90%がUIコードとビジネスロジックです。
  It contains a little bit of VT logic in `setup_terminal`.
  `setup_terminal` に少しVTロジックが含まれています。

If you have an issue with your terminal, the places of interest are the aforementioned:
端末に問題がある場合、関心のある場所は前述のとおりです。
* VT parser in `src/vt.rs`
* `src/vt.rs` のVTパーサー
* Platform specific code in `src/sys`
* `src/sys` のプラットフォーム固有のコード
* And the `setup_terminal` function in `src/bin/edit/main.rs`
* そして `src/bin/edit/main.rs` の `setup_terminal` 関数
