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


_INTRODUCTION_URL = ws_urls.he_url("ויקיטקסט:מבוא_למקרא_על_פי_המסורה")
# No non-Dovi equivalent exists for this Hebrew talk-page URL.
_REPORT_URL = ws_urls.he_url("שיחת_משתמש:Dovi")
# No non-Dovi equivalent exists for this English page URL.
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
