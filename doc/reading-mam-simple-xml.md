# Reading MAM-simple: XML Format

## XML Element Hierarchy

You can get a feel for the hierarchy from this schematic overview of how the book of Job is encoded:

```xml
<book24 versification-tradition="..."> <!-- root element -->
  <book39 osisID="Job">
    <chapter osisID="Job.1">
      <verse osisID="Job.1.1" .../>
      <verse osisID="Job.1.2" .../>
      ...
    </chapter>
    <spi-pe2/> <!-- parashah marker between chapters -->
    <chapter osisID="Job.2">
      ...
    </chapter>
  </book39>
</book24>
```

The root element is always `<book24>`, and its one attribute is
`versification-tradition`, whose value is `vtmam`, `vtbhs`, or `vtsef`
according to which of the six folders the file came from.

A parashah element (`spi-pe2`, `spi-pe3`, `spi-samekh2`, `spi-samekh3`)
can appear:

- as a child of `book24`, between `book39` elements (e.g., between 1 Samuel and 2 Samuel)
- as a child of `book39`, between chapters
- as a child of `chapter`, between verses
- as a child of `verse`, within a verse

This treatment of parashah breaks is a distinctive feature of MAM-simple. Most encodings of the Tanakh make every parashah break belong to a verse. This requires the vast majority of breaks to be assigned to either the preceding or following verse. (The few mid-verse breaks of course naturally belong to their verse.)

Each system (freely-placed breaks and verse-assigned breaks) has its merits. MAM-simple has freely-placed breaks, but also provides `starts-with-sampe` and `ends-with-sampe` verse attributes. These attributes support use-cases for which a starts-with or ends-with encoding is a better fit.

Thus, MAM-simple has three encodings of each parashah break: free, starts-with, and ends-with.
This makes MAM-simple less simple, but we believe the tradeoff is a good one.
Choosing a single encoding would simplify the data at a cost to use-cases that don't fit
that encoding well.

## Three invariants worth relying on

**All text is in a `text` attribute. There is no PCDATA.**
MAM-simple's XML has no text between tags.
Among other advantages, this makes its relationship to the JSON version much tighter.
It also means an XML reader never has to consult `element.text` or `element.tail`.

**An element has a `text` attribute or children, never both.**
So for any element, either its text is the `text` attribute directly, or its text
is assembled from its children — there is no case in which you must combine the two.

**The combining marks of a letter are in MAM's order, not Unicode's.**
Four marks come first, in this order: shin dot (U+05C1), sin dot (U+05C2),
dagesh or mapiq (U+05BC), and rafe (U+05BF).
Every other mark keeps the relative order it already had.
The consequence you will meet first is that a dagesh comes before its vowel,
where Unicode's canonical order puts the vowel first.

This text is therefore neither NFC nor NFD, so
**do not run `unicodedata.normalize`, or any other normalization, over it.**
Normalizing reorders the marks of tens of thousands of clusters, changes nothing on
screen, and raises no error: the two orders render identically, so the damage surfaces
only where something later compares bytes.
Genesis alone has 337 clusters with a shin or sin dot before a dagesh and 8,325 with
a dagesh before a vowel; across all 24 files of a flavour the counts are 4,836 and
122,797, and are the same in all six flavours.

