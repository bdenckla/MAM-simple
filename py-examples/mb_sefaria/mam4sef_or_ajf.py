"""Exports main_helper"""

import json
import os
from mb_misc import my_utils_for_mainish as my_utils_fm
from mb_misc import osis_book_abbrevs
from mb_sefaria import sef_cmn
from mb_cmn import bib_locales as tbn
from mb_cmn import provenance
from mb_misc import write_utils
from mb_sefaria import write_utils_sef_or_ajf
from mb_cmn import shrink


def main_helper(variant):
    """Create the Sefaria MAM or AJF MAM from the XML MAM."""
    bkids = my_utils_fm.get_bk39_tuple_from_argparse()
    bkgs = osis_book_abbrevs.bk24_bkgs(bkids)
    _write_output_provenance(variant, bkgs)
    for bkg in bkgs:
        _do_one_book_group(variant, bkg)


def _write_output_provenance(variant, bkgs):
    if not bkgs:
        return
    sample_name = sef_cmn.SEF_BKNA[bkgs[0]["bkg-bkids"][0]]
    csv_dir = os.path.dirname(write_utils.bkg_path(variant, sample_name))
    unicode_dir = os.path.dirname(
        write_utils.bkg_path(variant, sample_name, fmt_is_unicode_names=True)
    )
    provenance.write_directory_provenance(
        csv_dir,
        __file__,
        "Sefaria CSV exports",
    )
    provenance.write_directory_provenance(
        unicode_dir,
        __file__,
        "Sefaria Unicode-name exports",
    )


def _handle(handlers, jobj):  # jobj: JSON dict
    ofc1_raw = []  # output for all children, summed together
    ofc2 = []  # output for all children, per child
    for child in jobj.get("contents", []):
        output_for_child = _handle(handlers, child)
        ofc1_raw.extend(output_for_child)
        ofc2.append((child, output_for_child))
    ofc1 = shrink.shrink(ofc1_raw)
    attr_text = jobj.get("text")
    if attr_text is not None:
        assert not ofc1
        ofc1 = [attr_text]
    tag_and_class = jobj["type"], jobj.get("class")
    handler = handlers[tag_and_class]
    return shrink.shrink(handler(jobj, ofc1, ofc2))


def _read_book_group(variant, bkg_name):
    vtrad = variant["variant-vtrad"]
    json_vtrad_xxx_dic = {
        tbn.VT_BHS: "json-vtrad-bhs",
        tbn.VT_SEF: "json-vtrad-sef",
    }
    json_vtrad_xxx = json_vtrad_xxx_dic[vtrad]
    json_path = f"../MAM-simple/{json_vtrad_xxx}/{bkg_name}.json"
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def _iter_verses(root_jobj):
    for book39 in root_jobj["contents"]:
        if book39["type"] != "book39":
            continue
        for item in book39["contents"]:
            if item["type"] == "chapter":
                yield from (v for v in item["contents"] if v["type"] == "verse")


def _iter_verses_with_cant_all_three(root_jobj):
    for verse in _iter_verses(root_jobj):
        contents = verse.get("contents", [])
        if any(c["type"] == "cant-all-three" for c in contents):
            yield verse


_ITER_VERSES_FROM_CANT_DAB = {
    "rv-cant-combined": _iter_verses,
    "rv-cant-alef": _iter_verses_with_cant_all_three,
    "rv-cant-bet": _iter_verses_with_cant_all_three,
}


def _process_book_group(variant, root, cant_dab):
    handlers = variant["variant-handlers"]
    vtrad = variant["variant-vtrad"]
    if tuple(handlers.keys()) == _ALL_3_CANT_DAB_VALUES:
        handlers2 = handlers[cant_dab]
    else:
        handlers2 = handlers
    verses_in = _ITER_VERSES_FROM_CANT_DAB[cant_dab](root)
    bk39s_out = {}
    for verse in verses_in:
        osis_id = verse["osisID"]
        bcvt = _get_bcvt_from_osis_id(vtrad, osis_id)
        bkid = tbn.bcvt_get_bk39id(bcvt)
        verse_out = _handle(handlers2, verse)
        if bkid not in bk39s_out:
            bk39s_out[bkid] = []
        bk39s_out[bkid].append((bcvt, verse_out))
    return bk39s_out


def _get_bcvt_from_osis_id(vtrad, osid_id):
    bkid, chnu, vrnu = osis_book_abbrevs.get_bcv_from_osis_id(osid_id)
    return tbn.mk_bcvtxxx(bkid, chnu, vrnu, vtrad)


def _do_for_cant_dab(bkg_out, variant, root, cant_dab):
    bk39s = _process_book_group(variant, root, cant_dab)
    for bkid, verses in bk39s.items():
        if bkid not in bkg_out:
            bkg_out[bkid] = {}
        bkg_out[bkid][cant_dab] = verses


def _do_one_book_group(variant, bkg):
    """Do the book group bkg"""
    bkg_name = bkg["bkg-name"]
    root = _read_book_group(variant, bkg_name)
    bkg_out = {}
    if variant.get("variant-include-abcants"):
        cant_dabs = _ALL_3_CANT_DAB_VALUES
    else:
        cant_dabs = ("rv-cant-combined",)
    for cant_dab in cant_dabs:
        _do_for_cant_dab(bkg_out, variant, root, cant_dab)
    for bkid, cant_to_verses in bkg_out.items():
        sef_bkna = sef_cmn.SEF_BKNA[bkid]
        csv_path = write_utils.bkg_path(variant, sef_bkna)
        write_utils_sef_or_ajf.write_bkg_in_csv_fmt(
            csv_path, variant, cant_to_verses, cant_dabs
        )
        write_utils.write_bkg_in_un_fmt(
            variant, sef_bkna, cant_to_verses, "rv-cant-combined"
        )


_ALL_3_CANT_DAB_VALUES = "rv-cant-combined", "rv-cant-alef", "rv-cant-bet"
