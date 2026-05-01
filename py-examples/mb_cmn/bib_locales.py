"""
This module exports various constants and functions related to identifying
the books of the Hebrew Bible and identifying verses within those books.
"""

import re

# Various programs take a --book39 argument.
# This comment explains here, centrally, what values are expected for such an
# argument.
# book39 is a book name of the following type:
#    * It names a book in the "1 out of 39 books" sense of the word "book".
#         (This is as opposed to the "1 out of 24 books" sense.)
#    * It names these books using our "tbn" convention. The "tbn" convention
#         is encoded here in the my_locales Python module, in
#         constants like FST_SAMUEL.
# A pithy example of a valid value for book39 is 1Samuel.
# The example is pithy since:
#    * It shows that this is a "39 books" name, since we identify a "half"
#         of Samuel.
#    * It shows that this is neither the Sefaria nor the UXLC book naming
#         convention, since those would be I Samuel and Samuel_1 respectively.


def bk39_is_of_sec(secid, bk39id):
    """Return whether the given book belongs to the given section."""
    return get_secid(bk39id) == secid


def bk39s_of_sec(secid):
    """Return a tuple of all book names in the given section."""
    return tuple(b for b in ALL_BK39_IDS if bk39_is_of_sec(secid, b))


def get_secid(bk39id):
    """Return the section ID to which the given book belongs."""
    assert bk39id in ALL_BK39_IDS
    return _bkprop_secid(_BK39_PROPERTIES[bk39id])


def section_for_bk24(bk24id):
    """Return the section to which the given book24 belongs."""
    bk39ids = bk39ids_of_bk24(bk24id)
    return get_secid(bk39ids[0])  # a book24 never spans a section


def book_is_of_bk24(in_bk24id, bk39id):
    """Return whether the given book belongs to the given book24."""
    assert bk39id in ALL_BK39_IDS
    return _bkprop_bk24id(_BK39_PROPERTIES[bk39id]) == in_bk24id


def bk39ids_of_bk24(in_bk24id):
    """Return a tuple of all book names in the given book24."""
    return tuple(b for b in ALL_BK39_IDS if book_is_of_bk24(in_bk24id, b))


def bk24id(bk39id):
    """Return the book24 to which the given bk39 belongs."""
    return _bkprop_bk24id(_BK39_PROPERTIES[bk39id])


def get_bknu(bk39id):  # E.g. 1 for GENESIS, 39 for SND_CHRONICLES.
    """
    E.g. 1 for GENESIS, 39 for SND_CHRONICLES.
    """
    return _bkprop_number(_BK39_PROPERTIES[bk39id])


def ordered_short_dash_full_39(bk39id):
    """Return, for example, A1-Genesis given Genesis"""
    assert bk39id in ALL_BK39_IDS
    return f"{ordered_short(bk39id)}-{bk39id}"


def ordered_short_dash_full_24(bk24id):
    """Return, for example, 'BC-Kings.json' given 'Kings'."""
    assert bk24id in _ALL_BK24_IDS
    return f"{_ordered_short_24(bk24id)}-{bk24id}"


def short_bcv(bcv):
    """
    Returns, for example, G2:3 for Genesis chapter 2 verse 3.
    Note that, to minimize string length, there is no space between the
    (short) book name and the chapter.
    """
    return f"{short(bcv[0])}{bcv[1]}:{bcv[2]}"


def parse_short_bcv(short_bcv):
    bcv_patt = r"([A-Za-z0-9][A-Za-z]?)" + r"(\d+)" + ":" + r"(\d+)"
    match = re.fullmatch(bcv_patt, short_bcv)
    assert match is not None
    book_name_short, bcv_chnu_str, bcv_vrnu_str = match.groups()
    chnu_int = int(bcv_chnu_str)
    vrnu_int = int(bcv_vrnu_str)
    book_name_std = std_from_short(book_name_short)
    return book_name_std, chnu_int, vrnu_int