MAM's mark order is a property of MAM itself, which MAM-simple preserves rather than
imposes: the generator checks every element it renders and aborts on a violation
instead of repairing one.
The implementation is `give_std_mark_order`, in MAM-basics'
[`py/mb_cmn/uni_denorm.py`](https://github.com/bdenckla/MAM-basics/blob/main/py/mb_cmn/uni_denorm.py).
The combining-class values `give_std_mark_order` sorts by follow the recommendation at
the end of the SBL Hebrew Font user manual.

Only those four marks have a declared place.
A vowel and an accent pass in either order, so MAM's mark order is not a full canonical
form: agreement on the four marks does not imply byte-identity after a round trip
through some other sort.

## How Verse Text Is Stored

### Simple verses: `text` attribute

A `<verse>` element without any special features stores its full, plain text in a `text` attribute, e.g.:

```xml
<verse osisID="Job.34.2" yeivinID="Job 34:2"
       text="שִׁמְע֣וּ חֲכָמִ֣ים מִלָּ֑י וְ֝יֹדְעִ֗ים הַאֲזִ֥ינוּ לִֽי׃"/>
```

Most verses are of this kind.

### Complex verses: child elements

A `<verse>` element with one or more special features
(legarmeh, paseq, ketiv/qere, etc.)
has **no** `text` attribute.
Instead, the plain text between special features is in `<text>` child elements,
interspersed with elements encoding special features, e.g.:

```xml
<verse osisID="Job.1.1" yeivinID="Job 1:1">
  <text text="אִ֛ישׁ הָיָ֥ה בְאֶֽרֶץ־ע֖וּץ אִיּ֣וֹב שְׁמ֑וֹ וְהָיָ֣ה"/>
  <lp-legarmeih/>
  <text text=" הָאִ֣ישׁ הַה֗וּא תָּ֧ם וְיָשָׁ֛ר וִירֵ֥א אֱלֹהִ֖ים וְסָ֥ר מֵרָֽע׃"/>
</verse>
```

## Extracting the plain text of a verse

1. If the `<verse>` has a `text` attribute, that attribute is the whole plain text.
2. Otherwise, walk its children in document order. Each child contributes either its
   `text` attribute or, if it has children instead, the text assembled from those.

**Step 2 has to recurse, and a reader that skips the recursion loses text silently.**
It is tempting to write step 2 as "concatenate the `text` attributes of the `<text>`
children," but plain text also sits below `<kq>`, `<kq-trivial>`, `<slh-word>`,
`<cant-all-three>`, `<scrdfftar>` and the ketiv/qere singletons. A direct-children-only
walk drops every ketiv/qere and every suspended-letter word without raising anything.
Raise on an unrecognized tag rather than ignoring it, so that a tag added later
announces itself.

**Four element types hold alternatives rather than a stretch of running text**, and for
these a reader has to choose among the children instead of concatenating them:

| Element | The choice |
|---------|-----------|
| `<kq>` | `<kq-k>` (ketiv, unpointed) or `<kq-q>` (qere, pointed) |
| `<cant-all-three>` | `<cant-combined>`, `<cant-alef>`, or `<cant-bet>` |
| `<scrdfftar>` | `<sdt-target>` is the text; `<sdt-note>` is a note about it |
| `<good-ending>` | an added repetition, not part of the running text |

## Child Element Types

The "Text" column says where an element's text is: `text` means the `text` attribute,
`children` means it always has children instead, and `either` means both cases occur.

| Element | Meaning | Text |
|---------|---------|------|
| `<text text="..."/>` | A run of Hebrew text | `text` |
| `<lp-legarmeih/>` | Legarmeh | none |
| `<lp-paseq/>` | Paseq in the narrow sense | none |
| `<implicit-maqaf/>` | Maqaf that is implicit in the manuscript | none |
| `<slh-word>` | An atom with a small, large, or hung letter | children |
| `<letter-small>` | Small letter | `text` |
| `<letter-large>` | Large letter | `text` |
| `<letter-hung>` | Hung (aka suspended) letter | `text` |
| `<kq>` | Ketiv/Qere pair | children |
| `<kq-k>` | Ketiv portion | either |
| `<kq-q>` | Qere portion | either |
| `<kq-trivial>` | Trivial Ketiv/Qere | either |
| `<kq-k-velo-q>` | Ketiv with no Qere | `text` |
| `<kq-k-velo-q-maq/>` | Maqaf after a ketiv with no qere | none |
| `<kq-q-velo-k>` | Qere with no Ketiv | `text` |
| `<cant-all-three>` | Wraps combined, alef, and bet | children |
| `<cant-combined>` | Combined cantillation (1 of 3) | either |
| `<cant-alef>` | Alef cantillation (2 of 3) | either |
| `<cant-bet>` | Bet cantillation (3 of 3) | either |
| `<shirah-space/>` | Shirah (song) spacing | none |
| `<good-ending>` | Repeated ending | `text` |
| `<scrdfftar>` | Targeted scroll-difference note | children |
| `<sdt-target>` | The `<scrdfftar>` target | either |
| `<sdt-note>` | The `<scrdfftar>` note itself | either |
| `<spi-samekh2/>`, `<spi-samekh3/>` | Parashah setumah markers | none |
| `<spi-pe2/>`, `<spi-pe3/>` | Parashah petuḥah markers | none |
| `<spi-invnun/>` | Inverted nun | none |

`<letter-small>`, `<letter-large>` and `<letter-hung>` appear only inside `<slh-word>`.

### Legarmeh and paseq

`<lp-legarmeih>` and `<lp-paseq>` render as the same glyph,
`\N{HEBREW PUNCTUATION PASEQ}` (U+05C0) — there is no separate codepoint for legarmeh.
The two tags record which of the two MAM takes the mark to be, a distinction that is
grammatical rather than graphical: `<lp-legarmeih>` is a legarmeh, which is part of the
cantillation system, and `<lp-paseq>` is a paseq in the narrow sense, which is not.
The OSIS example program annotates the latter with פסק ולא לגרמיה.

So MAM-simple has already made a judgement a bare glyph leaves open, and a reader that
maps both tags onto one output throws that judgement away.

### Ketiv/Qere

`<kq>` has exactly two children, `<kq-k>` (ketiv) and `<kq-q>` (qere). The ketiv is
unpointed and the qere is pointed.

Both children usually have a `text` attribute, but not always:

- A `<kq-q>` may instead have children, when the qere spans a legarmeh or a paseq, e.g.
  1Chr.27.12, where the qere is `<text text="לַבֵּ֣ן"/><lp-paseq/><text text="יְמִינִ֑י"/>`.
- A `<kq-k>` may instead have an `<slh-word>` child. This happens once, at Job.7.5:

```xml
<kq>
  <kq-k>
    <slh-word slhw-desc-0="וגיש" slhw-desc-1=".ג.." slhw-desc-2="ק" slhw-desc-3="ג/ק">
      <text text="ו"/><letter-small text="ג"/><text text="יש"/>
    </slh-word>
  </kq-k>
  <kq-q text="וְג֣וּשׁ"/>
</kq>
```

So when reading a ketiv, try the `text` attribute first and fall back to assembling the
children. Do not silently skip a `<kq-k>` that has neither.

`<kq-trivial>` is for a ketiv/qere whose two forms differ in a way that needs no separate
display. `<kq-k-velo-q>` and `<kq-q-velo-k>` are the singletons: a ketiv that is not read,
and a qere that is not written. `<kq-k-velo-q-maq>` is a maqaf after a ketiv that is not
read, and occurs at 2Kgs.5.18 and 2Sam.13.33.

### Suspended-letter words: `<slh-word>`

`<slh-word>` wraps an atom one or more of whose letters is small (קטנה), large (גדולה),
or hung (תלויה). Its children spell the atom out, with each such letter in a
`<letter-small>`, `<letter-large>`, or `<letter-hung>` element. It also has four
description attributes:

| Attribute | Meaning | Example (Dan.6.20) |
|-----------|---------|--------------------|
| `slhw-desc-0` | The whole atom, pointed | `בִּשְׁפַּרְפָּרָ֖א` |
| `slhw-desc-1` | One character per letter: the letter itself where it is small, large, or hung, and `.` elsewhere; maqafs kept | `..פ.פ..` |
| `slhw-desc-2` | One code per marked letter: `ק` small, `ג` large, `ת` hung | `קג` |
| `slhw-desc-3` | `letter/code` pairs, comma-separated | `פ/ק,פ/ג` |

`slhw-desc-0` is the attribute to reach for when you want the atom as text and do not
care which letters are marked.

`<slh-word>` appears inside `<verse>`, and also inside `<kq-k>`, `<sdt-note>`, and
`<sdt-target>`.

### Scroll differences: `<scrdfftar>`

`<scrdfftar>` has a `<sdt-target>`, which is the text the note is about, and a
`<sdt-note>`, which is the note. Its `sdt-starpos` attribute is `before-word` or
`after-word`, and says on which side of the target the note's marker belongs:

```xml
<scrdfftar sdt-starpos="after-word">
  <sdt-target text="עַל־הָאָֽרֶץ"/>
  <sdt-note>
    <text text="בספרי תימן "/>
    <slh-word slhw-desc-0="הָאָֽרֶץ" ...>...</slh-word>
    <text text=" בצד״י גדולה"/>
  </sdt-note>
</scrdfftar>
```

### The three cantillations: `<cant-all-three>`

`<cant-all-three>` has exactly three children, `<cant-combined>`, `<cant-alef>`, and
`<cant-bet>`, giving three accentuations of the same consonantal text. It appears in the
Decalogue, where MAM has both the תחתון accentuation (`<cant-alef>`) and the עליון one
(`<cant-bet>`), plus a combined form that has the marks of both (`<cant-combined>`).

### Repeated endings: `<good-ending>`

`<good-ending>` has the verse that is repeated after the last verse of a book, so that
the reading ends on a favorable note. It occurs at the end of the four books that have
this custom: Isa.66.24, Mal.3.24, Eccl.12.14, and Lam.5.22.

### `class` attributes

Three elements take an optional `class` attribute:

| Element | `class` | Meaning |
|---------|---------|---------|
| `<kq>` | `sep-maqaf` | Separate ketiv from qere with a maqaf rather than a space (1Chr.9.4, Isa.26.20) |
| `<spi-invnun>` | `including-trailing-space` | The marker includes a trailing space |
| `<spi-samekh3>` | `nu10-invnun-neighbor` | The setumah adjoins an inverted nun of Numbers 10 |

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

`osisID` is on every verse. `yeivinID` is on every verse of the `vtmam` files and on no
verse of the `vtbhs` or `vtsef` ones, so a reader that wants it should read `vtmam`.
The last two attributes are the other way about: they never appear in `vtmam`.

`starts-with-sampe` and `ends-with-sampe` take a bare marker name — `pe2`, `pe3`,
`samekh2`, `samekh3` — rather than the `spi-` prefixed element name.

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
corresponds to. It is absent in the third case, `no verse in MAM`,
there being no source verse to name.

For a description of every place where the three
versifications differ, see
[versification-differences.md](versification-differences.md).
