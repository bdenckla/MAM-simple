"""Deploy the MAM-parsed authored-docs stylesheet.

The CSS is static (no interpolation), so its source of truth is a real .css file
beside this module (styles_mam_parsed.css), not a Python string. make_css_file_for_mam_parsed
copies it verbatim to the destination. (Unlike the repo's other styles_*.py, which still
keep their CSS as Python strings; the versification-and-cantillation doc uses this same
real-.css approach.)
"""

from pathlib import Path

_CSS_SOURCE_PATH = Path(__file__).with_name("styles_mam_parsed.css")


def make_css_file_for_mam_parsed(out_path):
    css = _CSS_SOURCE_PATH.read_text(encoding="utf-8")
    # Force LF: the deployed copies are LF, and a plain text-mode write would emit
    # CRLF on Windows and churn them.
    with open(out_path, "w", encoding="utf-8", newline="") as out_fp:
        out_fp.write(css)