def ordered_short_bcv(bcv):
    """
    Returns, for example, A1G0203 for Genesis 2:3.
    """
    ord_bk = ordered_short(bcv[0])
    sht_bk = short(bcv[0])
    return ord_bk + sht_bk + zfilled_cv(bcv)


def zfilled_cv(bcv):
    ord_chnu_str = my_zfill(bcv[1], _max_width_for_chnu(bcv[0]))
    ord_vrnu_str = my_zfill(bcv[2], _max_width_for_vrnu(bcv[0], bcv[1]))
    return ord_chnu_str + ord_vrnu_str


def my_zfill(the_int, width):
    """Call str.zfill, asserting that width is adhered to."""
    zfilled_str = str(the_int).zfill(width)
    assert len(zfilled_str) == width
    return zfilled_str


def short_bcv_of_bcvt(bcvt):
    """Like short_bcv but on a bcvt."""
    return short_bcv(bcvt_get_bcv_triple(bcvt))


def has_dualcant(bcvtmam):  # bcvt in MAM vtrad
    """Return whether locale bcvt has dual cantillation"""
    assert bcvt_is_tmam(bcvtmam)
    return (
        bcvtmam == _SAGA_OF_REUBEN_BCV
        or bcvtmam in _EXDEC_RANGE
        or bcvtmam in _DEDEC_RANGE
    )


def is_poetcant(bcvt):
    """Return whether locale uses poetic (as opposed to prose) cantillation."""
    bk39id = bcvt_get_bk39id(bcvt)
    return get_secid(bk39id) == SEC_SIF_EM and not _is_prose_section_of_job(bcvt)


def nu10(verse_num, vtrad):
    """Return a bcvt in Numbers chapter 10"""
    cvt = mk_cvt(10, verse_num, vtrad)
    return mk_bcvt(BK_NUMBERS, cvt)


def add_part2_bk39ids(bk39ids):
    """
    For each "part 1" bk39id included in bk39ids, add the "part 2" ("next") bk39id.
    """
    nexts = tuple(filter(None, map(part2_bk39id, bk39ids)))
    return tuple(set(tuple(bk39ids) + tuple(nexts)))


def part2_bk39id(bk39id):
    """
    If bk39id is part 1 of a 2-part book, return the bk39id of part 2.
    Otherwise return None.
    """
    the_next_bk39id = {  # next book ID
        BK_FST_SAM: BK_SND_SAM,
        BK_FST_KGS: BK_SND_KGS,
        BK_FST_CHR: BK_SND_CHR,
        BK_EZRA: BK_NEXEM,
    }
    return the_next_bk39id.get(bk39id)


def mk_bcvtmam(bk39id, chnu, vrnu):
    """Return a bcvt with t=VT_MAM"""
    return mk_bcvt(bk39id, mk_cvtmam(chnu, vrnu))


def mk_bcvtsef(bk39id, chnu, vrnu):
    """Return a bct with t=vtrad Sef"""
    return mk_bcvt(bk39id, mk_cvtsef(chnu, vrnu))


def mk_bcvtbhs(bk39id, chnu, vrnu):
    """Return a bcvt with t=vtrad BHS"""
    return mk_bcvt(bk39id, mk_cvtbhs(chnu, vrnu))


def mk_bcvtxxx(bk39id, chnu, vrnu, vtrad):
    """Return a bcvt with t=the given vtrad"""
    return mk_bcvt(bk39id, mk_cvt(chnu, vrnu, vtrad))


def mk_bcvt(bk39id, cvt):
    """Make a bcvt from a cvt"""
    assert is_cvt(cvt)
    return "_bcvt", bk39id, *cvt


def mk_cvtmam(chnu, vrnu):
    """Return a cv qualified with VT_MAM"""
    return chnu, vrnu, VT_MAM


def mk_cvtsef(chnu, vrnu):
    """Return a cv with vtrad Sef"""
    return chnu, vrnu, VT_SEF


def mk_cvtbhs(chnu, vrnu):
    """Return a cv with vtrad BHS"""
    return chnu, vrnu, VT_BHS


