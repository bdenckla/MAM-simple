"""Coalesce adjacent strings in mixed iterables."""

import copy
import xml.etree.ElementTree as ET

__all__ = ["shrink", "shrink_xml"]


def shrink(parts):
    """
    Coalesce (or "collapse") adjacent strings in an iterable whose parts are
    a mix of strings and non-strings.
    """
    acc = []
    for part in parts:
        if part == "":
            continue
        if acc and _both_str(acc[-1], part):
            acc[-1] += part
            continue
        acc.append(part)
    type_of_parts = type(parts)  # presumably list or tuple
    return type_of_parts(acc)


def shrink_xml(parts):
    """
    Coalesce (or "collapse") adjacent strings in an iterable whose parts are
    a mix of strings and ET.Elements.
    """
    acc = []
    for part in parts:
        if part == "":
            continue
        if acc and isinstance(part, str):
            _append_to_last(acc, part)
            continue
        assert isinstance(part, (ET.Element, str))
        acc.append(part)
    type_of_parts = type(parts)  # presumably list or tuple
    return type_of_parts(acc)


def shrextend(accum, objs):
    """Extend accum with objs."""
    for obj in objs:
        shrappend(accum, obj)


def shrappend(accum, obj):
    """Append obj to accum."""
    if accum and _both_str(accum[-1], obj):
        accum[-1] += obj
    elif obj != "":
        accum.append(obj)


def _both_str(obj1, obj2):
    return isinstance(obj1, str) and isinstance(obj2, str)


def _append_to_last(acc, part):
    if isinstance(acc[-1], ET.Element):
        acc[-1] = copy.deepcopy(acc[-1])
        if acc[-1].tail is None:
            acc[-1].tail = part
        else:
            acc[-1].tail += part
        return
    assert isinstance(acc[-1], str)
    acc[-1] += part
