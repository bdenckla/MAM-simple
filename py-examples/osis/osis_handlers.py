"""Exports HANDLERS, child_handlers"""

from mb_misc import slh_description
from mb_cmn import str_defs as sd
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import shrink
from osis import osis_namespace as osisn


def child_handlers(tag_and_class):
    """Return the handlers appropriate for children of tag_and_class."""
    if tag_and_class == ("sdt-note", None):
        return _HANDLERS_INSIDE_NOTE
    return HANDLERS


# etel: ElementTree element
# ofc1: output for all children, summed together
# ofc2: output for all children, per child


def _bk24(etel, ofc1, _ofc2):
    # In MAM XML, every bk39 is inside a bk24.
    # In contrast, in MAM OSIS, we allow the equivalent of a bk39
    # (a div with type "book")
    # to exist alongside the equivalent of a bk24
    # (a div with type "bookGroup").
    bk39s = etel.findall("./book39")
    assert bk39s
    if len(bk39s) == 1:
        # Here we ignore the bk24 level, returning only its contents.
        return ofc1
    # Here we "respect" the bk24 level, since it has multiple bk39s
    # below it.
    attr = {"type": "bookGroup", "scope": _scope(bk39s)}
    return _singleton("div", attr, ofc1)


def _bk39(etel, ofc1, _ofc2):
    attr = {"type": "book", "osisID": etel.attrib["osisID"]}
    return _singleton("div", attr, ofc1)


def _chapter(etel, ofc1, _ofc2):
    attr = {"osisID": etel.attrib["osisID"]}
    return _singleton("chapter", attr, ofc1)


def _verse(etel, ofc1, _ofc2):
    attr = {"osisID": etel.attrib["osisID"]}
    return _singleton("verse", attr, ofc1)


def _text(etel, _ofc1, _ofc2):
    return [etel.attrib["text"]]


def _samekh2(_etel, _ofc1, _ofc2):
    """Handle a double-samekh (סס) element"""
    return [
        osisn.etel_ons("lb", {"type": "x-samekh-type-1"}),
        _seg_with_text("x-space-samekh-type-1", sd.OCTO_NBSP),
    ]


def _samekh3(_etel, _ofc1, _ofc2):
    """Handle a triple-samekh (ססס) element"""
    return [_seg_with_text("x-space-samekh-type-2", sd.OCTO_NBSP)]


def _pe2(_etel, _ofc1, _ofc2):
    """
    Handle a double-pe (פפ) element.
    We only distinguish double-pe from triple-pe by type.
    They won't appear (i.e. they won't be rendered) distinctly unless
    someone applies distinct CSS to them.
    """
    el_lb = osisn.etel_ons("lb", {"type": "x-pe-type-1"})
    return [el_lb, el_lb]


def _pe3(_etel, _ofc1, _ofc2):
    """
    Handle a triple-pe (פפפ) element.
    We only distinguish double-pe from triple-pe by type.
    They won't appear (i.e. they won't be rendered) distinctly unless
    someone applies distinct CSS to them.
    """
    el_lb = osisn.etel_ons("lb", {"type": "x-pe-type-2"})
    return [el_lb, el_lb]


def _samekh3_nin(_etel, _ofc1, _ofc2):
    """
    Handle a triple-samekh (ססס) element with class "nu10-invnun-neighbor"
    These are inside the two Numbers 10 invnuns. Those invnuns are
    at the start of verse 35 and the end of verse 36.
    """
    return [_seg_with_text("x-space-nu10-invnun-neighbor", sd.NBSP)]


def _invnun(etel, _ofc1, _ofc2):
    """
    Handle either of the following two types of invnun elements:

        Type 1: a default (i.e., no trailing space) invnun element.
        These are the two Numbers 10 invnuns,
        at the start of verse 35 and the end of verse 36.

        Type 2: an invnun element with class "including-trailing-space"
        These are the 7 Psalm 107 invnuns,
        at the start of verses 23-28 and 40.
    """
    maybe_nbsp_dic = {"including-trailing-space": sd.NBSP, None: ""}
    maybe_nbsp = maybe_nbsp_dic[etel.attrib.get("class")]
    return [hpu.NUN_HAF + maybe_nbsp]


