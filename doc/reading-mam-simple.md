# Reading MAM-simple

This document describes the XML and JSON formats used in MAM-simple and how to extract text from them.

## File Layout

<!-- sync: folder table also appears in README.md -->
folder | format | versification
---- | ---- | ----
`xml-vtrad-bhs` | XML | BHS
`xml-vtrad-sef` | XML | Sefaria
`xml-vtrad-mam` | XML | MAM native
`json-vtrad-bhs` | JSON | BHS
`json-vtrad-sef` | JSON | Sefaria
`json-vtrad-mam` | JSON | MAM native

Each folder contains one file per `book24` (e.g., `1Sam-2Sam.xml`, `Gen.xml`, `Hos-Mal.xml`).
A `book24` corresponds to one of the 24 books of the Hebrew Bible; some of them span more than one `book39`, i.e. some of them span more than one book in the system that divides the Hebrew Bible up into 39 rather than 24 books.

For a full description of where and how the three versifications differ, see [Versification Differences](versification-differences.md).

## Format Details

- **[XML format](reading-mam-simple-xml.md)** — element hierarchy, verse text storage, child element types, verse attributes, and versification attributes.
- **[JSON format](reading-mam-simple-json.md)** — JSON object structure mirroring the XML hierarchy.

## Reading MAM-simple from Python

Nothing beyond the standard library is needed. This program writes the plain text of
Job 34 to a file, and it handles every element type MAM-simple has:

```python
import xml.etree.ElementTree as ET

# Elements whose children are alternatives rather than a stretch of running text.
_CHOOSE = {"kq": "kq-q", "cant-all-three": "cant-combined", "scrdfftar": "sdt-target"}
_SKIP = ("good-ending",)  # a repetition after the last verse, not running text


def element_text(el):
    """The plain text of one element, assembled recursively."""
    if "text" in el.attrib:  # a text attribute and children never co-occur
        return el.attrib["text"]
    chosen = _CHOOSE.get(el.tag)
    if chosen is not None:
        return element_text(el.find(chosen))
    return "".join(element_text(k) for k in el if k.tag not in _SKIP)


def verses_of(xml_path):
    """Yield (osisID, plain text) for each verse of one MAM-simple XML file."""
    for book39 in ET.parse(xml_path).getroot():
        if book39.tag != "book39":
            continue  # a parashah marker between books
        for chapter in book39:
            if chapter.tag != "chapter":
                continue  # a parashah marker between chapters
            for verse in chapter:
                if verse.tag != "verse":
                    continue  # a parashah marker between verses
                yield verse.attrib["osisID"], element_text(verse)


def main():
    with open("py-examples-out/job-34.txt", "w", encoding="utf-8") as out:
        for osis_id, text in verses_of("xml-vtrad-mam/Job.xml"):
            if osis_id.startswith("Job.34."):
                out.write(f"{osis_id}: {text}\n")
```

Three points in it are easy to get wrong:

- **The recursion is not optional.** Plain text sits below `<kq>`, `<slh-word>` and
  others, so a walk that reads only the `<text>` children of a verse drops every
  ketiv/qere and every suspended-letter word, and drops them silently.
- **`_CHOOSE` picks among alternatives.** Concatenating the children of `<kq>` would
  give you the ketiv and the qere run together. Which child to choose is the caller's
  decision; `kq-q` above is one reasonable answer, not the only one.
- **Write non-ASCII to a file, not to stdout.** On Windows, Python encodes a redirected
  stdout with the locale code page, and printing Hebrew there raises
  `UnicodeEncodeError`. If you do want it on stdout, call
  `sys.stdout.reconfigure(encoding="utf-8")` first.

For the element and attribute names the program relies on, see
[the XML format](reading-mam-simple-xml.md).

## The `py-examples/` Programs

The `py-examples/` directory contains three complete working examples:

<!-- sync: bullet list of example programs also appears in README.md -->
- **[`main_mam4sef_example.py`](../py-examples/main_mam4sef_example.py)** — creates the Sefaria edition of MAM, using the JSON format as its input.
- **[`main_mam_osis_example.py`](../py-examples/main_mam_osis_example.py)** — creates the OSIS edition of MAM, using the XML format as its input.
- **[`main_letter_small_job_example.py`](../py-examples/main_letter_small_job_example.py)** — reports all of the `<letter-small>` elements in `Job.xml`, writing output to `py-examples-out/letter-small-job.txt`.

The example programs [`main_mam4sef_example.py`](../py-examples/main_mam4sef_example.py) and [`main_mam_osis_example.py`](../py-examples/main_mam_osis_example.py) both use a recursive handler
pattern where each element type has a registered handler function. For
[`main_mam4sef_example.py`](../py-examples/main_mam4sef_example.py) the relevant modules are:

- **[`mam4sef_or_ajf.py`](../py-examples/mb_sefaria/mam4sef_or_ajf.py)** — reads JSON, walks the tree with `_handle()`
- **[`mam4sef_handlers.py`](../py-examples/mb_sefaria/mam4sef_handlers.py)** — handler functions for every element type, keyed by `(tag, class)` tuple

The program [`main_mam_osis_example.py`](../py-examples/main_mam_osis_example.py) uses the same pattern over XML elements, with handler
functions in [`osis/osis_handlers.py`](../py-examples/osis/osis_handlers.py) and the walk itself in
[`osis/osis_runner.py`](../py-examples/osis/osis_runner.py). Its `_handle()` is where to look to see the pattern
whole. It processes one element by first processing that element's children, and then
calling the element's handler with three arguments:

- `etel` — the element itself
- `ofc1` — output for all children, summed together
- `ofc2` — output for all children, per child

When the element has a `text` attribute, `ofc1` is that attribute instead, which works
because a `text` attribute and children never co-occur. Handlers are keyed by
`(tag, class)`, so `("kq", "sep-maqaf")` gets a different handler from `("kq", None)`.
The `ofc2` argument is what lets a handler choose among its children rather than take
them all: `<scrdfftar>`'s handler uses it to tell the target from the note.

Together, [`main_mam4sef_example.py`](../py-examples/main_mam4sef_example.py) and [`main_mam_osis_example.py`](../py-examples/main_mam_osis_example.py) are the canonical
reference for how to process the full range of MAM-simple element types.

The program [`main_letter_small_job_example.py`](../py-examples/main_letter_small_job_example.py) is a simpler example that iterates directly
over XML elements without the handler pattern.