def mk_cvt(chnu, vrnu, vtrad):
    """Return a cv with the given vtrad"""
    return chnu, vrnu, vtrad


def bcvt_get_bk39id(bcvt):
    """Return the book ID part of bcvt"""
    assert is_bcvt(bcvt)
    return bcvt[1]


def bcvt_get_cvt(bcvt):
    """Strip the book name"""
    assert is_bcvt(bcvt)
    return bcvt[2:]


def bcvt_get_chnu(bcvt):
    """Return the chapter number part of bcvt"""
    return cvt_get_chnu(bcvt_get_cvt(bcvt))


def bcvt_get_vrnu(bcvt):
    """Return the verse number part of bcvt"""
    return cvt_get_vrnu(bcvt_get_cvt(bcvt))


def bcvt_get_vtrad(bcvt):
    """Return the vtrad part of bcvt"""
    return cvt_get_vtrad(bcvt_get_cvt(bcvt))


def bcvt_get_chnu_vrnu(bcvt):
    """Return the chnu and vrnu parts of cvt, as a pair"""
    return bcvt_get_chnu(bcvt), bcvt_get_vrnu(bcvt)


def bcvt_get_bcv_triple(bcvt):
    """Return the book ID, chapter number, and verse number parts of bcvt"""
    return bcvt_get_bk39id(bcvt), bcvt_get_chnu(bcvt), bcvt_get_vrnu(bcvt)


def bcvt_is_tmam(bcvt):
    """Return whether the vtrad is VT_MAM"""
    return cvt_is_tmam(bcvt_get_cvt(bcvt))


def cvt_get_chnu(cvt):
    """Return the chnu part of cvt"""
    assert is_cvt(cvt)
    return cvt[0]


def cvt_get_vrnu(cvt):
    """Return the vrnu part of cvt"""
    assert is_cvt(cvt)
    return cvt[1]


def cvt_get_vtrad(cvt):
    """Return the vtrad part of cvt"""
    assert is_cvt(cvt)
    return cvt[2]


def cvt_get_chnu_vrnu(cvt):
    """Return the chnu and vrnu parts of cvt, as a pair"""
    return cvt_get_chnu(cvt), cvt_get_vrnu(cvt)


def cvt_is_tmam(cvt):
    """Return whether the vtrad is VT_MAM"""
    return cvt_get_vtrad(cvt) == VT_MAM


def cvt_is_tsef(cvt):
    """Return whether the vtrad is vtrad Sef"""
    return cvt_get_vtrad(cvt) == VT_SEF


def cvt_strip_vtrad(cvt):
    """Strip the vtrad"""
    assert is_cvt(cvt)
    return cvt[:-1]


def eq_mod_vtrad(cvt_a, cvt_b):
    """Return whether these cvts are equal modulo their vtrad."""
    return cvt_strip_vtrad(cvt_a) == cvt_strip_vtrad(cvt_b)


def short(bk39id):
    """
    Returns the (unordered) short name (1 or 2 letters) corresponding to
    the given book. E.g. G for Genesis, Er for Ezra.
    """
    return _bkprop_short(_BK39_PROPERTIES[bk39id])


def std_from_short(short_book_name):
    """
    Returns the standard book name given the (unordered) short name
    (1 or 2 letters). E.g. Genesis for G, Ezra for Er, etc.
    """
    return _SHORT_TO_STD[short_book_name]


def is_bcvt(obj):
    return (
        isinstance(obj, tuple)
        and len(obj) == 5
        and obj[0] == "_bcvt"
        and obj[1] in ALL_BK39_IDS
        and isinstance(obj[2], int)
        and isinstance(obj[3], int)
        and obj[4] in ALL_VTRADS
    )


def is_cvt(obj):
    return (
        isinstance(obj, tuple)
        and len(obj) == 3
        and isinstance(obj[0], int)
        and isinstance(obj[1], int)
        and obj[2] in ALL_VTRADS
    )