def _legarmeih(_etel, _ofc1, _ofc2):
    return [sd.THSP + hpu.PASOLEG]


def _paseq(_etel, _ofc1, _ofc2):
    attr = {"type": "x-paseq"}
    note_el = _etel_ons_with_text("note", attr, "פסק ולא לגרמיה")
    return [sd.NBSP + hpu.PASOLEG, note_el, " "]


def _good_ending(_etel, ofc1, _ofc2):
    return [osisn.etel_ons("lb"), *_singleton_seg("x-good-ending", ofc1)]


def _letter_small(_etel, ofc1, _ofc2):
    return _singleton_seg("x-small", ofc1)


def _letter_large(_etel, ofc1, _ofc2):
    # I guess we use "x-big" rather than "x-large" because "x-big" is a
    # closer analogy to HTML's "big".
    return _singleton_seg("x-big", ofc1)


def _letter_hung(_etel, ofc1, _ofc2):
    # A <hi type="super"> element is not ideal because it will often be
    # styled as smaller than normal text. Although we used to use "super",
    # we stopped using "super" when we added slh word notes. This only
    # affects four words, by the way.
    # return _singleton('hi', {'type': 'super'}, ofc1)
    return _singleton_seg("x-hung", ofc1)


def _empty(_etel, _ofc1, _ofc2):
    return []


def _pass_thru(_etel, ofc1, _ofc2):
    return ofc1


def _ketiv_qere(etel, _ofc1, ofc2):
    assert len(ofc2) == 2
    sep_dic = {"sep-maqaf": hpu.MAQ, None: " "}
    separator = sep_dic[etel.attrib.get("class")]
    kq_or_qk = tuple(ofc2.values())
    return [*kq_or_qk[0], separator, *kq_or_qk[1]]


def _ketiv(_etel, ofc1, _ofc2):
    """
    Handle a normal ketiv element, i.e. one that is the ketiv part of a
    ketiv/qere pair. I.e., one that is NOT a ketiv velo qere.
    """
    return _bracket("()", ofc1)


def _ketiv_velo_qere(_etel, ofc1, _ofc2):
    """
    Handle a ketiv velo qere.
    """
    return _ketiv_velo_qere_amx(ofc1)


def _ketiv_velo_qere_maq(_etel, ofc1, _ofc2):
    """
    Handle the rare-within-rare case of a maqaf needed after a ketiv velo qere.
    """
    return [hpu.MAQ]


def _qere(_etel, ofc1, _ofc2):
    """
    Handle a normal qere element, i.e. one that is the qere part of a
    ketiv/qere pair. I.e., one that is NOT a qere velo ketiv.
    """
    return _bracket("[]", ofc1)


def _qere_velo_ketiv(_etel, ofc1, _ofc2):
    """
    Handle a qere velo ketiv.
    """
    return _singleton_seg("x-qere-velo-ketiv", _bracket("[]", ofc1))


def _slh_word(etel, ofc1, _ofc2):
    desc3_es = etel.attrib["slhw-desc-3"]
    desc3 = slh_description.desc3_decoded_from_a_str(desc3_es)
    desc_parts = (
        etel.attrib["slhw-desc-0"],
        etel.attrib["slhw-desc-1"],
        etel.attrib["slhw-desc-2"],
        desc3,
    )
    desc_str = slh_description.desc_parts_shown_as_a_str(desc_parts)
    attr = {"type": "x-slh-word"}
    note = _singleton("note", attr, [desc_str])
    return ofc1 + note


def _scrdfftar(etel, _ofc1, ofc2):
    target, note = ofc2.values()
    attr = {"type": "x-scroll-difference"}
    note2 = _singleton("note", attr, note)
    starpos = etel.attrib["sdt-starpos"]
    assert starpos in ("before-word", "after-word")
    maybe_note_0 = note2 if starpos == "before-word" else []
    maybe_note_1 = note2 if starpos == "after-word" else []
    return maybe_note_0 + target + maybe_note_1


