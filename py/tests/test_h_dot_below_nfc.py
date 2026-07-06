"""Enforcement test (cross-repo standard, MAM-basics issue #187): tracked
text must standardize Latin transliteration of Hebrew het ("h with dot
below") on NFC, i.e. the precomposed U+1E25 / U+1E24 forms, never the
decomposed "h"/"H" + COMBINING DOT BELOW (U+0323) sequence. Python comments
must not use either Unicode form at all -- plain ASCII "x"/"X" is used
instead, since comments don't flow to output.

Scope note: this test deliberately does NOT assert whole-file NFC
(unicodedata.normalize("NFC", text) == text). A blanket NFC pass reorders
unrelated Hebrew combining marks (shin dot, sin dot, dagesh, rafeh) against
this project's intentional, documented non-Unicode Hebrew mark order. So
this test checks only the specific h-with-dot-below sequence, which composes
unambiguously ("h"/"H" + U+0323 -> U+1E25/U+1E24).

MAM-simple specifics: this repo is entirely generated output (produced by
MAM-basics py/main_mam_simple.py -- json/xml/txt exports, docs, copied
py-examples sources). There is no hand-authored source of its own. The guard
still runs over the generated tree so drift is caught if the generators ever
regress; only GitHub Pages output (gh-pages/) is excluded, as it is a
separate publish artifact. Root is discovered via git so the test runs under
any interpreter from the repo directory (this repo has no .venv of its own).
"""
import subprocess
import unicodedata
import unittest
from pathlib import Path

REPO_ROOT = Path(
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.strip()
)

_COMBINING_DOT_BELOW = chr(0x0323)
_H_WITH_DOT_BELOW = chr(0x1E25)
_H_CAP_WITH_DOT_BELOW = chr(0x1E24)

_BINARY_EXTENSIONS = {
    ".png",
    ".woff2",
    ".svg",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".ttf",
    ".otf",
    ".eot",
    ".zip",
    ".gz",
    ".pyc",
    ".exe",
    ".dll",
}

# GitHub Pages publish output -- excluded like a generated publish artifact.
_EXCLUDE_DIR_PREFIXES = ("gh-pages/",)

_EXCLUDE_FILES = frozenset()

# See MAM-basics reference test: intentionally empty; a future exception can
# be documented here rather than silently carved out elsewhere.
_COMMENT_GLYPH_ALLOWLIST = frozenset()


def _is_binary(path: Path) -> bool:
    return path.suffix.lower() in _BINARY_EXTENSIONS


def _is_excluded(posix_rel: str) -> bool:
    if posix_rel in _EXCLUDE_FILES:
        return True
    return any(posix_rel.startswith(prefix) for prefix in _EXCLUDE_DIR_PREFIXES)


def _tracked_files_in_scope():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    in_scope = []
    for line in result.stdout.splitlines():
        rel = line.strip()
        if not rel:
            continue
        posix_rel = rel.replace("\\", "/")
        if _is_excluded(posix_rel):
            continue
        full = REPO_ROOT / rel
        if not full.is_file():
            continue
        if _is_binary(full):
            continue
        in_scope.append(posix_rel)
    return in_scope


# --- General NFC-Latin-diacritic enforcement (generalizes the het NFC rule to
# --- every Latin base letter carrying a combining diacritic that has a
# --- precomposed form). Composes conceptually only Latin-script clusters; every
# --- Hebrew codepoint (U+0590-05FF, U+FB1D-FB4F) is left untouched. Self-
# --- contained (stdlib unicodedata only), no literal combining mark is typed.
_HEBREW_RANGES_NFC = ((0x0590, 0x05FF), (0xFB1D, 0xFB4F))


def _is_hebrew_cp(ch):
    o = ord(ch)
    return any(lo <= o <= hi for lo, hi in _HEBREW_RANGES_NFC)


def _is_latin_base(ch):
    if unicodedata.combining(ch) != 0:
        return False
    try:
        return unicodedata.name(ch).startswith("LATIN")
    except ValueError:
        return False


def _find_decomposed_latin_clusters(text):
    """Return sorted 1-indexed line numbers where a Latin base + combining
    mark(s) has a strictly-shorter NFC (precomposed) form -- hand-authored
    source that should be composed. Hebrew clusters are never flagged."""
    line_nos = set()
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if (
            _is_latin_base(ch)
            and i + 1 < n
            and unicodedata.combining(text[i + 1]) != 0
        ):
            j = i + 1
            while (
                j < n
                and unicodedata.combining(text[j]) != 0
                and not _is_hebrew_cp(text[j])
            ):
                j += 1
            cluster = text[i:j]
            nfc = unicodedata.normalize("NFC", cluster)
            if len(nfc) < len(cluster) and not any(_is_hebrew_cp(c) for c in nfc):
                line_nos.add(text.count("\n", 0, i) + 1)
            i = j
            continue
        i += 1
    return sorted(line_nos)


