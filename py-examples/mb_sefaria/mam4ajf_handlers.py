"""Exports HANDLERS"""

# jobj: JSON dict
# ofc1: output for all children, summed together
# ofc2: output for all children, per child

from mb_cmn import hebrew_punctuation as hpu


def _verse(jobj, ofc1, _ofc2):
    return ofc1 + _maybe_sampe(jobj)


def _text(jobj, _ofc1, _ofc2):
    return [jobj["text"]]


def _samekh2_or_3(_etel, _ofc1, _ofc2):
    return [" {ס} "]


def _pe2_or_3(_etel, _ofc1, _ofc2):
    return [" {פ} "]


def _samekh3_nin(_etel, _ofc1, _ofc2):
    """Handle a samekh3 element with class "nu10-invnun-neighbor" """
    return [" "]


def _invnun(jobj, _ofc1, _ofc2):
    """
    Handle either of the following two types of invnun elements:

        Type 1: a default (i.e., no trailing space) invnun element.
        These are the two Numbers 10 invnuns,
        at the start of verse 35 and the end of verse 36.

        Type 2: an invnun element with class "including-trailing-space"
        These are the 7 Psalm 107 invnuns,
        at the start of verses 23-28 and 40.
    """
    maybe_sp_dic = {"including-trailing-space": " ", None: ""}
    maybe_sp = maybe_sp_dic[jobj.get("class")]
    return [hpu.NUN_HAF + maybe_sp]


def _legarmeih(_etel, _ofc1, _ofc2):
    return [hpu.PASOLEG]


def _paseq(_etel, _ofc1, _ofc2):
    return [hpu.PASOLEG + hpu.PASOLEG]


def _empty(_etel, _ofc1, _ofc2):
    return []


def _pass_thru(_etel, ofc1, _ofc2):
    return ofc1


def _ketiv_qere(jobj, _ofc1, ofc2):
    assert len(ofc2) == 2
    sep_dic = {"sep-maqaf": hpu.MAQ, None: " "}
    separator = sep_dic[jobj.get("class")]
    # for AJF, we always use ketiv-then-qere ordering
    kq_dic = {c["type"]: val for c, val in ofc2}
    return [*kq_dic["kq-k"], separator, *kq_dic["kq-q"]]


def _ketiv(etel, ofc1, _ofc2):
    """
    Handle a ketiv element that is:
       * the ketiv part of a ketiv ve qere (common)
       * a ketiv velo qere (rare)
    """
    return _ketiv_or_qere_helper("()", ofc1)


def _k_velo_q_maq(_etel, _ofc1, _ofc2):
    """
    Handle the rare-within-rare (2 cases) of maqaf after ketiv velo qere.
    """
    return [hpu.MAQ]


def _qere(_etel, ofc1, _ofc2):
    """
    Handle a qere element that is:
       * the qere part of a ketiv ve qere (common)
       * a qere velo ketiv (rare)
    """
    return _ketiv_or_qere_helper("[]", ofc1)


def _scrdfftar(_jobj, _ofc1, ofc2):
    target, _note = [v for _, v in ofc2]
    return target


def _scrdfftar_target(_etel, ofc1, _ofc2):
    return ofc1


def _shirah_space(_etel, _ofc1, _ofc2):
    return [" "]


def _implicit_maqaf(_etel, _ofc1, _ofc2):
    return [hpu.MAQ]


#######################################################################
#######################################################################


def _ketiv_or_qere_helper(brackets, ofc1):
    return [brackets[0], *ofc1, brackets[1]]


def _maybe_sampe(jobj):
    ews = jobj.get("ends-with-sampe")
    if ews is None:
        return []
    sampe_fn_dic = {
        "samekh2": _samekh2_or_3,
        "samekh3": _samekh2_or_3,
        "pe2": _pe2_or_3,
        "pe3": _pe2_or_3,
    }
    sampe_fn = sampe_fn_dic[ews]
    return sampe_fn(None, None, None)


_HANDLERS_0 = {
    ("verse", None): _verse,
    ("text", None): _text,
    #
    ("good-ending", None): _empty,
    ("letter-small", None): _pass_thru,
    ("letter-large", None): _pass_thru,
    ("letter-hung", None): _pass_thru,
    #
    ("kq-k-velo-q", None): _ketiv,
    ("kq-k-velo-q-maq", None): _k_velo_q_maq,
    ("kq-q-velo-k", None): _qere,
    ("kq", None): _ketiv_qere,
    ("kq", "sep-maqaf"): _ketiv_qere,
    ("kq-k", None): _ketiv,
    ("kq-q", None): _qere,
    ("kq-trivial", None): _pass_thru,
    #
    ("cant-combined", None): _empty,
    ("cant-alef", None): _empty,
    ("cant-bet", None): _empty,
    ("cant-all-three", None): _pass_thru,
    #
    ("spi-samekh2", None): _samekh2_or_3,
    ("spi-samekh3", None): _samekh2_or_3,
    ("spi-samekh3", "nu10-invnun-neighbor"): _samekh3_nin,
    ("spi-pe2", None): _pe2_or_3,
    ("spi-pe3", None): _pe2_or_3,
    ("spi-invnun", None): _invnun,
    ("spi-invnun", "including-trailing-space"): _invnun,
    ("shirah-space", None): _shirah_space,
    ("lp-legarmeih", None): _legarmeih,
    ("lp-paseq", None): _paseq,
    ("implicit-maqaf", None): _implicit_maqaf,
    #
    ("scrdfftar", None): _scrdfftar,
    ("sdt-target", None): _scrdfftar_target,
    ("sdt-note", None): _empty,
    #
    ("slh-word", None): _pass_thru,
}
_HANDLERS_CANT_DUAL = {**_HANDLERS_0, ("cant-combined", None): _pass_thru}
_HANDLERS_CANT_ALEF = {**_HANDLERS_0, ("cant-alef", None): _pass_thru}
_HANDLERS_CANT_BET = {**_HANDLERS_0, ("cant-bet", None): _pass_thru}
HANDLERS = {
    "rv-cant-combined": _HANDLERS_CANT_DUAL,
    "rv-cant-alef": _HANDLERS_CANT_ALEF,
    "rv-cant-bet": _HANDLERS_CANT_BET,
}