def _scrdfftar_target(_etel, ofc1, _ofc2):
    return ofc1


def _scrdfftar_note(_etel, ofc1, _ofc2):
    return ofc1


def _shirah_space(_etel, _ofc1, _ofc2):
    return [_seg_with_text("x-space-shirah-space", sd.OCTO_NBSP)]


def _implicit_maqaf(_etel, _ofc1, _ofc2):
    return [_seg_with_text("x-implicit-maqaf", hpu.MAQ)]


#######################################################################
#######################################################################


def _bracket(brackets, ofc1):
    return shrink.shrink([brackets[0], *ofc1, brackets[1]])


def _ketiv_velo_qere_amx(ofc1):
    return _singleton_seg("x-ketiv-velo-qere", _bracket("()", ofc1))


def _scope(bk39_etels):
    first_id = bk39_etels[0].attrib["osisID"]
    last_id = bk39_etels[-1].attrib["osisID"]
    return first_id + "-" + last_id  # e.g. 1Chr-2Chr


def _singleton_seg(seg_type: str, ofc1):
    return _singleton("seg", {"type": seg_type}, ofc1)


def _seg_with_text(seg_type: str, the_text: str):
    return _etel_ons_with_text("seg", {"type": seg_type}, the_text)


def _singleton(tag, attr, ofc1):
    etel = osisn.etel_ons(tag, attr)
    _my_extend(etel, ofc1)
    return [etel]


def _etel_ons_with_text(tag: str, attr, text):
    etel = osisn.etel_ons(tag, attr)
    etel.text = text
    return etel


def _my_extend(etel, ofc1):
    if ofc1 and isinstance(ofc1[0], str):
        assert etel.text is None
        etel.text = ofc1[0]
        etel.extend(ofc1[1:])
    else:
        etel.extend(ofc1)


HANDLERS = {
    ("book24", None): _bk24,
    ("book39", None): _bk39,
    ("chapter", None): _chapter,
    ("verse", None): _verse,
    ("text", None): _text,
    #
    ("good-ending", None): _good_ending,
    ("letter-small", None): _letter_small,
    ("letter-large", None): _letter_large,
    ("letter-hung", None): _letter_hung,
    #
    ("kq-k-velo-q", None): _ketiv_velo_qere,
    ("kq-k-velo-q-maq", None): _ketiv_velo_qere_maq,
    ("kq-q-velo-k", None): _qere_velo_ketiv,
    ("kq", None): _ketiv_qere,
    ("kq", "sep-maqaf"): _ketiv_qere,
    ("kq-k", None): _ketiv,
    ("kq-q", None): _qere,
    ("kq-trivial", None): _pass_thru,
    #
    ("cant-combined", None): _pass_thru,
    ("cant-alef", None): _empty,
    ("cant-bet", None): _empty,
    ("cant-all-three", None): _pass_thru,
    #
    ("spi-samekh2", None): _samekh2,
    ("spi-samekh3", None): _samekh3,
    ("spi-samekh3", "nu10-invnun-neighbor"): _samekh3_nin,
    ("spi-pe2", None): _pe2,
    ("spi-pe3", None): _pe3,
    ("spi-invnun", None): _invnun,
    ("spi-invnun", "including-trailing-space"): _invnun,
    ("shirah-space", None): _shirah_space,
    ("lp-legarmeih", None): _legarmeih,
    ("lp-paseq", None): _paseq,
    ("implicit-maqaf", None): _implicit_maqaf,
    #
    ("scrdfftar", None): _scrdfftar,
    ("sdt-target", None): _scrdfftar_target,
    ("sdt-note", None): _scrdfftar_note,
    #
    ("slh-word", None): _slh_word,
}
_HANDLERS_INSIDE_NOTE = {
    **HANDLERS,
    # Below, we override the slh word handler to be simply a pass thru
    # because we don't want a note within a note!
    ("slh-word", None): _pass_thru,
}
