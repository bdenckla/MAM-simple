"""Exports Latin-alphabet symbols for some template names"""

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
    "מ:קו״כ-אם-2": "kq-trivial",
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
