"""Exports functions that help create and use templates"""

from mb_cmn import hebrew_punctuation as hpu
from mb_cmn.my_utils import first_and_only
from mb_cmn.my_utils import sl_map


def template_elements(tmpl):
    """Return all elements."""
    return tmpl.get("tmpl") or _stmpl_elements(tmpl)


def template_element(tmpl: dict, idx: int):
    """Return template element at index."""
    return template_elements(tmpl)[idx]


def template_i0(tmpl, idx: int):
    """Return element 0 of element idx of the given template."""
    return first_and_only(template_element(tmpl, idx))


def template_arguments(tmpl):
    """Return the second & any further elements."""
    return template_elements(tmpl)[1:]


def template_len(tmpl):
    """Return the length of the template."""
    return len(template_elements(tmpl))


def template_name(tmpl):
    """Return normalized template name from element 0.

    The ASCII double-quote shorthand is normalized to Hebrew gershayim
    (U+05F4). This applies to both tmpl and stmpl template representations.
    """
    el0 = template_element(tmpl, 0)
    if len(el0) == 2:
        assert el0[0] == "#בלי קטע:"
        assert template_elements(el0[1]) == [["שם הדף המלא"]]
    return _normalize_template_name(el0[0])


def is_template(wtel):
    """Return whether wtel is a template."""
    if isinstance(wtel, str):
        return False
    assert isinstance(wtel, dict)
    return dic_is_template(wtel)


def dic_is_template(dic: dict):
    """Return whether the given dict is a template."""
    return tuple(dic.keys()) in (("tmpl",), ("stmpl",))


def is_template_with_name(wtel, name):
    """Return whether wtel is a template with the given name."""
    return is_template(wtel) and template_name(wtel) == _normalize_template_name(name)


def is_template_with_name_in(wtel, names):
    """Return whether wtel is a template with on eof the given names."""
    return is_template(wtel) and template_name(wtel) in {
        _normalize_template_name(name) for name in names
    }


def is_doc_template(wtel):
    """Return whether wtel is a documentation template."""
    return is_template_with_name(wtel, "נוסח")


def mktmpl(elements):
    """Construct a template."""
    return simplify_wtel({"tmpl": elements})


def mktmpl_ma(foc, tmpl):  # ma: [with] mapped args
    """Map a foc (function or closure) over the args of a template."""
    tmpl_args = template_arguments(tmpl)
    return mktmpl([[template_name(tmpl)], *sl_map(foc, tmpl_args)])


def is_abtag(wtel):
    """Return whether wtel is an abtag."""
    return isinstance(wtel, dict) and list(wtel.keys()) == ["custom_tag"]


def _stmpl_elements(stmpl):
    return list(map(_make_singleton, stmpl["stmpl"].split("|")))


def _make_singleton(x):
    # Note that [x] is not the same as list(x) if x is an iterable, e.g. a string!
    return [x]


def named_template_element(tmpl: dict, idx: int, name: str):
    """
    For element ['foo=bar', 'baz'] at index, return ['bar', 'baz'].
    """
    return _strip_prefix(name + "=", template_element(tmpl, idx))


def simplify_wtel(wtel):
    if not is_template(wtel):
        return wtel
    tmpl_els_orig = template_elements(wtel)
    tmpl_els_simp_1 = list(map(_simplify_wtseq, tmpl_els_orig))
    if not all(map(_is_singleton, tmpl_els_simp_1)):
        return {"tmpl": tmpl_els_simp_1}
    tmpl_els_simp_2 = list(map(lambda x: x[0], tmpl_els_simp_1))
    simple_tmpl_str = "|".join(tmpl_els_simp_2)
    if len(simple_tmpl_str) > 100:
        return wtel
    return {"stmpl": simple_tmpl_str}


def _simplify_wtseq(tel):
    return list(map(simplify_wtel, tel))


def _is_singleton(wtseq):
    return len(wtseq) == 1 and isinstance(wtseq[0], str) and "|" not in wtseq[0]


_Q2_TO_G2 = str.maketrans({'"': hpu.GERSHAYIM})


def _normalize_template_name(name):
    """Normalize template names for stable matching and reporting.

    Convert ASCII double quote shorthand (") to gershayim (U+05F4).
    """
    assert isinstance(name, str), name
    return name.translate(_Q2_TO_G2)


def _strip_prefix(prefix, in_list):
    """Strip prefix off first element of in_list"""
    # Example in_list/output table, assuming prefix='pre'
    #
    # in_list          | output
    # ---------------- | ------------
    # ['pre=foo']      | ['foo']
    # ['pre=foo', bar] | ['foo', bar]
    # ['pre=', bar]    | [bar]
    #
    assert isinstance(in_list, list)
    assert isinstance(in_list[0], str)
    assert in_list[0].startswith(prefix)
    new_el0 = in_list[0][len(prefix) :]
    return [new_el0] + in_list[1:] if new_el0 else in_list[1:]


SDT_ARG_IDX_FOR_TARG = 1
SDT_ARG_IDX_FOR_NOTE = 2
SDT_ARG_IDX_FOR_STARPOS = 3
#
SLHW_ARG_IDX_FOR_TARG = 1
SLHW_ARG_IDX_FOR_DESC0 = 2
SLHW_ARG_IDX_FOR_DESC1 = 3
SLHW_ARG_IDX_FOR_DESC2 = 4
SLHW_ARG_IDX_FOR_DESC3 = 5