def ordered_short(bk39id):  # E.g. 'A1' for GENESIS, 'FD' for SND_CHRONICLES
    """
    Returns the ordered short name (2 alphanumerics) corresponding to the
    given book.
    E.g. A1 for Genesis, BA for 1Samuel.
    The 1st alphanumeric is a letter in the range A to F
    corresponding to the book's section.
    The 2nd alphanumeric is a capital Latin letter or base-10 digit.
    This 2nd alphanumeric identifies and orders the book within its
    section.
    ASCII ordering, in particular digits-before-letters ordering,
    is assumed. E.g. B1 (Joshua) comes before BA (1Samuel).
    """
    return _bkprop_ordered_short(_BK39_PROPERTIES[bk39id])


def _is_prose_section_of_job(bcvt):
    if bcvt_get_bk39id(bcvt) != BK_JOB:
        return False
    chnu = bcvt_get_chnu(bcvt)
    if chnu in (1, 2):
        return True
    vrnu = bcvt_get_vrnu(bcvt)
    if chnu == 3 and vrnu < 2:
        return True
    if chnu == 42 and vrnu > 6:
        return True
    return False


def _max_width_for_chnu(bk39id):
    if bk39id == BK_PSALMS:
        return 3
    if bk39id in _BOOKS_WITH_LESS_THAN_10_CHAPS:
        return 1
    return 2


def _max_width_for_vrnu(bk39id, chnu):
    if (bk39id, chnu) == (BK_PSALMS, 119):
        return 3  # Psalm 119 has 176 verses!
    return 2


def _bkprop_bk24id(bkprop):
    return bkprop[0]


def _bkprop_secid(bkprop):
    return bkprop[1]


def _bkprop_short(bkprop):
    return bkprop[2]


def _bkprop_ordered_short(bkprop):
    return bkprop[3]


def _bkprop_number(bkprop):
    return bkprop[4]


def _shorts_are_unique():
    unique_shorts = set(map(short, ALL_BK39_IDS))
    return len(unique_shorts) == len(ALL_BK39_IDS)


def _mk_verse_range(bcvt, length):
    vrnu_start = bcvt_get_vrnu(bcvt)
    vrange = range(vrnu_start, vrnu_start + length)
    return tuple(_bcvt_setv(bcvt, vrnu) for vrnu in vrange)


def _bcvt_setv(bcvt, new_vrnu):
    bk39id, cvt = bcvt_get_bk39id(bcvt), bcvt_get_cvt(bcvt)
    new_cvt = _cvt_setv(cvt, new_vrnu)
    return mk_bcvt(bk39id, new_cvt)


def _cvt_setv(cvt, new_vrnu):
    chnu, vtrad = cvt_get_chnu(cvt), cvt_get_vtrad(cvt)
    return mk_cvt(chnu, new_vrnu, vtrad)


def _ordered_short_24(bk24id):
    """Return, for example, 'BC' given 'Kings'."""
    assert bk24id in _ALL_BK24_IDS
    bk39ids = bk39ids_of_bk24(bk24id)
    return ordered_short(bk39ids[0])


