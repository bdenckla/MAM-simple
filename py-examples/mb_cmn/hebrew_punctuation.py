SOPA = "\N{HEBREW PUNCTUATION SOF PASUQ}"  # ׃
MAQ = "\N{HEBREW PUNCTUATION MAQAF}"  # ־
PASOLEG = "\N{HEBREW PUNCTUATION PASEQ}"  # ׀
NUN_HAF = "\N{HEBREW PUNCTUATION NUN HAFUKHA}"
GERSHAYIM = "\N{HEBREW PUNCTUATION GERSHAYIM}"  # ״
# GERESH = '\N{HEBREW PUNCTUATION GERESH}'
UPDOT = "\N{HEBREW MARK UPPER DOT}"  # aka extraordinary upper dot
LODOT = "\N{HEBREW MARK LOWER DOT}"  # aka extraordinary lower dot
MCIRC = "\N{HEBREW MARK MASORA CIRCLE}"
#
MAQ_RE = r"\u05be"

NU_GMAQ = "~"  # non-unicode gray maqaf (tilde)


def split_at_maq(string):
    return string.split(MAQ)
