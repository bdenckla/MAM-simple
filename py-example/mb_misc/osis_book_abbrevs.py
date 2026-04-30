import re
from mb_cmn import bib_locales as tbn

# From https://wiki.crosswire.org/OSIS_Book_Abbreviations.


def bk24_bkgs(bk39ids):
    """
    Return the bk24 book groups corresponding to the given bk39ids.
    """
    bkg_dic = {}
    for bk39id in bk39ids:
        bk24id = tbn.bk24id(bk39id)
        bkids_of_bk24 = tbn.bk39ids_of_bk24(bk24id)
        osis_ids_of_bk24 = map(_osis_id_of_bkid, bkids_of_bk24)
        osis_bk24na = "".join(osis_ids_of_bk24)
        bkg_dic[osis_bk24na] = bkids_of_bk24
    bkgs = tuple(_bkg_make(*item) for item in bkg_dic.items())
    return bkgs


def get_bcv_from_osis_id(osid_id):
    # Get bkid, chnu, & vrnu triple from an osisID.
    patt = r"([A-Za-z0-9]*)\.(\d+)\.(\d+)"
    match = re.match(patt, osid_id)
    assert match
    oba, chnu_str, vrnu_str = match.groups()
    bkid = BK39ID_FROM_OBA[oba]
    chnu = int(chnu_str)
    vrnu = int(vrnu_str)
    return bkid, chnu, vrnu


def get_bc_from_osis_id(osid_id):
    # Get bkid & chnu pair from an osisID.
    patt = r"([A-Za-z0-9]*)\.(\d+)"
    match = re.match(patt, osid_id)
    assert match
    oba, chnu_str = match.groups()
    bkid = BK39ID_FROM_OBA[oba]
    chnu = int(chnu_str)
    return bkid, chnu


def _bkg_make(name, bkids):
    """Make a "book group" structure."""
    return {
        "bkg-name": name,
        "bkg-bkids": bkids,
    }


def _osis_id_of_bkid(bkid):
    return BOOK_ABBREVS[bkid]


BOOK_ABBREVS = {
    tbn.BK_GENESIS: "Gen",
    tbn.BK_EXODUS: "Exod",
    tbn.BK_LEVIT: "Lev",
    tbn.BK_NUMBERS: "Num",
    tbn.BK_DEUTER: "Deut",
    tbn.BK_JOSHUA: "Josh",
    tbn.BK_JUDGES: "Judg",
    tbn.BK_RUTH: "Ruth",
    tbn.BK_FST_SAM: "1Sam",
    tbn.BK_SND_SAM: "2Sam",
    tbn.BK_FST_KGS: "1Kgs",
    tbn.BK_SND_KGS: "2Kgs",
    tbn.BK_FST_CHR: "1Chr",
    tbn.BK_SND_CHR: "2Chr",
    tbn.BK_EZRA: "Ezra",
    tbn.BK_NEXEM: "Neh",
    tbn.BK_ESTHER: "Esth",
    tbn.BK_JOB: "Job",
    tbn.BK_PSALMS: "Ps",
    tbn.BK_PROV: "Prov",
    tbn.BK_QOHELET: "Eccl",
    tbn.BK_SONG: "Song",
    tbn.BK_ISAIAH: "Isa",
    tbn.BK_JEREM: "Jer",
    tbn.BK_LAMENT: "Lam",
    tbn.BK_EZEKIEL: "Ezek",
    tbn.BK_DANIEL: "Dan",
    tbn.BK_HOSHEA: "Hos",
    tbn.BK_JOEL: "Joel",
    tbn.BK_AMOS: "Amos",
    tbn.BK_OVADIAH: "Obad",
    tbn.BK_JONAH: "Jonah",
    tbn.BK_MIKHAH: "Mic",
    tbn.BK_NAXUM: "Nah",
    tbn.BK_XABA: "Hab",
    tbn.BK_TSEF: "Zeph",
    tbn.BK_XAGGAI: "Hag",
    tbn.BK_ZEKHAR: "Zech",
    tbn.BK_MALAKHI: "Mal",
}
BK39ID_FROM_OBA = {oba: bk39id for bk39id, oba in BOOK_ABBREVS.items()}
