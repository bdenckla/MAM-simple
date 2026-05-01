"""Exports names for Unicode Hebrew letters"""

import re

# אבגדהוזחטיכךלמםנןסעפףצץקרשת

ALEF = "\N{HEBREW LETTER ALEF}"
BET = "\N{HEBREW LETTER BET}"
GIMEL = "\N{HEBREW LETTER GIMEL}"
DALET = "\N{HEBREW LETTER DALET}"
HE = "\N{HEBREW LETTER HE}"
VAV = "\N{HEBREW LETTER VAV}"
ZAYIN = "\N{HEBREW LETTER ZAYIN}"
XET = "\N{HEBREW LETTER HET}"
TET = "\N{HEBREW LETTER TET}"
YOD = "\N{HEBREW LETTER YOD}"
FKAF = "\N{HEBREW LETTER FINAL KAF}"
KAF = "\N{HEBREW LETTER KAF}"
LAMED = "\N{HEBREW LETTER LAMED}"
FMEM = "\N{HEBREW LETTER FINAL MEM}"
MEM = "\N{HEBREW LETTER MEM}"
FNUN = "\N{HEBREW LETTER FINAL NUN}"
NUN = "\N{HEBREW LETTER NUN}"
SAMEKH = "\N{HEBREW LETTER SAMEKH}"
AYIN = "\N{HEBREW LETTER AYIN}"
FPE = "\N{HEBREW LETTER FINAL PE}"
PE = "\N{HEBREW LETTER PE}"
FTSADI = "\N{HEBREW LETTER FINAL TSADI}"
TSADI = "\N{HEBREW LETTER TSADI}"
QOF = "\N{HEBREW LETTER QOF}"
RESH = "\N{HEBREW LETTER RESH}"
SHIN = "\N{HEBREW LETTER SHIN}"
TAV = "\N{HEBREW LETTER TAV}"


def letters(string: str):
    """Return only the letters in the given string"""
    # I.e. strip out any vowel points, accents, maqaf marks, etc.
    pattern = r"[^א-ת]*"
    return re.sub(pattern, "", string)
