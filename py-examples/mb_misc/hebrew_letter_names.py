from mb_cmn import hebrew_punctuation as hpu

_DIC_OF_LETTERS_TO_LETTER_NAMES_Q2 = {
    #
    # alphabet spelled out
    #
    "א": 'אל"ף',  # alef
    "ב": 'בי"ת',  # bet
    "ג": 'גימ"ל',  # gimel
    "ד": 'דל"ת',  # dalet
    "ה": 'ה"א',  # he
    "ו": 'וי"ו',  # vav
    "ז": 'זי"ן',  # zayin
    "ח": 'חי"ת',  # xet
    "ט": 'טי"ת',  # tet
    "י": 'יו"ד',  # yod
    "כ": 'כ"ף',  # kaf
    "ל": 'למ"ד',  # lamed
    "מ": 'מ"ם',  # mem
    "נ": 'נו"ן',  # nun
    "ס": 'סמ"ך',  # samekh
    "ע": 'עי"ן',  # ayin
    "פ": 'פ"א',  # pe
    "צ": 'צד"י',  # tsadi
    "ק": 'קו"ף',  # qof
    "ר": 'רי"ש',  # resh
    "ש": 'שי"ן',  # shin
    "ת": 'תי"ו',  # tav
    "ך": 'כ"ף סופית',
    "ם": 'מ"ם סופית',
    "ן": 'נו"ן סופית',
    "ף": 'פ"א סופית',
    "ץ": 'צד"י סופית',
}
LETTER_NAMES_Q2 = tuple(_DIC_OF_LETTERS_TO_LETTER_NAMES_Q2.values())
_Q2_TO_G2 = str.maketrans({'"': hpu.GERSHAYIM})
DIC_OF_LETTERS_TO_LETTER_NAMES_G2 = {
    k: v.translate(_Q2_TO_G2) for k, v in _DIC_OF_LETTERS_TO_LETTER_NAMES_Q2.items()
}
