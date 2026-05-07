"""Exports various HTML utilities"""

import xml.etree.ElementTree as ET
import re
from dataclasses import dataclass
from typing import Union

from mb_cmn import file_io
from mb_misc import mb_html_get_lines
from mb_cmn import str_defs as sd
from mb_cmn.my_utils import st_map
from mb_cmn.my_utils import sum_of_map
from mb_cmn import shrink


@dataclass
class WriteCtx:
    """Holds info needed to write HTML to a file."""

    title: str
    path: str
    head_style: Union[str, None] = None
    css_hrefs: tuple = ()
    body_class: Union[str, None] = None
    add_wbr: bool = False
    html_comment: Union[str, None] = None


def write_html_to_file(body_contents, wc: WriteCtx):
    """
    Write HTML to file based on the following inputs:
        * a body contents
        * a "write context" structure containing:
            * a title
            * an output path
    """
    other = {"head_style": wc.head_style, "body_class": wc.body_class}
    html_el = html_el2(wc.title, body_contents, wc.css_hrefs, other=other)
    file_io.with_tmp_openw(
        wc.path, {}, _write_callback, wc.add_wbr, wc.html_comment, html_el
    )


def el_to_str_for_sef(html_el):
    hgl_opts = {
        "hgl-add-wbr": False,
        "hgl-max-line-len": -1,
        "hgl-line-breaks-allowed": False,
    }
    lines = mb_html_get_lines.get_lines_from_html_el(hgl_opts, html_el)
    assert len(lines) == 1
    return lines[0]


def add_htel_to_etxml(etxml_parent, htel):
    """
    Add our proprietary-format HTML/XML element "htel"
    to the ElementTree-format element xml_parent.
    """
    if isinstance(htel, str):
        ET.SubElement(etxml_parent, "text", {"text": htel})
        return
    attr = htel.get("attr") or {}
    tmp_attr = attr
    if contents := htel.get("contents"):
        assert isinstance(contents, (tuple, list))
        if _is_text_singleton(contents):
            assert "text" not in attr
            tmp_attr = dict(attr, text=contents[0])
            contents = None
    xml_elem = ET.SubElement(etxml_parent, htel_get_tag(htel), tmp_attr)
    if contents:
        for contents_el in contents:
            add_htel_to_etxml(xml_elem, contents_el)


def html_el2(title_text, body_contents, css_hrefs=(), other=None):
    """Make an <html> element."""
    other_defaults = {"lang": "en", "head_style": None, "body_class": None}
    if other is None:
        other = {}
    other = {**other_defaults, **other}
    meta = htel_mk("meta", attr={"charset": "utf-8"})
    title = htel_mk("title", flex_contents=(title_text,))
    links_to_css = st_map(_link_to_css, css_hrefs)
    if other["head_style"] is None:
        style_els = ()
    else:
        style_el = htel_mk("style", flex_contents=(other["head_style"],))
        style_els = (style_el,)
    head_cont = (meta, title) + style_els + links_to_css
    _head = htel_mk("head", flex_contents=head_cont)
    body_attr = {"class": other["body_class"]} if other["body_class"] else None
    _body = htel_mk("body", attr=body_attr, flex_contents=body_contents)
    return _html_el1({"lang": other["lang"]}, (_head, _body))


def para(contents, attr=None):
    """Make a <p> element."""
    return htel_mk("p", attr=attr, flex_contents=contents)


def blockquote(contents, attr=None):
    """Make a <blockquote> element."""
    return htel_mk("blockquote", attr=attr, flex_contents=contents)


def img(attr=None):
    """Make an <img> element."""
    return htel_mk("img", attr=attr)


def caption(contents):
    """Make a <caption> element."""
    return htel_mk("caption", flex_contents=contents)


def table_row(contents, attr=None):
    """Make a <tr> element."""
    return htel_mk("tr", attr=attr, flex_contents=contents)


