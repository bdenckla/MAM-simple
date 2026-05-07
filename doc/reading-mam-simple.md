# Reading MAM-simple

This document describes the XML and JSON formats used in MAM-simple and how to extract text from them.

## File Layout

folder | format | versification
---- | ---- | ----
`out/xml-vtrad-bhs` | XML | BHS
`out/xml-vtrad-sef` | XML | Sefaria
`out/xml-vtrad-mam` | XML | MAM native
`out/json-vtrad-bhs` | JSON | BHS
`out/json-vtrad-sef` | JSON | Sefaria
`out/json-vtrad-mam` | JSON | MAM native

Each folder contains one file per `book24` (e.g., `1Sam-2Sam.xml`, `Gen.xml`, `Hos-Mal.xml`).
A `book24` corresponds to one of the 24 books of the Hebrew Bible; some of them span more than one `book39`, i.e. some of them span more than one book in the system that divides the Hebrew Bible up into 39 rather than 24 books.

For a full description of where and how the three versifications differ, see [Versification Differences](versification-differences.md).

The JSON format mirrors the XML structure: the same hierarchy (`book24` → `book39` → chapter → verse → child elements) and the same element types appear in both, with XML elements and attributes mapped to JSON objects and fields. See [JSON Structure](#json-structure) below.

## XML Element Hierarchy

```xml
<book24 versification-tradition="..."> <!-- root element -->
  <book39 osisID="Job">
    <chapter osisID="Job.1">
      <verse osisID="Job.1.1" .../>
      <verse osisID="Job.1.2" .../>
      ...
    </chapter>
    <spi-pe2/>
    <!-- parashah marker between chapters; can also appear between books and within verses -->
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
| `contents-corresponds-to` | Versification note |
| `osisID-of-MAM-src` | Source verse in MAM's native versification |

### Versification Attributes

The BHS and Sefaria versions describe the way in which their versifications
differ from MAM's native versification via two `<verse>` attributes:
`contents-corresponds-to` and `osisID-of-MAM-src`.
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
The `contents-corresponds-to` attribute can take on one of three values:

* `a full verse in MAM`
* `less than a full verse in MAM`
* `no verse in MAM`

The `osisID-of-MAM-src` attribute complements the first two cases
above. It says _which_ verse in MAM this verse fully or partially
corresponds to.

For a description of every place where the three
versifications differ, see
[versification-differences.md](versification-differences.md).

## JSON Structure

The JSON format mirrors the XML structure.
The full set of child element types is the same as in XML (see [Child Element Types](#child-element-types) above).

### Root object

```json
{
  "versification-tradition": "vtmam",
  "contents": [ ... ]
}
```

The `versification-tradition` field is one of `"vtbhs"`, `"vtsef"`, or `"vtmam"`.
The `contents` array contains `book39` objects and parashah-marker objects.

### Book39 objects

```json
{
  "type": "book39",
  "osisID": "Ruth",
  "contents": [ ... ]
}
```

The `contents` array contains chapter objects and parashah-marker objects (same types as in XML).

### Chapter objects

```json
{
  "type": "chapter",
  "osisID": "Ruth.1",
  "contents": [ ... ]
}
```

The `contents` array contains verse objects and parashah-marker objects.

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

### Parashah-marker objects

```json
{ "type": "spi-pe2" }
```

Parashah-marker objects can appear as children of the root object's `contents` array (between `book39` objects — e.g., between 1 Samuel and 2 Samuel), or as children of `book39`, `chapter`, or `verse` `contents` arrays.

## The `py-examples/` Programs

The `py-examples/` directory contains three complete working examples:

- **[`main_mam4sef.py`](../py-examples/main_mam4sef.py)** — reads MAM-simple JSON and produces the
  MAM-for-Sefaria CSV/HTML output.
- **[`main_mam_osis.py`](../py-examples/main_mam_osis.py)** — reads MAM-simple XML and produces the
  MAM-OSIS XML output.
- **[`main_letter_small_job.py`](../py-examples/main_letter_small_job.py)** — reads MAM-simple XML and writes a
  report of all `<letter-small>` occurrences in Job.

The example programs [`main_mam4sef.py`](../py-examples/main_mam4sef.py) and [`main_mam_osis.py`](../py-examples/main_mam_osis.py) both use a recursive handler
pattern where each element type has a registered handler function. For
[`main_mam4sef.py`](../py-examples/main_mam4sef.py) the relevant modules are:

- **`mam4sef_or_ajf.py`** — reads JSON, walks the tree with `_handle()`
- **`mam4sef_handlers.py`** — handler functions for every element type, keyed by `(tag, class)` tuple

The program [`main_mam_osis.py`](../py-examples/main_mam_osis.py) uses the same pattern over XML elements, with handler
functions in the `osis/` helper modules.

Together, [`main_mam4sef.py`](../py-examples/main_mam4sef.py) and [`main_mam_osis.py`](../py-examples/main_mam_osis.py) are the canonical
reference for how to process the full range of MAM-simple element types.

The program [`main_letter_small_job.py`](../py-examples/main_letter_small_job.py) is a simpler example that iterates directly
over XML elements without the handler pattern.