BK_GENESIS = "Genesis"
BK_EXODUS = "Exodus"
BK_LEVIT = "Levit"
BK_NUMBERS = "Numbers"
BK_DEUTER = "Deuter"
BK_JOSHUA = "Joshua"
BK_JUDGES = "Judges"
BK_FST_SAM = "1Samuel"
BK_SND_SAM = "2Samuel"
BK_FST_KGS = "1Kings"
BK_SND_KGS = "2Kings"
BK_ISAIAH = "Isaiah"
BK_JEREM = "Jeremiah"
BK_EZEKIEL = "Ezekiel"  # guts to change it to Ezeqiel? (k to k)
BK_HOSHEA = "Hosea"  # guts to change it to Hoshea? (s to sh)
BK_JOEL = "Joel"
BK_AMOS = "Amos"
BK_OVADIAH = "Obadiah"  # guts to change it to Ovadiah? (b to v)
BK_JONAH = "Jonah"
BK_MIKHAH = "Micah"  # guts to change it to Mikhah or Miḳah? (c to kh or ḳ)
BK_NAXUM = "Nahum"  # guts to change it to Naxum? (h to x)
BK_XABA = "Habakkuk"  # guts to change it to Xabakkuk? Xabaqquq? (H to X, k to q)
BK_TSEF = "Tsefaniah"
BK_XAGGAI = "Haggai"  # guts to change it to Xaggai? (H to X)
BK_ZEKHAR = "Zechariah"  # guts to change it to Zekhariah or Zeḳariah? (ch to kh or ḳ)
BK_MALAKHI = "Malachi"  # guts to change it to Malakhi or Malaḳi? (ch to kh or ḳ)
BK_PSALMS = "Psalms"
BK_PROV = "Proverbs"
BK_JOB = "Job"
BK_SONG = "Song of Songs"
BK_RUTH = "Ruth"
BK_LAMENT = "Lamentations"
BK_QOHELET = "Ecclesiastes"
BK_ESTHER = "Esther"
BK_DANIEL = "Daniel"
BK_EZRA = "Ezra"
BK_NEXEM = "Nehemiah"  # guts to change it to Nexemiah? (h to x)
BK_FST_CHR = "1Chronicles"
BK_SND_CHR = "2Chronicles"

BK24_GENESIS = BK_GENESIS
BK24_EXODUS = BK_EXODUS
BK24_LEVIT = BK_LEVIT
BK24_NUMBERS = BK_NUMBERS
BK24_DEUTER = BK_DEUTER
BK24_JOSHUA = BK_JOSHUA
BK24_JUDGES = BK_JUDGES
BK24_SAMUEL = "Samuel"
BK24_KINGS = "Kings"
BK24_ISAIAH = BK_ISAIAH
BK24_JEREM = BK_JEREM
BK24_EZEKIEL = BK_EZEKIEL
BK24_THE_12 = "The-12-Minor-Prophets"
BK24_PSALMS = BK_PSALMS
BK24_PROV = BK_PROV
BK24_JOB = BK_JOB
BK24_SONG = BK_SONG
BK24_RUTH = BK_RUTH
BK24_LAMENT = BK_LAMENT
BK24_QOHELET = BK_QOHELET
BK24_ESTHER = BK_ESTHER
BK24_DANIEL = BK_DANIEL
BK24_EZ_NE = "Ezra-Nexemiah"
BK24_CHRON = "Chronicles"

SEC_TORAH = "Torah"
SEC_NEV_RISH = "NevRish"
SEC_NEV_AX = "NevAx"
SEC_SIF_EM = "SifEm"
SEC_XAM_MEG = "XamMeg"
SEC_KET_AX = "KetAx"

VT_MAM = "vtmam"
VT_SEF = "vtsef"
VT_BHS = "vtbhs"
ALL_VTRADS = VT_MAM, VT_SEF, VT_BHS

BK39IDS_OF_BOOKS_WITH_DUALCANT = BK_GENESIS, BK_EXODUS, BK_DEUTER

