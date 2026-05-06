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

* `py-examples/main_mam4sef.py` uses the XML to create the
       Sefaria-format (CSV/HTML) version of MAM.
* `py-examples/main_mam_osis.py` uses the XML to create the OSIS XML
       output in the sibling `MAM-OSIS` repo. It validates the output against
       the OSIS XSD and therefore requires `lxml`.

To catalog all `<letter-small>` occurrences into a file you can use this
function (identical to `write_letter_small_report_from_xml_dir` in
`py-examples/mb_sefaria/mam4sef_letter_small_report.py`):

```python
import pathlib
import xml.etree.ElementTree as ET


def write_letter_small_report_from_xml_dir(xml_dir, out_path):
    lines = []
    for xml_path in sorted(pathlib.Path(xml_dir).glob("*.xml")):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for book39 in root:
            if book39.tag != "book39":
                continue
            for chapter in book39:
                if chapter.tag != "chapter":
                    continue
                for verse in chapter:
                    if verse.tag != "verse":
                        continue
                    book, ch, vr = verse.attrib["osisID"].split(".")
                    for el in verse.iter("letter-small"):
                        lines.append(
                            f"{book} {ch}:{vr}\t<small>{el.attrib['text']}</small>"
                        )
    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines))
        if lines:
            fp.write("\n")
    print(f"Wrote {len(lines)} lines to {out_path}")


write_letter_small_report_from_xml_dir("out/xml-vtrad-mam", "out/letter-small.txt")
```

The source of this data is
[MAM-parsed](https://github.com/bdenckla/MAM-parsed)/plus.

Other versions/formats of MAM (each with their tradeoffs) include:

* [MAM-parsed](https://github.com/bdenckla/MAM-parsed)
* [MAM for Sefaria](https://github.com/bdenckla/MAM-for-Sefaria)

One obscure-but-cool feature of the MAM-simple data
is that the BHS and Sefaria versions describe
the way in which their versifications differ from MAM's native versification.
Here are three abbreviated examples, using the XML format:
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
As you can see above, the versification-related attributes are
`contents-corresponds-to` and `osisID-of-MAM-src`.
The `contents-corresponds-to` attribute can take on one of three values:

* `a full verse in MAM`
* `less than a full verse in MAM`
* `no verse in MAM`

The `osisID-of-MAM-src` attribute complements the first two cases
above. It says _which_ verse in MAM this verse fully or partially
corresponds to.

For a complete, human-readable description of every place where the three
versifications differ, see
[doc/versification-differences.md](doc/versification-differences.md).


Questions? Email maintainer@miqra.simplelogin.com.
