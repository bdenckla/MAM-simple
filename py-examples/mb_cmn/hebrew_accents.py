"""Exports names for Unicode Hebrew accents"""

from mb_cmn import cantsys

ATN = "\N{HEBREW ACCENT ETNAHTA}"
SEG_A = "\N{HEBREW ACCENT SEGOL}"
SHA = "\N{HEBREW ACCENT SHALSHELET}"
ZAQ_Q = "\N{HEBREW ACCENT ZAQEF QATAN}"
ZAQ_G = "\N{HEBREW ACCENT ZAQEF GADOL}"
TIP = "\N{HEBREW ACCENT TIPEHA}"
REV = "\N{HEBREW ACCENT REVIA}"
ZSH_OR_TSIT = "\N{HEBREW ACCENT ZARQA}"
PASH = "\N{HEBREW ACCENT PASHTA}"
YET = "\N{HEBREW ACCENT YETIV}"
TEV = "\N{HEBREW ACCENT TEVIR}"
GER = "\N{HEBREW ACCENT GERESH}"
GER_M = "\N{HEBREW ACCENT GERESH MUQDAM}"
GER_2 = "\N{HEBREW ACCENT GERSHAYIM}"
QAR = "\N{HEBREW ACCENT QARNEY PARA}"
TEL_G = "\N{HEBREW ACCENT TELISHA GEDOLA}"
PAZ = "\N{HEBREW ACCENT PAZER}"
ATN_H = "\N{HEBREW ACCENT ATNAH HAFUKH}"
MUN = "\N{HEBREW ACCENT MUNAH}"
MAH = "\N{HEBREW ACCENT MAHAPAKH}"
MER = "\N{HEBREW ACCENT MERKHA}"
MER_2 = "\N{HEBREW ACCENT MERKHA KEFULA}"
DAR = "\N{HEBREW ACCENT DARGA}"
QOM = "\N{HEBREW ACCENT QADMA}"
TEL_Q = "\N{HEBREW ACCENT TELISHA QETANA}"
YBY = "\N{HEBREW ACCENT YERAH BEN YOMO}"
OLE = "\N{HEBREW ACCENT OLE}"
ILU = "\N{HEBREW ACCENT ILUY}"
DEX = "\N{HEBREW ACCENT DEHI}"
Z_OR_TSOR = "\N{HEBREW ACCENT ZINOR}"
#
ZSH_OR_TSIT_RE = r"\u0598"
MER_RE = r"\u05a5"  # For use in regular expressions
MAH_RE = r"\u05a4"
TIP_RE = r"\u0596"

# In SEG_A, the A is for "accent", i.e. distinguishing it from the vowel SEGOL_V.
# In ZSH_OR_TSIT, the ZSH stands for "zarqa stress helper" (!)
# In ZSH_OR_TSIT, the TSIT stands for "tsinnorit" (an accent confined to Sifrei Emet)
# In Z_OR_TSOR, the Z stands for "zarqa"
# In Z_OR_TSOR, the TSOR stands for "tsinnor" (an accent confined to Sifrei Emet)
# In QOM, the Q stands for qadma (aka azla)
# In QOM, the O stands for "or".
# In QOM, the M stands for "metigah".
# Thus, QOM stands for "qadma or metigah".
# YBY is also known as galgal.

UNI_OVER_ACCENTS = {
    REV,
    GER,
    GER_2,
    GER_M,
    TEL_G,
    TEL_Q,
    QAR,
    PASH,
    QOM,
    ZAQ_Q,
    ZAQ_G,
    SEG_A,
    ZSH_OR_TSIT,
    Z_OR_TSOR,
    PAZ,
    SHA,
    OLE,
    ILU,
}
UNI_UNDER_ACCENTS = {
    ATN,
    MUN,
    TEV,
    TIP,
    MER,
    MAH,
    DAR,
    YET,
    YBY,
    MER_2,
    DEX,
    ATN_H,
}


# NU: non-Unicode
# Both prose and poetic
NU_SLQ = "üslq"
NU_MTG = "ümtg"
NU_SHA_LEG = "üshall"
NU_MUN_LEG = "ümunl"
# Prose only
NU_Z = "üz"
NU_QOM = "üqom"
NU_TIP = "ütip"
# Poetic only
NU_MAH_LEG = "ümahl"
NU_AZL_LEG = "üazll"
NU_AZL = "üazl"
NU_TSOR = "ütsor"
NU_TSIT = "ütsit"
NU_TAR = "ütar"
#
NU_REV_IRM = "ürevirm"
# XXX TODO probably we should also re-code the revia marks that are not part of revia mugrash

NON_UNICODE_ACCENTS = {
    NU_SLQ,
    # NU_MTG,
    NU_SHA_LEG,
    NU_MUN_LEG,
    NU_Z,
    NU_MAH_LEG,
    NU_AZL_LEG,
    # NU_AZL,
    NU_TSOR,
    NU_TSIT,
}

G1_TG = GER + TEL_G
G2_TG = GER_2 + TEL_G

ACCENTS_AND_MTG = r"\u0591-\u05ae\u05bd"

_CONJUNCTIVES_BCC_PROSE = [  # See Yeivin ITM #194 (page 167)
    MUN,  # (but munax legarmeih is disjunctive)
    MAH,
    MER,
    DAR,
    QOM,
    TEL_Q,
    YBY,
    MER_2,
    # MAYELA (coded as tipexa; need to distinguish)
]
_CONJUNCTIVES_BCC_POETIC = [  # See Yeivin ITM #358 (page 264) and, for ATN_H only, #361 (page 266)
    MUN,
    MER,  # but as yored (always in oleh-we-yored) is disjunctive
    ILU,
    TIP,  # tarxa
    YBY,
    MAH,  # (but mehuppak legarmeih is disjunctive)
    QOM,  # aka azla (but azla legarmeih is disjunctive)
    SHA,  # shalshelet qeṭannah (but shalshelet gedolah (shalshelet legarmeih) is disjunctive)
    NU_TSIT,  # tsinnorit
    ATN_H,
    # In Yeivin ITM (#361 (page 266)), atnax hafukh is called only "a 'v' shaped sign"
    # and is not listed with the other poetic conjunctives,
    # i.e. is not listed in #358 (page 264).
]
CONJUNCTIVES_BCC = cantsys.mk_cantsys_struct(
    _CONJUNCTIVES_BCC_PROSE, _CONJUNCTIVES_BCC_POETIC
)
