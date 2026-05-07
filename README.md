# MAM-simple
This repo has extracts of MAM in XML and JSON formats that are simple but not complete.
Each of these two formats is, in turn, available in three versifications.
This yields a total of six extracts of MAM:

<!-- sync: folder table also appears in doc/reading-mam-simple.md ##File-Layout -->
folder | format | versification
---- | ---- | ----
`out/xml-vtrad-bhs` | XML | BHS
`out/xml-vtrad-sef` | XML | Sefaria
`out/xml-vtrad-mam` | XML | MAM native
`out/json-vtrad-bhs` | JSON | BHS
`out/json-vtrad-sef` | JSON | Sefaria
`out/json-vtrad-mam` | JSON | MAM native

The JSON format mirrors the XML structure: it has the same hierarchy and element types.

For a detailed guide to the hierarchy and element types of both formats,
see [Reading MAM-simple](doc/reading-mam-simple.md).

This repo also has example programs under `py-examples/`:

<!-- sync: bullet list of example programs also appears in doc/reading-mam-simple.md ##The-py-examples-Programs -->
* [`py-examples/main_mam4sef.py`](py-examples/main_mam4sef.py)
creates the Sefaria edition of MAM, using the JSON format as its input.
* [`py-examples/main_mam_osis.py`](py-examples/main_mam_osis.py)
creates the OSIS edition of MAM, using the XML format as its input.
* [`py-examples/main_letter_small_job.py`](py-examples/main_letter_small_job.py)
reports all of the `<letter-small>` elements in `Job.xml`.

As I said above, MAM-simple is not complete.
It is an extract of MAM, not a full version of the MAM dataset.
For a version of the MAM dataset that is complete (but therefore far from simple),
see [MAM-parsed](https://github.com/bdenckla/MAM-parsed)/plus.

Questions? Email maintainer@miqra.simplelogin.com.
