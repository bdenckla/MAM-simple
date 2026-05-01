"""Exports sef_header"""

from mb_sefaria import sef_cmn
from mb_misc import ws_urls


def sef_header(bkid):
    """Return Sefaria header for book with ID bkid."""
    return {
        "Index Title": sef_cmn.SEF_BKNA[bkid],
        "Version Title": "Miqra according to the Masorah",
        "Language": "he",
        "Version Source": ws_urls.HEBREW,
        "Version Notes": _VERSION_NOTES,
    }


_INTRODUCTION_URL = (
    ws_urls.HEBREW + "/"
    r"%D7%9E%D7%99%D7%93%D7%A2_"
    r"%D7%A2%D7%9C_"
    r"%D7%9E%D7%94%D7%93%D7%95%D7%A8%D7%94_"
    r"%D7%96%D7%95"
)
_REPORT_URL = (
    "https://he.wikisource.org/wiki/"
    r"%D7%A9%D7%99%D7%97%D7%AA_"
    r"%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi"
)
_ENGLISH_ABSTRACT = (
    "https://en.wikisource.org/wiki/"
    "User:Dovi/"
    "Miqra_according_to_the_Masorah#"
    "About_this_Edition_(English_Abstract)"
)
_VERSION_NOTES = (
    "<i>Miqra According to the Masorah</i> (MAM) is a digital Hebrew "
    "edition of the Tanakh based on the Aleppo Codex and related "
    "manuscripts. It is designed for readers, and as such it contains added "
    "elements to aid "
    "vocalization of the text. For instance: When an accent is marked in an "
    "unstressed syllable, an extra accent is added in the proper place "
    "(<i>pashta</i>, <i>zarqa</i>, <i>segol</i>, <i>telisha</i>). "
    "<i>Legarmeih</i> and <i>paseq</i> are visibly distinguished. <i>Qamaz "
    "qatan</i> is indicated by its designated Unicode character "
    "(alternatives are documented where traditions differ about its "
    "application).<br>The text "
    'of MAM is fully documented. The <a href="' + _INTRODUCTION_URL + '">complete '
    "introduction</a> to the edition (Hebrew) explains the types of "
    "editorial decisions that have been made and the reasons for them (<a "
    'href="' + _ENGLISH_ABSTRACT + '">English '
    "abstract</a>). In addition, every word in the Bible about which there "
    "is some textual concern or ambiguity includes a documentation note; "
    "these "
    'notes can be viewed conveniently <a href="'
    "https://bdenckla.github.io/MAM-with-doc/"
    '">here</a>. '
    'If an error is discovered, it may be reported to <a href="'
    + _REPORT_URL
    + '">User:Dovi</a> '
    "at Hebrew Wikisource. Please check the documentation notes before "
    "reporting an error."
)