def table_row_of_data(tdconts, tdattrs=None):
    """Make a <tr> element containing <td> elements."""
    # tdcont: table datum contents
    # tdconts: a sequence where each element is a tdcont
    if tdattrs is None:
        tdattrs = (None,) * len(tdconts)
    return table_row(st_map(table_datum2, zip(tdconts, tdattrs)))


def table_row_of_headers(thconts):
    """Make a <tr> element containing <th> elements."""
    # thcont: table header contents
    # thconts: a sequence where each element is a thcont
    return table_row(st_map(table_header, thconts))


def table_datum2(contents_and_attr):
    return table_datum(*contents_and_attr)


def table_datum(contents, attr=None):
    """Make a <td> (table datum cell) element."""
    return htel_mk("td", attr, contents)


def table_header(contents, attr=None):
    """Make a <th> (table header cell) element."""
    return htel_mk("th", attr, contents)


def div(contents, attr=None):
    """Make a <div> element."""
    return htel_mk("div", attr=attr, flex_contents=contents)


def table(contents, attr=None):
    """Make a <table> element."""
    return htel_mk("table", attr, contents)


def unordered_list(liconts, attr=None):
    """Make a <ul> element."""
    # licont: list item contents
    # liconts: a tuple where each element is a licont
    return htel_mk("ul", attr, st_map(_list_item, liconts))


def ordered_list(liconts, attr=None):
    """Make an <ol> element."""
    # licont: list item contents
    # liconts: a tuple where each element is a licont
    return htel_mk("ol", attr, st_map(_list_item, liconts))


def heading_level_1(contents, attr=None):
    """Make an <h1> element."""
    return htel_mk("h1", attr, contents)


def heading_level_2(contents, attr=None):
    """Make an <h2> element."""
    return htel_mk("h2", attr, contents)


def heading_level_3(contents, attr=None):
    """Make an <h3> element."""
    return htel_mk("h3", attr, contents)


def anchor(contents, attr=None):
    """Make an <a> element."""
    return htel_mk("a", attr, contents)


def colgroup(contents, attr=None):
    """Make a <colgroup> element."""
    return htel_mk("colgroup", attr, contents)


def col(attr=None):
    """Make a <col> element."""
    return htel_mk("col", attr=attr)


def span(contents, attr=None):
    """Make a <span> element."""
    return htel_mk("span", attr=attr, flex_contents=contents)


def emphasis(contents, attr=None):
    """Make an <em> (emphasis) element."""
    return htel_mk("em", attr=attr, flex_contents=contents)


def abbr(contents, attr=None):
    """Make an <abbr> (abbreviation) element."""
    return htel_mk("abbr", attr, contents)


def span_c(contents, the_class=None):
    """Make a <span> element, given a value for the "class" attr."""
    return span(contents, the_class and {"class": the_class})


def bold(contents, attr=None):
    """Make a <bold> element."""
    return htel_mk("b", attr=attr, flex_contents=contents)


def italic(contents, attr=None):
    """Make a <italic> element."""
    return htel_mk("i", attr=attr, flex_contents=contents)


def small(contents, attr=None):
    """Make a <small> element."""
    return htel_mk("small", attr=attr, flex_contents=contents)


def big(contents, attr=None):
    """Make a <big> element."""
    return htel_mk("big", attr=attr, flex_contents=contents)


def sup(contents, attr=None):
    """Make a <sup> (superscript) element."""
    return htel_mk("sup", attr=attr, flex_contents=contents)


def sub(contents, attr=None):
    """Make a <sub> (subscript) element."""
    return htel_mk("sub", attr=attr, flex_contents=contents)


def bdi(contents, attr=None):
    """Make a <bdi> element."""
    return htel_mk("bdi", attr, contents)


def code(contents, attr=None):
    """Make a <code> (inline code) element."""
    return htel_mk("code", attr=attr, flex_contents=contents)


