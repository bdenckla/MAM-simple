"""Exports Latin-alphabet symbols for some template names

QUOTE MARKS: a name here carrying a quote mark uses Hebrew gershayim (U+05F4),
which is the canonical form of the name rather than one format's variant of it.
The raw wikitext writes an ASCII double quote as a shorthand for the gershayim,
and ``ws_tmpl1.template_name()`` resolves that shorthand — it normalizes the quote
to gershayim for both the ``stmpl`` and the ``tmpl`` shape, via
``py_misc.true_gershayim``, whose ``in_str`` is named for treating the gershayim as
the true character and the ASCII quote as the stand-in. So the parsed name is
always the canonical one, and these constants are what it equals.

The shorthand is still visible in stored data, which is the one thing to watch:
MAM-parsed-PLAIN keeps the raw wikitext spelling in its ``stmpl`` strings and
``tmpl`` lists — ``קו"כ``, ``מ:קו"כ-אם-2``, ``מ:כו"ק מיוחד``,
``מ:אין פרשה בתחילת פרק בספרי אמ"ת`` — so a raw plain name compared without going
through ``template_name()`` will not equal any constant here. MAM-parsed-PLUS
stores the canonical spelling directly in ``tmpl_name`` and can be compared raw,
and has since MAM-parsed 2993dbd of 2026-05-09, "Use g2 not q2 in tmpl names".
Before 2993dbd, though, plus data has the ASCII shorthand in ``tmpl_name`` just as
plain data does. So code reading plus data from arbitrary git revisions, rather than
from the working tree, must normalize the quote before comparing;
``py/mb_diff_mpu/mpplus_extract.py``'s ``_canonicalize_template_names`` is the
worked example.
Names with no quote mark are spelled identically everywhere and raise none of this.
"""

# Named because more than one comparison site needs them, in this repo's siblings
# as well as here; see the quote-mark note above for how each name is spelled.
INVERTED_NUN = "מ:נו״ן הפוכה"
TRIVIAL_QERE = "מ:קו״כ-אם-2"

TWO_ACCENTS_OF_QUPO = "שני טעמים באות אחת קמץ-תחתון-פתח-עליון"
NO_PAR_AT_STA_OF_CHAP21 = "מ:אין פרשה בתחילת פרק"
NO_PAR_AT_STA_OF_CHAP03 = "מ:אין פרשה בתחילת פרק בספרי אמ״ת"
NO_PAR_AT_STA_OF_WEEKLY = "מ:אין רווח של פרשה בתחילת פרשת השבוע"
SLH_WORD = "מ:אות-מיוחדת-במילה"
SCRDFF_TAR = "מ:הערה-2"
SCRDFF_NO_TAR = "מ:הערה"

LATIN_SHORTS = {
    "כו״ק": "k1q1-kq",  # 1
    "קו״כ": "k1q1-qk",  # 2
    TRIVIAL_QERE: "kq-trivial",
    "קרי ולא כתיב": "kq-q-velo-k",
    "כתיב ולא קרי": "kq-k-velo-q",
}
#  1: a normal ketiv/qere.
#  2: a ketiv/qere where template arguments are in kq order but they should be rendered in reverse order (qk order).
# Retired special-kq subtypes (k1q1-mcom through k3q3) are intentionally
# excluded from this modern-only module.


def map_all_std_kq_to_a_constant(the_constant):
    return {n: the_constant for n in STD_KQ_TMPL_NAMES}


def map_all_whitespace_to_a_constant(the_constant):
    return {n: the_constant for n in WHITESPACE_TMPL_NAMES}


STD_KQ_TMPL_NAMES = (
    "כו״ק",
    "קו״כ",
    "מ:כו״ק מיוחד",
)
WHITESPACE_TMPL_NAMES = {
    "מ:ששש",
    "סס",
    "פפ",
    "ססס",
    "פפפ",
    "ר0",
    "ר1",
    "ר2",
    "ר3",
}
