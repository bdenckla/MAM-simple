"""Exports HEBREW and Hebrew Wikisource URL helpers."""

from mb_cmn.he_wikisource_url import he_page_url


def he_url(path: str, fragment: str | None = None) -> str:
    """Build a Hebrew Wikisource URL from readable path and optional fragment."""
    return he_page_url(path, fragment)


HEBREW = he_page_url("מקרא_על_פי_המסורה")