_SH_GENESIS = "G", "A1", 1
_SH_EXODUS = "E", "A2", 2  # E in contrast to Ee, Ec, Es, Er
_SH_LEVIT = "L", "A3", 3  # L in contrast to La
_SH_NUMBERS = "N", "A4", 4  # N in contrast to Ne & Na
_SH_DEUTER = "D", "A5", 5  # D in contrast to Da
_SH_JOSHUA = "Js", "B1", 6  # Jo.*: JsJlJnJb
_SH_JUDGES = "Ju", "B2", 7
_SH_FST_SAM = "1S", "BA", 8
_SH_SND_SAM = "2S", "BB", 9
_SH_FST_KGS = "1K", "BC", 10
_SH_SND_KGS = "2K", "BD", 11
_SH_ISAIAH = "I", "C1", 12
_SH_JEREM = "Je", "C2", 13
_SH_EZEKIEL = "Ee", "C3", 14  # Ez.*: EeEr
_SH_HOSEA = "Ho", "CA", 15
_SH_JOEL = "Jl", "CB", 16  # Jo.*: JsJlJnJb
_SH_AMOS = "A", "CC", 17
_SH_OBADIAH = "O", "CD", 18
_SH_JONAH = "Jn", "CE", 19  # Jo.*: JsJlJnJb
_SH_MICAH = "Mi", "CF", 20
_SH_NAXUM = "Na", "CG", 21
_SH_XABA = "Hb", "CH", 22  # Ha.*: HbHg
_SH_TSEF = "Ts", "CI", 23  # was Zp (see note below)
_SH_XAGGAI = "Hg", "CJ", 24  # Ha.*: HbHg
_SH_ZEKHAR = "Zc", "CK", 25  # Zc (see note below)
_SH_MALAKHI = "Ma", "CL", 26
_SH_PSALMS = "Ps", "D1", 27
_SH_PROV = "Pr", "D2", 28
_SH_JOB = "Jb", "D3", 29  # Jo.*: JsJlJnJb
_SH_SONG = "S", "E1", 30
_SH_RUTH = "R", "E2", 31
_SH_LAMENT = "La", "E3", 32
_SH_QOHELET = "Ec", "E4", 33
_SH_ESTHER = "Es", "E5", 34
_SH_DANIEL = "Da", "F1", 35
_SH_EZRA = "Er", "FA", 36  # Ez.*: EeEr
_SH_NEXEM = "Ne", "FB", 37
_SH_FST_CHR = "1C", "FC", 38
_SH_SND_CHR = "2C", "FD", 39
# Tsefaniah was formerly Zp because (a) it was formerly spelled Zephaniah
# and (b) with this former spelling, Ze would have been ambiguous with
# Zechariah.
# Zechariah is Zc since Ze would have been ambiguous with Tsefaniah when
# Tsefaniah was spelled Zephaniah.


