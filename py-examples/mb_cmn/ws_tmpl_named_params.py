import re
from mb_cmn.my_utils import sl_map
from mb_cmn.my_utils import dv_map


def simplify_singletons(tmpl2_args):
    assert isinstance(tmpl2_args, list)
    return sl_map(simplify_singleton, tmpl2_args)


def get_tmpl_params(tmpl2_args):
    assert isinstance(tmpl2_args, list)
    return dv_map(simplify_singleton, get_tmpl_params_ss(tmpl2_args))


def get_tmpl_params_ss(tmpl2_args):
    # ss: sans simplification, i.e. without simplification
    assert isinstance(tmpl2_args, list)
    return dict(sl_map(_dictify_one, enumerate(tmpl2_args)))


def simplify_singleton(tmpl2_arg):
    assert isinstance(tmpl2_arg, list)
    if len(tmpl2_arg) == 1:
        assert not isinstance(tmpl2_arg[0], list)
        return tmpl2_arg[0]
    return tmpl2_arg


_DIGITS_1_TO_9 = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}


def _dictify_one(enumerate_item):
    arg_idx, arg = enumerate_item
    arg_num_str = str(arg_idx + 1)
    assert isinstance(arg, list)
    if arg == [] or not isinstance(arg[0], str):
        return arg_num_str, arg
    arg0 = arg[0]
    if match := re.fullmatch(r"(.+?)=(.*)", arg0):
        lhs = match.group(1)
        rhs = match.group(2)
        if lhs in _DIGITS_1_TO_9:
            # Somewhat arbitrarily, we only check single-digit numbered args.
            assert arg_num_str == lhs
        if rhs == "":
            return lhs, arg[1:]
        return lhs, [rhs, *arg[1:]]
    return arg_num_str, arg
