"""Exports HEBREW and Hebrew Wikisource URL helpers."""

from mb_cmn.url_percent import pct_fragment, pct_path_component

_HE_WIKISOURCE_BASE = "https://he.wikisource.org/wiki"


def he_url(path: str, fragment: str | None = None) -> str:
    """Build a Hebrew Wikisource URL from readable path and optional fragment."""
    out = f"{_HE_WIKISOURCE_BASE}/{pct_path_component(path, safe='/:')}"
    if fragment is None:
        return out
    return f"{out}#{pct_fragment(fragment)}"


HEBREW = he_url("מקרא_על_פי_המסורה")
