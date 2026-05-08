from mb_misc import hebrew_letter_names as hln
from mb_misc import hebrew_letter_words as hlw
from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import str_defs as sd
from mb_cmn import my_utils


def get_parts(wtseq):
    """Describe the small, large, and hung parts of wtseq in 4 parts"""
    desc0123 = "", "", "", []
    for wtel in wtseq:
        desc0123 = _add(desc0123, _slh_parts_for_wtel(wtel))
    return desc0123


def desc_parts_shown_as_a_str(parts):
    """Show a full slh description as a human-friendly string."""
    desc3_shown = _desc3_shown_as_a_str(parts[3])
    return "/".join(parts[0:3]) + " " + desc3_shown


def desc3_encoded_as_a_str(desc3):
    """Encode a desc3 as a (not that human-friendly) string."""
    # Below, "es" means "encoded as a string"
    desc3_elements_es = ["/".join(e) for e in desc3]
    # E.g., desc3_elements_as_strs = ['ו/ג', 'ז/ק']
    desc3_es = ",".join(desc3_elements_es)
    # E.g. desc3_es = 'ו/ג,ז/ק'
    return desc3_es


def desc3_decoded_from_a_str(desc3_es):
    """Decode desc3 from a string to a list of pairs."""
    desc3_elements_es = desc3_es.split(",")
    desc3 = [pair_str.split("/") for pair_str in desc3_elements_es]
    return desc3


def _desc3_shown_as_a_str(desc3):
    """Show a desc3 as a human-friendly string."""
    list_of_results = tuple(map(_slh_desc_single, desc3))
    return "(" + ", ".join(list_of_results) + ")"


def _slh_parts_for_wtel(wtel):
    if wtp.is_template(wtel):
        return _slh_parts_for_tmpl(wtel)
    assert isinstance(wtel, str)
    desc1 = _periods_and_maqafs(hlw.letters_and_maqafs(wtel))
    return wtel, desc1, "", []


PASOLEG_DESC0 = {
    "מ:לגרמיה-2": hpu.PASOLEG,
    "מ:לגרמיה": hpu.PASOLEG,
    "מ:פסק": sd.DOUB_VERT_LINE,
}


def _slh_parts_for_tmpl(tmpl):
    # Below, מ:פסק is needed only for משלי ל,טו (Proverbs 30:15) in old
    # versions of MAM. At some point that paseq was converted to a legarmeih.
    # Similarly, מ:לגרמיה ("classic" legarmeih) is only needed for old versions of MAM.
    tmpl_name = wtp.template_name(tmpl)
    if tmpl_name in PASOLEG_DESC0:
        return PASOLEG_DESC0[tmpl_name], ".", "", []
    tmpl_el1 = wtp.template_element(tmpl, 1)
    if len(tmpl_el1) > 1:
        assert len(tmpl_el1) == 2
        assert wtp.template_name(tmpl_el1[1]) in ("מ:לגרמיה-2", "מ:לגרמיה")
    desc1_code = _DESC1_CODE[tmpl_name]  # qof, gimel, or tav
    desc0 = tmpl_el1[0]
    desc1 = hlw.letters_and_maqafs(desc0)
    desc2 = desc1_code * len(desc1)
    desc3 = [(desc1, desc1_code)]
    return desc0, desc1, desc2, desc3


def _periods_and_maqafs(string):
    parts = string.split(hpu.MAQ)
    return hpu.MAQ.join(_periods(part) for part in parts)


def _periods(string):
    return "." * len(string)


def _add(tup1, tup2):
    return tuple(a + b for a, b in my_utils.szip(tup1, tup2))


def _slh_desc_single(desc3_element):
    the_letters, desc1_code = desc3_element
    is_single = len(the_letters) == 1
    ot_or_otot = "אות" if is_single else "אותות"
    parts = (ot_or_otot, _letter_names(the_letters), _adjective(desc1_code, is_single))
    return " ".join(parts)


def _letter_names(the_letters):
    l_to_ln = hln.DIC_OF_LETTERS_TO_LETTER_NAMES_G2
    names = tuple(l_to_ln[letter] for letter in the_letters)
    return ", ".join(names)


def _adjective(desc1_code, is_single):
    adj1, adjn = _ADJECTIVES[desc1_code]
    return adj1 if is_single else adjn


_DESC1_CODE = {
    "מ:אות-ק": "ק",
    "מ:אות-ג": "ג",
    "מ:אות תלויה": "ת",
}
_ADJECTIVES = {
    "ק": ("קטנה", "קטנות"),
    "ג": ("גדולה", "גדולות"),
    "ת": ("תלויה", "תלויות"),
}