def horizontal_rule(attr=None):
    """
    Make a <hr> element
    """
    return htel_mk("hr", attr=attr)


def line_break(attr=None):
    """
    Make a <br> element
    """
    return htel_mk("br", attr=attr)


def flatten(flex_contents):
    if _is_str_or_htel(flex_contents):
        return [flex_contents]
    if isinstance(flex_contents, (tuple, list)):
        return sum_of_map(flatten, flex_contents)
    assert flex_contents is None, flex_contents
    return None


def htel_mk(tag: str, attr=None, flex_contents=None):
    """Make an HTML element"""
    assert isinstance(tag, str)
    assert isinstance(attr, (type(None), dict))
    flat_contents = flatten(flex_contents)
    fs_contents = flat_contents and shrink.shrink(flat_contents)
    if not (attr and "lt-space-okay" in attr):
        _do_space_asserts(tag, fs_contents)
    opts1 = {
        "attr": attr,
        "contents": fs_contents,
    }
    opts2 = {k: v for k, v in opts1.items() if v is not None}
    return {"_htel_tag": tag, **opts2}


def anchor_h(contents, href_val):
    return anchor(contents, {"href": href_val})


def htel_get_tag(html_el):
    """Get the tag of an HTML element."""
    return html_el["_htel_tag"]


def htel_get_class_attr(html_el):
    """Get the class attribute of an HTML element."""
    return html_el["attr"]["class"]


def is_htel(obj):
    return isinstance(obj, dict) and "_htel_tag" in obj


def is_raw_html(obj):
    """Return True for raw-HTML leaf dicts created by raw_html()."""
    return isinstance(obj, dict) and "_raw_html" in obj


def raw_html(html_str: str):
    """Return an opaque raw-HTML leaf element.

    The string is emitted verbatim (not HTML-escaped) by the HTML writer.
    Only use for trusted, internally-generated HTML.
    """
    return {"_raw_html": html_str}


###########################################################


def _do_space_asserts(tag, fs_contents):
    if not fs_contents:
        return
    if tag == "style":
        return
    assert not _has_lt_space(fs_contents), (fs_contents[0], fs_contents[-1])
    for htel in fs_contents:
        if isinstance(htel, str):
            assert "  " not in htel, _double_space_helper(htel)


def _double_space_helper(string: str):
    match = re.search(r"\S*  \S*", string)
    return match and (match.group(0), string)


def _has_lt_space(xs):
    """Does this have either leading or trailing space?"""
    if xs[0] == sd.OCTO_NBSP:
        return False  # make an exception for OCTO_NBSP
    return _iswlts(xs[0], str.lstrip) or _iswlts(xs[-1], str.rstrip)


def _iswlts(x, strip_fn):
    """Is [this a] string with leading [or] trailing space?"""
    return isinstance(x, str) and strip_fn(x) != x


def _is_str_or_htel(obj):
    return isinstance(obj, str) or is_htel(obj) or is_raw_html(obj)


def _write_callback(add_wbr, html_comment, html_el, out_fp):
    out_fp.write("<!doctype html>\n")
    if html_comment:
        out_fp.write(f"<!-- {html_comment} -->\n")
    hgl_opts = {
        "hgl-add-wbr": add_wbr,
        "hgl-max-line-len": 100,
        "hgl-line-breaks-allowed": True,
    }
    lines = mb_html_get_lines.get_lines_from_html_el(hgl_opts, html_el)
    out_fp.write("\n".join(lines))


def _is_text_singleton(array):  # "array": tuple or list
    return len(array) == 1 and isinstance(array[0], str)


def _list_item(contents, attr=None):
    return htel_mk("li", attr, contents)


def _link_to_css(css_href):
    link_to_css_attr = {"rel": "stylesheet", "href": css_href}
    return htel_mk("link", attr=link_to_css_attr)


def _html_el1(attr, contents):
    return htel_mk("html", attr, contents)