class TestHDotBelowNfc(unittest.TestCase):
    """Tracked text must use precomposed h-with-dot-below, never the
    decomposed sequence, and must never use either Unicode form in a
    '#'-led Python comment (plain ASCII "x"/"X" instead)."""

    @classmethod
    def setUpClass(cls):
        cls.in_scope_files = _tracked_files_in_scope()
        # Sanity check: the scoping logic should select a non-trivial number
        # of files (catches a badly broken exclusion filter that accidentally
        # excludes everything). This repo has ~385 in-scope tracked files;
        # 200 is a comfortable floor below that.
        assert len(cls.in_scope_files) > 200, (
            f"Only {len(cls.in_scope_files)} files in scope -- exclusion "
            "filters may be too broad."
        )

    def test_no_decomposed_h_dot_below_in_tracked_files(self):
        offenders = []
        for posix_rel in self.in_scope_files:
            full = REPO_ROOT / posix_rel
            text = full.read_text(encoding="utf-8")
            for i, ch in enumerate(text):
                if (
                    ch in ("h", "H")
                    and i + 1 < len(text)
                    and text[i + 1] == _COMBINING_DOT_BELOW
                ):
                    line_no = text.count("\n", 0, i) + 1
                    offenders.append(f"{posix_rel}:{line_no}")
                    break
        self.assertEqual(
            offenders,
            [],
            "Found decomposed h-with-dot-below (h/H + COMBINING DOT BELOW) "
            "in tracked files; run the NFC migration or fix the generator: "
            f"{offenders}",
        )

    @staticmethod
    def _comment_has_h_dot_below(comment: str) -> bool:
        """True if `comment` contains h-with-dot-below specifically (either
        decomposed "h"/"H" + U+0323, or precomposed U+1E25/U+1E24) -- NOT
        just any U+0323, since U+0323 also legitimately appears on other
        base letters (e.g. "S" in "Sere", "t" in "qetannah"), which is a
        different character combination and out of scope for this issue."""
        if _H_WITH_DOT_BELOW in comment or _H_CAP_WITH_DOT_BELOW in comment:
            return True
        for i, ch in enumerate(comment):
            if (
                ch in ("h", "H")
                and i + 1 < len(comment)
                and comment[i + 1] == _COMBINING_DOT_BELOW
            ):
                return True
        return False

    def test_no_decomposed_latin_diacritic_cluster(self):
        """General NFC rule (supersedes the het-only file check above): no
        hand-authored file may contain a decomposed Latin base+diacritic that
        has a precomposed NFC form (e.g. t/s + dot-below, a + breve, i +
        acute, a + diaeresis). Applies to literals AND comments alike -- this
        is pure NFC precomposition and never ASCII-fies anything; the
        het->ASCII 'x' comment rule is a separate assertion below."""
        offenders = []
        for posix_rel in self.in_scope_files:
            full = REPO_ROOT / posix_rel
            text = full.read_text(encoding="utf-8")
            for line_no in _find_decomposed_latin_clusters(text):
                offenders.append(f"{posix_rel}:{line_no}")
        self.assertEqual(
            offenders,
            [],
            "Found decomposed Latin base+diacritic clusters that have a "
            "precomposed NFC form; run the NFC-Latin migration: "
            f"{offenders}",
        )

    def test_comments_use_ascii_not_h_dot_below(self):
        offenders = []
        for posix_rel in self.in_scope_files:
            if not posix_rel.endswith(".py"):
                continue
            if posix_rel in _COMMENT_GLYPH_ALLOWLIST:
                continue
            full = REPO_ROOT / posix_rel
            text = full.read_text(encoding="utf-8")
            for line_no, line in enumerate(text.split("\n"), start=1):
                hash_idx = line.find("#")
                if hash_idx == -1:
                    continue
                comment = line[hash_idx:]
                if self._comment_has_h_dot_below(comment):
                    offenders.append(f"{posix_rel}:{line_no}")
        self.assertEqual(
            offenders,
            [],
            "Found h-with-dot-below (either Unicode form) in a '#' comment; "
            f"use plain ASCII x/X instead: {offenders}",
        )

    def test_h_dot_below_composition_is_canonically_lossless(self):
        """Spot-check unicodedata agrees h/H + U+0323 composes to
        U+1E25/U+1E24, guarding the core assumption behind this test."""
        self.assertEqual(
            unicodedata.normalize("NFC", "h" + _COMBINING_DOT_BELOW),
            _H_WITH_DOT_BELOW,
        )
        self.assertEqual(
            unicodedata.normalize("NFC", "H" + _COMBINING_DOT_BELOW),
            _H_CAP_WITH_DOT_BELOW,
        )

    def test_comment_detector_flags_decomposed_and_precomposed_h_dot_below(self):
        self.assertTrue(
            self._comment_has_h_dot_below("# guttural / h" + _COMBINING_DOT_BELOW + " slot")
        )
        self.assertTrue(
            self._comment_has_h_dot_below("# guttural / " + _H_WITH_DOT_BELOW + " slot")
        )
        self.assertTrue(
            self._comment_has_h_dot_below("# Capital H" + _COMBINING_DOT_BELOW + "olam")
        )
        self.assertTrue(
            self._comment_has_h_dot_below("# Capital " + _H_CAP_WITH_DOT_BELOW + "olam")
        )

    def test_comment_detector_ignores_dot_below_on_other_base_letters(self):
        # U+0323 legitimately appears on letters other than h/H (e.g. "S" in
        # "Sere", "t" in "qetannah"); that is a different character
        # combination and must NOT be flagged by this check.
        self.assertFalse(
            self._comment_has_h_dot_below("# Closed, S" + _COMBINING_DOT_BELOW + "ere-vowelled")
        )
        self.assertFalse(
            self._comment_has_h_dot_below("# shalshelet qet" + _COMBINING_DOT_BELOW + "annah")
        )


if __name__ == "__main__":
    unittest.main()
