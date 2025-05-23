// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.
// MITライセンスに基づきライセンスされています。

//! Abstractions over reading/writing arbitrary text containers.
//! 任意のテキストコンテナの読み書きに関する抽象化。

use std::ffi::OsString;
use std::mem;
use std::ops::Range;
use std::path::PathBuf;

use crate::arena::{ArenaString, scratch_arena};
use crate::helpers::ReplaceRange as _;

/// An abstraction over reading from text containers.
/// テキストコンテナからの読み取りに関する抽象化。
pub trait ReadableDocument {
    /// Read some bytes starting at (including) the given absolute offset.
    /// 指定された絶対オフセットから始まる (含む) バイトを読み取ります。
    ///
    /// # Warning // 警告
    ///
    /// * Be lenient on inputs: // 入力には寛容であること:
    ///   * The given offset may be out of bounds and you MUST clamp it. // 指定されたオフセットは範囲外の可能性があり、クランプする必要があります。
    ///   * You should not assume that offsets are at grapheme cluster boundaries. // オフセットが書記素クラスタ境界にあると仮定しないでください。
    /// * Be strict on outputs: // 出力には厳密であること:
    ///   * You MUST NOT break grapheme clusters across chunks. // チャンク間で書記素クラスタを分割してはいけません。
    ///   * You MUST NOT return an empty slice unless the offset is at or beyond the end. // オフセットが末尾またはそれを超えている場合を除き、空のスライスを返してはいけません。
    fn read_forward(&self, off: usize) -> &[u8];

    /// Read some bytes before (but not including) the given absolute offset.
    /// 指定された絶対オフセットの前の (含まない) バイトを読み取ります。
    ///
    /// # Warning // 警告
    ///
    /// * Be lenient on inputs: // 入力には寛容であること:
    ///   * The given offset may be out of bounds and you MUST clamp it. // 指定されたオフセットは範囲外の可能性があり、クランプする必要があります。
    ///   * You should not assume that offsets are at grapheme cluster boundaries. // オフセットが書記素クラスタ境界にあると仮定しないでください。
    /// * Be strict on outputs: // 出力には厳密であること:
    ///   * You MUST NOT break grapheme clusters across chunks. // チャンク間で書記素クラスタを分割してはいけません。
    ///   * You MUST NOT return an empty slice unless the offset is zero. // オフセットがゼロの場合を除き、空のスライスを返してはいけません。
    fn read_backward(&self, off: usize) -> &[u8];
}

/// An abstraction over writing to text containers.
/// テキストコンテナへの書き込みに関する抽象化。
pub trait WriteableDocument: ReadableDocument {
    /// Replace the given range with the given bytes.
    /// 指定された範囲を指定されたバイトで置き換えます。
    ///
    /// # Warning // 警告
    ///
    /// * The given range may be out of bounds and you MUST clamp it. // 指定された範囲は範囲外の可能性があり、クランプする必要があります。
    /// * The replacement may not be valid UTF8. // 置換は有効なUTF8ではない可能性があります。
    fn replace(&mut self, range: Range<usize>, replacement: &[u8]);
}

impl ReadableDocument for &[u8] {
    fn read_forward(&self, off: usize) -> &[u8] {
        let s = *self;
        &s[off.min(s.len())..]
    }

    fn read_backward(&self, off: usize) -> &[u8] {
        let s = *self;
        &s[..off.min(s.len())]
    }
}

impl ReadableDocument for String {
    fn read_forward(&self, off: usize) -> &[u8] {
        let s = self.as_bytes();
        &s[off.min(s.len())..]
    }

    fn read_backward(&self, off: usize) -> &[u8] {
        let s = self.as_bytes();
        &s[..off.min(s.len())]
    }
}

impl WriteableDocument for String {
    fn replace(&mut self, range: Range<usize>, replacement: &[u8]) {
        // `replacement` is not guaranteed to be valid UTF-8, so we need to sanitize it.
        // `replacement` は有効なUTF-8であることが保証されていないため、サニタイズする必要があります。
        let scratch = scratch_arena(None);
        let utf8 = ArenaString::from_utf8_lossy(&scratch, replacement);
        let src = match &utf8 {
            Ok(s) => s,
            Err(s) => s.as_str(),
        };

        // SAFETY: `range` is guaranteed to be on codepoint boundaries.
        // 安全性: `range` はコードポイント境界にあることが保証されています。
        unsafe { self.as_mut_vec() }.replace_range(range, src.as_bytes());
    }
}

impl ReadableDocument for PathBuf {
    fn read_forward(&self, off: usize) -> &[u8] {
        let s = self.as_os_str().as_encoded_bytes();
        &s[off.min(s.len())..]
    }

    fn read_backward(&self, off: usize) -> &[u8] {
        let s = self.as_os_str().as_encoded_bytes();
        &s[..off.min(s.len())]
    }
}

impl WriteableDocument for PathBuf {
    fn replace(&mut self, range: Range<usize>, replacement: &[u8]) {
        let mut vec = mem::take(self).into_os_string().into_encoded_bytes();
        vec.replace_range(range, replacement);
        *self = unsafe { Self::from(OsString::from_encoded_bytes_unchecked(vec)) };
    }
}
