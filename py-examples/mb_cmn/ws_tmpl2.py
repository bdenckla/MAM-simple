"""Exports functions that help create and use templates"""

from mb_cmn import ws_tmpl1 as wtp1
from mb_cmn import ws_tmpl_named_params as wtnp
from mb_cmn import template_names as tmpln
from mb_cmn.my_utils import first_and_only
from mb_cmn.my_utils import ss_map
from mb_cmn.my_utils import sl_map
from mb_cmn.my_utils import dv_map
from mb_cmn.shrink import shrink


def template_element(tmpl: dict, idx: int):
    """Return template element at index. Template name is at index 0."""
    if idx == 0:
        return [tmpl["tmpl_name"]]
    return template_param_val(tmpl, str(idx))


def template_i0(tmpl, idx: int):
    """Return element 0 of element idx of the given template. Template name is at index 0."""
    return first_and_only(template_element(tmpl, idx))


def template_len(tmpl):
    """Return the length of the template, including the template name."""
    return 1 + len(list(template_param_keys(tmpl)))


def template_name(tmpl):
    return tmpl["tmpl_name"]


def is_template(wtel):
    """Return whether wtel is a template."""
    if isinstance(wtel, str):
        return False
    assert isinstance(wtel, dict)
    return dic_is_template(wtel)


def dic_is_template(dic: dict):
    """Return whether the given dict is a template."""
    return tuple(dic.keys()) in _TMPL_KEYTUPLES


def is_template_with_name(wtel, name):
    """Return whether wtel is a template with the given name."""
    return template_name_if_is_template(wtel) == name


def is_template_with_name_in(wtel, names):
    """Return whether wtel is a template with one of the given names."""
    return template_name_if_is_template(wtel) in names


def is_doc_template(wtel):
    """Return whether wtel is a documentation template."""
    return is_template_with_name(wtel, "נוסח")


def mktmpl(elements, *, ignore_equals=False):
    """Construct a template."""
    name = first_and_only(elements[0])
    args = elements[1:]
    if len(args) == 0:
        return {"tmpl_name": name}
    if name == "נוסח" and len(args[0]) == 0:
        # Various code expects the 1st arg to נוסח to be [''] not []
        # ([] often results from calling "shrink")
        # XXX TODO tweak that code to allow [''] or []
        return mktmpl([["נוסח"], [""], *args[1:]])
    if ignore_equals:
        tmpl_args = wtnp.simplify_singletons(args)
        isks = _int_str_keys(tmpl_args)
        tp_basic = dict(zip(isks, tmpl_args))
        return {"tmpl_name": name, "tmpl_params": tp_basic}
    tp_parsed = wtnp.get_tmpl_params(args)
    return {"tmpl_name": name, "tmpl_params": tp_parsed}


def template_name_if_is_template(wtel):
    return is_template(wtel) and wtel["tmpl_name"]


def template_param_val(tmpl, param_name: str):
    return _restore_one_singleton(tmpl["tmpl_params"][param_name])


def template_param_keys(tmpl):
    if tmpl_params := tmpl.get("tmpl_params"):
        return tmpl_params.keys()
    return []


def template_param_vals(tmpl):
    return [template_param_val(tmpl, key) for key in template_param_keys(tmpl)]


def mktmpl_mp(foc, tmpl):  # mp: [with] mapped params
    """Map a foc (function or closure) over the params of a template."""
    out = {"tmpl_name": template_name(tmpl)}
    if params := tmpl.get("tmpl_params"):
        new_params = dv_map(_restore_one_singleton, params)
        new_params = dv_map(foc, new_params)
        new_params = dv_map(wtnp.simplify_singleton, new_params)
        out = {**out, "tmpl_params": new_params}
    return out


def map_params(foc, tmpl):
    if params := tmpl.get("tmpl_params"):
        res_vals = map(_restore_one_singleton, params.values())
        return sl_map(foc, res_vals)
    return []


def mktmpl2_fr_tmpl1_els(tmpl1_els):
    """Construct a tmpl2 from the elements of a tmpl1."""
    return mktmpl(_use_tmpl2_in_tmpl1_els(tmpl1_els))


def use_tmpl2(wtel):
    """Use tmpl2 format for this wtel & below"""
    if wtp1.is_template(wtel):
        return mktmpl2_fr_tmpl1_els(wtp1.template_elements(wtel))
    return wtel


def use_tmpl2_in_wtseq(wtseq):
    """Use tmpl2 format in the given wtseq."""
    assert isinstance(wtseq, (tuple, list))
    return ss_map(use_tmpl2, wtseq)


def is_scrdff_template(wtel):
    """Return whether wtel is a scrdff template."""
    return is_template_with_name(wtel, tmpln.SCRDFF_NO_TAR)


SDT_EL_IDX_FOR_TARG = 1
SDT_EL_IDX_FOR_NOTE = 2
SDT_EL_IDX_FOR_STARPOS = 3
#
SLHW_EL_IDX_FOR_TARG = 1
SLHW_EL_IDX_FOR_DESC0 = 2
SLHW_EL_IDX_FOR_DESC1 = 3
SLHW_EL_IDX_FOR_DESC2 = 4
SLHW_EL_IDX_FOR_DESC3 = 5


def _int_str_keys(seq):
    """Return a list of stringified integers from 1 to len(seq)."""
    return list(map(str, range(1, 1 + len(seq))))


def _restore_one_singleton(tmpl2_arg):
    if isinstance(tmpl2_arg, (dict, str)):
        return [tmpl2_arg]
    assert isinstance(tmpl2_arg, list)
    return tmpl2_arg


def _use_tmpl2_in_tmpl1_els(tmpl1_els):
    assert isinstance(tmpl1_els, list)
    return sl_map(use_tmpl2_in_wtseq, tmpl1_els)


_TMPL_KEYTUPLES = {
    ("tmpl_name",),
    ("tmpl_name", "tmpl_params"),
}
