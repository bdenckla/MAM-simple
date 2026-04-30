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

This repo also has a program, `py-example/main_mam4sef.py`,
that is an example of how the XML can be used.
This program uses the XML to create the Sefaria-format (CSV/HTML) version of MAM.

The source of this data is
[MAM-parsed](https://github.com/bdenckla/MAM-parsed)/plus.

Other versions/formats of MAM (each with their tradeoffs) include:

* [MAM-parsed](https://github.com/bdenckla/MAM-parsed)
* [MAM for Sefaria](https://github.com/bdenckla/MAM-for-Sefaria)

One obscure-but-cool feature of this XML format
is that the `<verse>` element has attributes
that describe the way in which the versification (BHS or Sefaria)
differs from MAM's native versification.
Here are three abbreviated examples:
```xml
<verse osisID="1Sam.24.1"
       contents-corresponds-to="a full verse in MAM"
       osisID-of-MAM-src="1Sam.23.29"/>
<verse osisID="Deut.5.7"
       contents-corresponds-to="less than a full verse in MAM"
       osisID-of-MAM-src="Deut.5.6">
<verse osisID="Josh.21.36"
       contents-corresponds-to="no verse in MAM"/>
```
As you can see above, these versification-related attributes are
`contents-corresponds-to` and `osisID-of-MAM-src`.
The `contents-corresponds-to` attribute can take on one of three values:

* `a full verse in MAM`
* `less than a full verse in MAM`
* `no verse in MAM`

The `osisID-of-MAM-src` attribute complements the first two cases
above. It says _which_ verse in MAM this verse fully or partially
corresponds to.


Questions? Email maintainer@miqra.simplelogin.com.
