"""Serialize an "htel" element tree into lines of HTML source text.

PURE ALGORITHM: every policy decision is the CALLER's, passed in ``hgl_opts`` -- which
tags get a newline after their open tag or after their close tag, which are void, and
which hold content to emit verbatim.  Those tables used to be module globals here, and
that is exactly what forced each repo wanting this serializer to keep a copy-and-edited
version of the whole file.  With the policy hoisted into the options, repos whose
generated HTML breaks lines differently share one algorithm: MAM-basics' tables live
next door in ``mb_html.py``, wlc-utils' in its own ``py_html/wlc_utils_html.py``, and
neither repo's break structure constrains the other's.

``hgl_opts`` keys, all required:

``hgl-max-line-len``
    Greedy wrap width.  ``-1`` disables wrapping, so each paragraph stays one line.
``hgl-add-wbr``
    Insert a ``<wbr>`` after each maqaf, offering the browser a break opportunity.
``hgl-line-breaks-allowed``
    When False, ``hgl-lb1``/``hgl-lb2`` go unconsulted and no paragraph is ever
    started, so wrapping is the only thing that can split the output.
``hgl-lb1``, ``hgl-lb2``
    Tag -> ``"\\n"`` or ``""``: whether a newline follows the open tag (``lb1``) and
    whether one follows the close tag (``lb2``).  Indexed strictly, so a tag missing
    from either table raises ``KeyError`` rather than silently picking a default.
``hgl-noclose``
    Set of void tags, emitted with no close tag.
``hgl-verbatim-tags``
    Set of tags whose string contents are emitted raw -- neither HTML-escaped nor split
    into wrappable words.  ``style`` and ``script`` need this because entities are not
    decoded inside them; ``pre`` needs it because its whitespace is significant.

A newline inside a text string is the author's own hard break and is preserved as one --
see ``_add_str``.  Wrapping therefore only ever REPLACES AN EXISTING SPACE with a newline;
it never invents a break point, moves text, or alters an entity.  That is what lets a
caller prove a rewrap changed nothing by collapsing whitespace runs and comparing.
"""

import html
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import str_defs as sd
from mb_cmn.my_utils import sum_of_map


def get_lines_from_html_el(hgl_opts, html_el):
    io_paragraphs = [[""]]
    max_line_len = hgl_opts["hgl-max-line-len"]
    _el_to_paragraphs(hgl_opts, io_paragraphs, html_el)
    return sum_of_map((_get_lines_from_words, max_line_len), io_paragraphs)


def _el_to_paragraphs(hgl_opts, io_paragraphs, html_el):
    """Convert an HTML element to a string."""
    add_wbr = hgl_opts["hgl-add-wbr"]
    if isinstance(html_el, str):
        _add_str(io_paragraphs, _finalize_string(add_wbr, html_el))
        return
    if isinstance(html_el, dict) and "_raw_html" in html_el:
        _add_word(io_paragraphs[-1], html_el["_raw_html"])
        return
    eltag = html_el["_htel_tag"]
    attr_str = _attr_str(html_el.get("attr"))
    _add_word(io_paragraphs[-1], f"<{eltag}{attr_str}>")
    lb_allowed = hgl_opts["hgl-line-breaks-allowed"]
    if lb_allowed:
        _maybe_start_new_paragraph(io_paragraphs, hgl_opts["hgl-lb1"][eltag])
    if contents := html_el.get("contents"):
        assert isinstance(contents, (tuple, list))
        if eltag in hgl_opts["hgl-verbatim-tags"]:
            for seq_el in contents:
                _add_word(io_paragraphs[-1], seq_el)
        else:
            for seq_el in contents:
                _el_to_paragraphs(hgl_opts, io_paragraphs, seq_el)
    if eltag not in hgl_opts["hgl-noclose"]:
        _add_word(io_paragraphs[-1], f"</{eltag}>")
    if lb_allowed:
        _maybe_start_new_paragraph(io_paragraphs, hgl_opts["hgl-lb2"][eltag])


def _finalize_string(add_wbr, string):
    outstr = string
    outstr = html.escape(outstr, quote=False)
    outstr = outstr.translate(_SSTT)
    if add_wbr:
        outstr = outstr.replace(hpu.MAQ, hpu.MAQ + "<wbr>")
    return outstr


def _add_str(io_paragraphs, string: str):
    """Add a text string, honoring any newline the AUTHOR put inside it.

    Such a newline is a hard break, ending the current paragraph exactly as an lb1/lb2
    newline does.  So it survives verbatim, and the text on either side of it wraps
    independently.  This used to be ``assert "\\n" not in string`` -- fine while every
    caller built its prose from newline-free pieces, but not a policy: wlc-utils' htel
    body modules were migrated byte-exactly from hand-authored HTML and carry both
    mid-sentence newlines and bare "\\n\\n" spacers, which the assert simply could not
    represent.  Splitting is what reproduces them.
    """
    segments = string.split("\n")
    _add_words(io_paragraphs[-1], segments[0])
    for segment in segments[1:]:
        io_paragraphs.append([""])
        _add_words(io_paragraphs[-1], segment)


def _add_words(io_paragraph, string: str):
    words = string.split(" ")
    _add_word(io_paragraph, words[0])
    io_paragraph.extend(words[1:])


def _add_word(io_paragraph, new_word: str):
    io_paragraph[-1] += new_word


def _maybe_start_new_paragraph(io_paragraphs, hts_lbn):
    if hts_lbn == "\n":
        io_paragraphs.append([""])
    else:
        assert hts_lbn == ""


def _get_lines_from_words(max_line_len, words):
    out_lines = [words[0]]
    for word in words[1:]:
        new_last_line = out_lines[-1] + " " + word
        if max_line_len == -1 or len(new_last_line) <= max_line_len:
            out_lines[-1] = new_last_line
        else:
            out_lines.append(word)
    return out_lines


def _attr_str(attr_dic):
    if not attr_dic:
        return ""
    return " " + " ".join(map(_kv_str, attr_dic.items()))


def _kv_str(key_and_val):
    key = key_and_val[0]
    value = html.escape(key_and_val[1], quote=True)
    return f'{key}="{value}"'


_SSTT = str.maketrans(
    {  # special space translation table
        "\N{EM SPACE}": "&emsp;",
        sd.THSP: "&thinsp;",
        sd.HAIRSP: "&hairsp;",
        sd.NBSP: "&nbsp;",
    }
)
