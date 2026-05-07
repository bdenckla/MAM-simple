# MAM-simple
This repo has an extract of MAM in XML and JSON formats that are simple but not complete. See:
* `out/xml-vtrad-bhs` for XML files that use BHS versification
* `out/xml-vtrad-sef` for XML files that use Sefaria versification
* `out/xml-vtrad-mam` for XML files that use MAM native versification
* `out/json-vtrad-bhs` for JSON files that use BHS versification
* `out/json-vtrad-sef` for JSON files that use Sefaria versification
* `out/json-vtrad-mam` for JSON files that use MAM native versification

The JSON format mirrors the XML structure (same hierarchy and element types,
expressed as nested JSON objects instead of XML elements).

For a detailed guide to the structure, element types, and how to extract text,
see [Reading MAM-simple](doc/reading-mam-simple.md).

This repo also has example programs under `py-examples/`:

* [`py-examples/main_mam4sef.py`](py-examples/main_mam4sef.py) uses the JSON to create the
       Sefaria-format (CSV/HTML) version of MAM.
* [`py-examples/main_mam_osis.py`](py-examples/main_mam_osis.py) uses the XML to create the OSIS XML
       output in the sibling `MAM-OSIS` repo. It validates the output against
       the OSIS XSD and therefore requires `lxml`.
* [`py-examples/main_letter_small_job.py`](py-examples/main_letter_small_job.py) uses the XML to find all
       `<letter-small>` elements in Job and write a report.

The source of this data is
[MAM-parsed](https://github.com/bdenckla/MAM-parsed)/plus.

Other versions/formats of MAM (each with their tradeoffs) include:

* [MAM-parsed](https://github.com/bdenckla/MAM-parsed)
* [MAM for Sefaria](https://github.com/bdenckla/MAM-for-Sefaria)

Questions? Email maintainer@miqra.simplelogin.com.
