# MAM-simple
This repo houses a version of MAM that is simple but not complete.
(See [MAM-parsed](https://github.com/bdenckla/MAM-parsed) for complete versions).
This repo's simple version of MAM is available in both XML and JSON formats.
Each of these two formats is, in turn, available in three versifications.
This yields a total of six flavors of MAM-simple:

<!-- sync: folder table also appears in doc/reading-mam-simple.md ##File-Layout -->
folder | format | versification
---- | ---- | ----
`xml-vtrad-bhs` | XML | BHS
`xml-vtrad-sef` | XML | Sefaria
`xml-vtrad-mam` | XML | MAM native
`json-vtrad-bhs` | JSON | BHS
`json-vtrad-sef` | JSON | Sefaria
`json-vtrad-mam` | JSON | MAM native

The JSON format mirrors the XML structure: it has the same hierarchy and element types.

For a detailed guide to the hierarchy and element types of both formats,
see [Reading MAM-simple](doc/reading-mam-simple.md).

This repo also has example programs. They are found under `py-examples/`:

<!-- sync: bullet list of example programs also appears in doc/reading-mam-simple.md ##The-py-examples-Programs -->
* The [`main_mam4sef.py`](py-examples/main_mam4sef.py) program
creates the Sefaria edition of MAM, using the JSON format as its input.
* The [`main_mam_osis.py`](py-examples/main_mam_osis.py) program
creates the OSIS edition of MAM, using the XML format as its input.
* The [`main_letter_small_job.py`](py-examples/main_letter_small_job.py) program
reports all of the `<letter-small>` elements in `Job.xml`,
writing output to `py-examples-out/letter-small-job.txt`.

As I said above, MAM-simple is not complete.
It is an extract of MAM, not a full version of MAM.
For versions of MAM that are complete (but therefore far from simple),
see [MAM-parsed](https://github.com/bdenckla/MAM-parsed).

Questions? Email maintainer@miqra.simplelogin.com.
