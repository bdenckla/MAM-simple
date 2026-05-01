# Reading MAM-simple

This document describes the XML and JSON formats used in MAM-simple and how to extract text from them.

## File Layout

```
out/
  xml-vtrad-bhs/    # XML, BHS versification
  xml-vtrad-sef/    # XML, Sefaria versification
  xml-vtrad-mam/    # XML, MAM native versification
  json-vtrad-bhs/   # JSON, BHS versification
  json-vtrad-sef/   # JSON, Sefaria versification
  json-vtrad-mam/   # JSON, MAM native versification
```

Each folder contains one file per book group (e.g., `Job.xml` / `Job.json`, `Gen.xml` / `Gen.json`, `1Sam-2Sam.xml` / `1Sam-2Sam.json`).
Within each format, the three versification folders differ only in versification — the text content is the same.
For a full description of where and how the three versifications differ, see [Versification Differences](versification-differences.md).

The JSON format mirrors the XML structure: the same hierarchy (book group → book → chapter → verse → child elements) and the same element types appear in both, with XML elements and attributes mapped to JSON objects and fields. See [JSON Structure](#json-structure) below.

## XML Element Hierarchy

```
<book24 versification-tradition="...">       ← root element
  <book39 osisID="Job">                      ← one per biblical book in the group
    <chapter osisID="Job.1">                 ← one per chapter
      <verse osisID="Job.1.1" .../>          ← one per verse
      <verse osisID="Job.1.2" .../>
      ...
    </chapter>
    <spi-pe2/>                               ← parashah marker between chapters
    <chapter osisID="Job.2">
      ...
    </chapter>
  </book39>
</book24>
```

Parashah elements (`spi-pe2`, `spi-pe3`, `spi-samekh2`, `spi-samekh3`)
can appear between chapters (as children of `book39`),
between books (as children of `book24` — e.g., between 1 Samuel and 2 Samuel),
and within verses (as children of `verse`).

## How Verse Text Is Stored

### Simple verses: `text` attribute

Most verses store their full text in a `text` attribute on the `<verse>` element:

```xml
<verse osisID="Job.34.2" yeivinID="Job 34:2"
       text="שִׁמְע֣וּ חֲכָמִ֣ים מִלָּ֑י וְ֝יֹדְעִ֗ים הַאֲזִ֥ינוּ לִֽי׃"/>
```

### Complex verses: child elements

Verses with special features (legarmeih, paseq, ketiv/qere, etc.)
have **no** `text` attribute.
Instead, the text is distributed across `<text>` child elements,
interspersed with markup elements:

```xml
<verse osisID="Job.1.1" yeivinID="Job 1:1">
  <text text="אִ֛ישׁ הָיָ֥ה בְאֶֽרֶץ־ע֖וּץ אִיּ֣וֹב שְׁמ֑וֹ וְהָיָ֣ה"/>
  <lp-legarmeih/>
  <text text=" הָאִ֣ישׁ הַה֗וּא תָּ֧ם וְיָשָׁ֛ר וִירֵ֥א אֱלֹהִ֖ים וְסָ֥ר מֵרָֽע׃"/>
</verse>
```

### Rule for extracting plain text

1. If the verse has a `text` attribute → use it directly.
2. Otherwise → concatenate the `text` attributes of all `<text>` child elements, in order.

## Child Element Types

| Element | Meaning |
|---------|---------|
| `<text text="..."/>` | A run of Hebrew text |
| `<lp-legarmeih/>` | Legarmeih |
| `<lp-paseq/>` | Paseq |
| `<implicit-maqaf/>` | Maqaf that is implicit in the manuscript |
| `<letter-small>` | Small letter |
| `<letter-large>` | Large letter |
| `<letter-hung>` | Hung (aka suspended) letter |
| `<kq>` | Ketiv/Qere pair |
| `<kq-k>` | Ketiv portion |
| `<kq-q>` | Qere portion |
| `<kq-trivial>` | Trivial Ketiv/Qere |
| `<kq-k-velo-q>` | Ketiv with no Qere |
| `<kq-q-velo-k>` | Qere with no Ketiv |
| `<cant-all-three>` | Wraps combined, alef, and bet |
| `<cant-combined>` | Combined cantillation (1 of 3)|
| `<cant-alef>` | Alef cantillation (2 of 3) |
| `<cant-bet>` | Bet cantillation (3 of 3) |
| `<shirah-space/>` | Shirah (song) spacing |
| `<good-ending>` | Alternative ending |
| `<scrdfftar>` | Targeted scroll-difference note |
| `<sdt-target>` | The `<scrdfftar>` target |
| `<sdt-note>` | The `<scrdfftar>` note itself |
| `<spi-samekh2>`, `<spi-samekh3>` | Parashah setumah markers |
| `<spi-pe2>`, `<spi-pe3>` | Parashah petuḥah markers |
| `<spi-invnun>` | Inverted nun |

## Verse Attributes

| Attribute | Meaning |
|-----------|---------|
| `osisID` | OSIS-format reference (e.g., `Job.34.24`) |
| `yeivinID` | Yeivin-format reference (e.g., `Job 34:24`) |
| `text` | Full verse text (only present for simple verses) |
| `starts-with-sampe` | Verse starts after a parashah marker (`pe2`, `samekh2`, etc.) |
| `ends-with-sampe` | Verse ends with a parashah marker |
| `contents-corresponds-to` | Versification note (see [Versification Differences](versification-differences.md)) |
| `osisID-of-MAM-src` | Source verse in MAM versification (see [Versification Differences](versification-differences.md)) |

## Example: Extracting Plain Text in Python

```python
import xml.etree.ElementTree as ET

def get_verse_text(verse_el):
    """Extract plain text from a <verse> element."""
    if 'text' in verse_el.attrib:
        return verse_el.attrib['text']
    return ''.join(
        c.attrib['text'] for c in verse_el if c.tag == 'text'
    )

tree = ET.parse('out/xml-vtrad-mam/Job.xml')
book39 = tree.getroot()[0]  # <book39 osisID="Job">

for child in book39:
    if child.tag != 'chapter':
        continue
    for verse in child:
        if verse.tag != 'verse':
            continue
        text = get_verse_text(verse)
        print(f"{verse.attrib['osisID']}: {text}")
```

**Note:** The above `get_verse_text` is a simplification suitable for
extracting the basic consonantal text with vowels and accents.
For handling ketiv/qere, special letters, legarmeih rendering, etc.,
see the handler-based approach in `py-examples/mb_sefaria/mam4sef_handlers.py`.

## The `py-examples/` Programs

The `py-examples/` directory contains two complete working examples:

- **`main_mam4sef.py`** — reads MAM-simple JSON and produces the
  MAM-for-Sefaria CSV/HTML output.
- **`main_mam_osis.py`** — reads MAM-simple XML and produces the
  MAM-OSIS XML output.

Both examples use a recursive handler pattern where each element type
has a registered handler function:

- **`mam4sef_or_ajf.py`** — reads JSON, walks the tree with `_handle()`
- **`mam4sef_handlers.py`** — handler functions for every element type, keyed by `(tag, class)` tuple

The OSIS example additionally uses the `osis/` helper modules.
Together these examples are the canonical reference for how to process
the full range of MAM-simple element types.

## JSON Structure

The JSON format mirrors the XML structure.
The root object has two fields:

| Field | Value |
|-------|-------|
| `versification-tradition` | `"vtbhs"`, `"vtsef"`, or `"vtmam"` |
| `contents` | Array of `book39` objects and parashah-marker objects |

### Book39 object

```json
{
  "type": "book39",
  "osisID": "Ruth",
  "contents": [ ... ]
}
```

`contents` is an array of chapter objects and parashah-marker objects (same types as in XML).

### Chapter object

```json
{
  "type": "chapter",
  "osisID": "Ruth.1",
  "contents": [ ... ]
}
```

`contents` is an array of verse objects and parashah-marker objects.

### Verse objects

Simple verses (no special markup) have a `text` field directly:

```json
{
  "type": "verse",
  "osisID": "Ruth.1.1",
  "yeivinID": "Rut 1:1",
  "text": "וַיְהִ֗י בִּימֵי֙ ..."
}
```

Complex verses (with legarmeih, ketiv/qere, etc.) have a `contents` array instead:

```json
{
  "type": "verse",
  "osisID": "Ruth.1.2",
  "yeivinID": "Rut 1:2",
  "contents": [
    { "type": "text", "text": "וְשֵׁ֣ם הָאִ֣ישׁ ..." },
    { "type": "lp-legarmeih" },
    { "type": "text", "text": " מַחְל֤וֹן ..." }
  ]
}
```

### Rule for extracting plain text (JSON)

1. If the verse object has a `text` field → use it directly.
2. Otherwise → concatenate the `text` fields of all objects in `contents` where `type == "text"`, in order.

Verse objects can be identified by `"type": "verse"`. The full set of child element types is the same as in XML (see [Child Element Types](#child-element-types) above).
Parashah-marker objects (e.g., `{ "type": "spi-pe2" }`) can appear as children of the root object's `contents` array (between `book39` objects — e.g., between 1 Samuel and 2 Samuel), or as children of `book39`, `chapter`, or `verse` `contents` arrays.
