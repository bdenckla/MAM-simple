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

## The `py-examples/` Programs

The `py-examples/` directory contains three complete working examples:

<!-- sync: bullet list of example programs also appears in README.md -->
- **[`main_mam4sef.py`](../py-examples/main_mam4sef.py)** — creates the Sefaria edition of MAM, using the JSON format as its input.
- **[`main_mam_osis.py`](../py-examples/main_mam_osis.py)** — creates the OSIS edition of MAM, using the XML format as its input.
- **[`main_letter_small_job.py`](../py-examples/main_letter_small_job.py)** — reports all of the `<letter-small>` elements in `Job.xml`, writing output to `py-examples-out/letter-small-job.txt`.

The example programs [`main_mam4sef.py`](../py-examples/main_mam4sef.py) and [`main_mam_osis.py`](../py-examples/main_mam_osis.py) both use a recursive handler
pattern where each element type has a registered handler function. For
[`main_mam4sef.py`](../py-examples/main_mam4sef.py) the relevant modules are:

- **[`mam4sef_or_ajf.py`](../py-examples/mb_sefaria/mam4sef_or_ajf.py)** — reads JSON, walks the tree with `_handle()`
- **[`mam4sef_handlers.py`](../py-examples/mb_sefaria/mam4sef_handlers.py)** — handler functions for every element type, keyed by `(tag, class)` tuple

The program [`main_mam_osis.py`](../py-examples/main_mam_osis.py) uses the same pattern over XML elements, with handler
functions in [`osis/osis_handlers.py`](../py-examples/osis/osis_handlers.py).

Together, [`main_mam4sef.py`](../py-examples/main_mam4sef.py) and [`main_mam_osis.py`](../py-examples/main_mam_osis.py) are the canonical
reference for how to process the full range of MAM-simple element types.

The program [`main_letter_small_job.py`](../py-examples/main_letter_small_job.py) is a simpler example that iterates directly
over XML elements without the handler pattern.