_BK39_PROPERTIES = {
    BK_GENESIS: (BK24_GENESIS, SEC_TORAH, *_SH_GENESIS),
    BK_EXODUS: (BK24_EXODUS, SEC_TORAH, *_SH_EXODUS),
    BK_LEVIT: (BK24_LEVIT, SEC_TORAH, *_SH_LEVIT),
    BK_NUMBERS: (BK24_NUMBERS, SEC_TORAH, *_SH_NUMBERS),
    BK_DEUTER: (BK24_DEUTER, SEC_TORAH, *_SH_DEUTER),
    BK_JOSHUA: (BK24_JOSHUA, SEC_NEV_RISH, *_SH_JOSHUA),
    BK_JUDGES: (BK24_JUDGES, SEC_NEV_RISH, *_SH_JUDGES),
    BK_FST_SAM: (BK24_SAMUEL, SEC_NEV_RISH, *_SH_FST_SAM),
    BK_SND_SAM: (BK24_SAMUEL, SEC_NEV_RISH, *_SH_SND_SAM),
    BK_FST_KGS: (BK24_KINGS, SEC_NEV_RISH, *_SH_FST_KGS),
    BK_SND_KGS: (BK24_KINGS, SEC_NEV_RISH, *_SH_SND_KGS),
    BK_ISAIAH: (BK24_ISAIAH, SEC_NEV_AX, *_SH_ISAIAH),
    BK_JEREM: (BK24_JEREM, SEC_NEV_AX, *_SH_JEREM),
    BK_EZEKIEL: (BK24_EZEKIEL, SEC_NEV_AX, *_SH_EZEKIEL),
    BK_HOSHEA: (BK24_THE_12, SEC_NEV_AX, *_SH_HOSEA),
    BK_JOEL: (BK24_THE_12, SEC_NEV_AX, *_SH_JOEL),
    BK_AMOS: (BK24_THE_12, SEC_NEV_AX, *_SH_AMOS),
    BK_OVADIAH: (BK24_THE_12, SEC_NEV_AX, *_SH_OBADIAH),
    BK_JONAH: (BK24_THE_12, SEC_NEV_AX, *_SH_JONAH),
    BK_MIKHAH: (BK24_THE_12, SEC_NEV_AX, *_SH_MICAH),
    BK_NAXUM: (BK24_THE_12, SEC_NEV_AX, *_SH_NAXUM),
    BK_XABA: (BK24_THE_12, SEC_NEV_AX, *_SH_XABA),
    BK_TSEF: (BK24_THE_12, SEC_NEV_AX, *_SH_TSEF),
    BK_XAGGAI: (BK24_THE_12, SEC_NEV_AX, *_SH_XAGGAI),
    BK_ZEKHAR: (BK24_THE_12, SEC_NEV_AX, *_SH_ZEKHAR),
    BK_MALAKHI: (BK24_THE_12, SEC_NEV_AX, *_SH_MALAKHI),
    BK_PSALMS: (BK24_PSALMS, SEC_SIF_EM, *_SH_PSALMS),
    BK_PROV: (BK24_PROV, SEC_SIF_EM, *_SH_PROV),
    BK_JOB: (BK24_JOB, SEC_SIF_EM, *_SH_JOB),
    BK_SONG: (BK24_SONG, SEC_XAM_MEG, *_SH_SONG),
    BK_RUTH: (BK24_RUTH, SEC_XAM_MEG, *_SH_RUTH),
    BK_LAMENT: (BK24_LAMENT, SEC_XAM_MEG, *_SH_LAMENT),
    BK_QOHELET: (BK24_QOHELET, SEC_XAM_MEG, *_SH_QOHELET),
    BK_ESTHER: (BK24_ESTHER, SEC_XAM_MEG, *_SH_ESTHER),
    BK_DANIEL: (BK24_DANIEL, SEC_KET_AX, *_SH_DANIEL),
    BK_EZRA: (BK24_EZ_NE, SEC_KET_AX, *_SH_EZRA),
    BK_NEXEM: (BK24_EZ_NE, SEC_KET_AX, *_SH_NEXEM),
    BK_FST_CHR: (BK24_CHRON, SEC_KET_AX, *_SH_FST_CHR),
    BK_SND_CHR: (BK24_CHRON, SEC_KET_AX, *_SH_SND_CHR),
}
_BOOKS_WITH_LESS_THAN_10_CHAPS = (
    BK_AMOS,
    BK_XAGGAI,
    BK_XABA,
    BK_LAMENT,
    BK_MALAKHI,
    BK_MIKHAH,
    BK_NAXUM,
    BK_OVADIAH,
    BK_RUTH,
    BK_SONG,
    BK_JOEL,
    BK_JONAH,
    BK_TSEF,
)
ALL_BK39_IDS = tuple(_BK39_PROPERTIES.keys())
_ALL_BK24_IDS = {bk24id(bk39id): True for bk39id in ALL_BK39_IDS}
ALL_BK24_IDS = tuple(_ALL_BK24_IDS.keys())
ALL_SECIDS = SEC_TORAH, SEC_NEV_RISH, SEC_NEV_AX, SEC_SIF_EM, SEC_XAM_MEG, SEC_KET_AX
_SHORT_TO_STD = {_bkprop_short(prop): std for std, prop in _BK39_PROPERTIES.items()}
_SAGA_OF_REUBEN_BCV = mk_bcvtmam(BK_GENESIS, 35, 22)
_EXDEC_START = mk_bcvtmam(BK_EXODUS, 20, 2)
_DEDEC_START = mk_bcvtmam(BK_DEUTER, 5, 6)
_EXDEC_RANGE = _mk_verse_range(_EXDEC_START, 12)
_DEDEC_RANGE = _mk_verse_range(_DEDEC_START, 12)
_ORDERED_SHORT_SECTION_CODE = {
    SEC_TORAH: "A",
    SEC_NEV_RISH: "B",
    SEC_NEV_AX: "C",
    SEC_SIF_EM: "D",
    SEC_XAM_MEG: "E",
    SEC_KET_AX: "F",
}
ORDERED_SHORT_SECTION_CODE_DASH_SECID = {
    secid: f"{_ORDERED_SHORT_SECTION_CODE[secid]}-{secid}" for secid in ALL_SECIDS
}


assert _shorts_are_unique()
