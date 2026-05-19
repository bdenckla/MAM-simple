"""Exports body"""

from mb_misc.mb_html import (
    unordered_list,
    para,
    img,
    line_break,
    heading_level_1,
    heading_level_2,
    heading_level_3,
)


def body():
    """Return contents of body element"""
    #
    # Screen captures are from “xulsword” aka “MK”.
    #
    return (
        INTRO,
        UL_TOP_LEVEL,
        H1_FEAT_PRES,
        *sum(SECTIONS_FOR_FEAT_PRES, tuple()),
        H1_FEAT_ABS,
        *sum(SECTIONS_FOR_FEAT_ABS, tuple()),
    )


def _section_ge(heading):
    the_head = heading_level_2(heading)
    the_para = para(
        (
            "Below is one of the 4 good endings. This one is at the end "
            "of Isaiah, whose last verse is 66:24. It repeats the verse "
            "before that (66:23) without pointing. "
            "(Unless otherwise noted, all image captures are from the "
            "xulsword (MK) application.)",
        )
    )
    the_img_br = _img_br("png/good-ending.png")
    return the_head, the_para, *the_img_br


def _section_scrdff(heading):
    the_head = heading_level_2(heading)
    the_para = para(
        (
            "Below is one of the 29 scroll difference notes. This one "
            "is in Exodus 25:31. It is noting the presence of a malei "
            "(full) spelling (note the yod) in scrolls of the Ashkenazic "
            "and Sephardic traditions. (This is as opposed to the ḥaser "
            "(“deficient”) spelling in MapM’s body text.)",
        )
    )
    the_img_br = _img_br("png/scrdff.png")
    return the_head, the_para, *the_img_br


def _section_kq(heading):
    the_head = heading_level_2(heading)
    part1_subhead = heading_level_3(("Ketiv/qere",))
    part1_para1 = para(
        "Below are three examples of ketiv/qere. The first " "is from 1Kgs 1:37."
    )
    part1_para2 = para(
        (
            "The second is from 1Kgs 1:27. It shows how "
            "qere-then-ketiv ordering is used when the qere is at the "
            "end of a maqaf compound.",
        )
    )
    part1_para3 = para(
        (
            "The third is from Isa 26:20 and shows how the ketiv is separated "
            "from the qere by a maqaf instead of a space when the qere "
            "is in the middle of a maqaf compound. (This is one of only "
            "two cases where this awkward situation happens.)",
        )
    )
    part1_imgs = (
        *_img_br("png/kq-ketiv-qere-1.png"),
        *_img_br("png/kq-ketiv-qere-2.png"),
        *_img_br("png/kq-ketiv-qere-3.png"),
    )
    part2_subhead = heading_level_3(("Ketiv velo qere",))
    part2_para1 = para(
        (
            "This is where the ketiv word has no qere counterpart. There "
            "are only 8 cases of ketiv velo qere. Below are two examples. "
            "The first is from Ezekiel 48:16.",
        )
    )
    part2_para2 = para(
        (
            "The second is from 2Sam 13:33. It is one of the two "
            "special cases of ketiv velo qere where a maqaf is appended, "
            "since the ketiv velo qere appears in the middle of a maqaf "
            "compound.",
        )
    )
    part2_imgs = (
        *_img_br("png/kq-ketiv-velo-qere-1.png"),
        *_img_br("png/kq-ketiv-velo-qere-2.png"),
    )
    part2_para3 = para(
        (
            "In MapM, ketiv velo qere isn’t implemented as a feature "
            "independent of normal ketiv/qere, but we still decided "
            "to list it here as a feature that is present rather than "
            "absent. It would perhaps be more clearly present if ketiv "
            "velo qere were presented more explicitly, i.e., more "
            "distinctly from a ketiv that is part of a normal ketiv/qere. "
            "As it is, ketiv velo qere is only presented implicitly: "
            "it can be distinguished from a ketiv that is part of a normal "
            "ketiv/qere only by the fact that there is no adjacent qere "
            "in square brackets.",
        )
    )
    part3_subhead = heading_level_3(("Qere velo ketiv",))
    part3_para1 = para(
        (
            "This is the “dual” of ketiv velo qere. There are "
            "only 9 cases of qere velo ketiv. Below is an example from "
            "2Kgs 19:31.",
        )
    )
    return (
        the_head,
        part1_subhead,
        part1_para1,
        part1_para2,
        part1_para3,
        *part1_imgs,
        part2_subhead,
        part2_para1,
        part2_para2,
        *part2_imgs,
        part2_para3,
        part3_subhead,
        part3_para1,
        *_img_br("png/kq-qere-velo-ketiv.png"),
    )


def _section_par(heading):
    the_head = heading_level_2(heading)
    part1_subhead = heading_level_3(("Parashot setumot of type 1",))
    part1_para1 = para(
        (
            "In English these are sometimes known as “closed sections” "
            "or “closed paragraphs”. Below are two examples of parashot "
            "setumot of type 1. In MapM, a type-1 parashah setumah is "
            "implemented as a line break followed by some horizontal whitespace "
            "(a “tab” or “indent” if you like). (In xulsword, a line break "
            "is also followed by a blank line.)"
            "",
        )
    )
    part1_para2 = para(
        (
            "The first example is a between-verse case, which is by far "
            "the most common case for a parashah setumah of type 1. It "
            "is between 1Kgs 1:27 and 28."
            "",
        )
    )
    part1_para3 = para(
        (
            "The second example is one of only 35 within-verse cases. "
            "This one is within 1Sam 10:11."
            "",
        )
    )
    part1_imgs = (
        *_img_br("png/par-setumah-type-1-number-1.png"),
        *_img_br("png/par-setumah-type-1-number-2.png"),
    )
    part2_subhead = heading_level_3(("Parashot setumot of type 2",))
    part2_para1 = para(
        (
            "Below is a single passage/screen snip containing several "
            "examples of parashot setumot of type 2. In MapM, a parashah "
            "setumah of type 2 is implemented as horizontal whitespace "
            "without a line break. The passage below is from the start "
            "of 1Kgs 4. The passage includes examples of both between-verse "
            "and within-verse cases."
            "",
        )
    )
    part3_subhead = heading_level_3(("Parashot petuḥot of type 1",))
    part3_para1 = para(
        (
            "In English these are sometimes known as “open sections” or “open "
            "paragraphs”. Below are three examples of parashot petuḥot of "
            "type 1. A parashah petuḥah of type 1 (like a parashah petuḥah "
            "of type 2 (see below)) is implemented as a line break. Importantly, "
            "in xulsword, a line break also includes a blank line, i.e., it "
            "includes some vertical whitespace. MapM doesn’t implement parashot "
            "petuḥot of type 1 as distinct from type 2 (both are simply a "
            "line break), but I’m still counting it as a feature present rather "
            "than absent."
            "",
        )
    )
    part3_para2 = para(
        (
            "The first example is a within-verse case. These are rare. "
            "This one is within 1Sam 14:12."
            "",
        )
    )
    part3_para3 = para(
        (
            "The second and third examples, both of which are presented "
            "in the same passage/screen snip, are between-verse cases, "
            "which are by far the more common (there are more than a thousand "
            "of them). These two are in Lev 7. These two between-verse cases "
            "are the subject of scroll difference notes, by the way (hence "
            "the two turquoise “ex” marks in the screen snip below, before "
            "verses 22 and 28)."
            "",
        )
    )
    part3_imgs = (
        *_img_br("png/par-petuḥah-type-1-number-1.png"),
        *_img_br("png/par-petuḥah-type-1-number-2.png"),
    )
    part4_subhead = heading_level_3(("Parashot petuḥot of type 2",))
    part4_para1 = para(
        (
            "Below are three examples of parashot petuḥot of type 2. These "
            "are rare (there are only 18 of them). A parashah petuḥah of type "
            "2 (like a parashah petuḥah of type 1 (see above)) is implemented "
            "as a line break. Unlike type 1, ideally type 2 would be a line "
            "break without an additional blank line, but so be it. Here’s "
            "a within-verse case, from 1Kgs 1:19:"
            "",
        )
    )
    return (
        the_head,
        part1_subhead,
        part1_para1,
        part1_para2,
        part1_para3,
        *part1_imgs,
        part2_subhead,
        part2_para1,
        *_img_br("png/par-setumah-type-2.png"),
        part3_subhead,
        part3_para1,
        part3_para2,
        part3_para3,
        *part3_imgs,
        part4_subhead,
        part4_para1,
        *_img_br("png/par-petuḥah-type-2.png"),
    )


def _section_invnun(heading):
    the_head = heading_level_2(heading)
    the_para1 = para(
        (
            "Inverted nun markers are used in two places: Numbers 10 "
            "and Psalm 107. Here are the Numbers 10 cases, in which the "
            "inverted nun markers “bracket” the span from the start of "
            "verse 35 to the end of verse 36 (the end of the chapter):",
        )
    )
    img_br_nu_10 = _img_br("png/invnun-numbers-10.png")
    the_para2 = para(
        (
            "Here are the Psalm 107 cases, in which the inverted nun "
            "markers “introduce” verses 23 thru 28, and verse 40 (shown "
            "in one-verse-per line mode to make this clearer):",
        )
    )
    img_br_ps_107_1 = _img_br("png/invnun-psalm-107-v23-to-v28.png")
    img_br_ps_107_2 = _img_br("png/invnun-psalm-107-v40.png")
    return (
        the_head,
        the_para1,
        *img_br_nu_10,
        the_para2,
        *img_br_ps_107_1,
        *img_br_ps_107_2,
    )


def _section_shirah(heading):
    the_head = heading_level_2(heading)
    the_para = para(
        (
            "In MapM, a shirah space looks just like a parashah setumah "
            "of type 2. So, as with other features we’ve seen, perhaps "
            "I’ve been a bit optimistic to consider this feature present "
            "rather than absent. Here’s what the start of Exodus 15 (“Az "
            "Yashir” aka “Song at the Sea”) looks like (it is full of "
            "shirah spaces):",
        )
    )
    the_img_br = _img_br("png/shirah-space.png")
    return the_head, the_para, *the_img_br


def _section_paseq(heading):
    the_head = heading_level_2(heading)
    the_para = para(
        (
            "In MapM, unlike any other edition of MAM, legarmeih is "
            "distinguished "
            "from paseq by having each paseq followed by a note reading "
            "פסק ולא לגרמיה (paseq velo legarmeih, i.e. “paseq and not "
            "legarmeih”). Lev 10:6 shows both marks in close proximity:",
        )
    )
    the_img_br = _img_br("png/paseq.png")
    return the_head, the_para, *the_img_br


def _section_slh(heading):
    head = heading_level_2(heading)
    intro_para_1 = para(
        (
            "Special letters are a feature not directly present in MapM. "
            "(A special letter is one that is small, large, or hung.) "
            "Special letters are not directly present "
            "since OSIS does not support small or large formatting, "
            "and it seemed inconsistent to have hung letters (via “super”) "
            "without small or large letters. "
            "Also, hung formatting via “super” is imperfect since typically "
            "a “super” letter is not only raised but also small.",
        )
    )
    intro_para_2 = para(
        (
            "Special letters are indirectly present in MapM via notes. "
            "(Thus, we could have considered this feature present "
            "rather than absent, but we opted to categorize it as absent.) "
            "We call these notes on special letters “slh notes”."
            "",
        )
    )
    sik_para_intro = para(
        (  # sik: small in ketiv
            "Compare this ketiv/qere from Job 7:5 as rendered in MapM "
            "(via xulsword) vs. MAM-WS (MAM on Hebrew Wikisource):",
        )
    )
    sik_img_br_a = _img_br("png/sm-lett-absent-OSIS.png")
    sik_img_br_b = _img_br("png/sm-lett-present-WS.png")
    sik_para_outro = para(
        (
            "Ignoring the different way ketiv/qere is presented on MAM-WS, "
            "note that the gimel in the ketiv is small."
            " "
            "(This is actually the only case in MapM where a special letter "
            "appears in a ketiv.)"
            " "
            "An “slh note” consists of two parts:"
            "",
        )
    )
    osol_para = para(
        (  # osol: one small, one large
            "Daniel 6:20 provides an example of two special "
            "letters in a normal word. The first pe is small and the second pe "
            "is large:",
        )
    )
    osol_img_br_a = _img_br("png/sm-lett-and-lg-lett-absent-OSIS.png")
    osol_img_br_b = _img_br("png/sm-lett-and-lg-lett-present-WS.png")
    hung_para = para(
        (
            "In Judges 18:30, we find one of "
            "the four hung (aka suspended) letters in MAM:",
        )
    )
    hung_img_br_a = _img_br("png/hung.png")
    return (
        head,
        intro_para_1,
        intro_para_2,
        sik_para_intro,
        *sik_img_br_a,
        *sik_img_br_b,
        sik_para_outro,
        _sik_slh_word_note_list(),
        osol_para,
        *osol_img_br_a,
        *osol_img_br_b,
        hung_para,
        *hung_img_br_a,
    )


def _sik_slh_word_note_list():
    licont11 = "Part 1 of 3 is the word itself. In this example, it is “וגיש”."
    licont12 = (
        "Part 2 of 3 is the word with special letters shown "
        "and regular letters replaced by periods. "
        "Maqaf marks are also shown. "
        "In this "
        "example, part 2 is “.ג..”."
    )
    licont13 = (
        "Part 3 of 3 is a string of one-letter codes for the "
        "formatting we “wish” we had for the special letters. "
        "In this example, it is “ק”. The one-letter codes are "
        "as follows:",
        unordered_list(
            (
                "qof for qetanah (small)",
                "gimel for gedolah (large)",
                "tav for תלויה (hung)",
            )
        ),
    )
    licont1 = (
        "The first part of an “slh note” is a compact but cryptic "
        "representation of the special formatting in this word. "
        "In this example, it is “וגיש/.ג../ק”. "
        "This representation has 3 parts:",
        unordered_list((licont11, licont12, licont13)),
    )
    licont2 = (
        "The second part of an “slh note” is a more verbose description of "
        "the special letters. In this example, it is “אות גימ״ל קטנה”.",
    )
    return unordered_list((licont1, licont2))


def _section_abcant(heading):
    the_head = heading_level_2(heading)
    the_para1 = para(
        (
            "Like many editions of MAM, MapM does not show the “A” and “B” "
            "cantillations. By “A” and “B” I mean the single "
            "cantillations that, together, can be used to represent "
            "the two cantillations of a dually-cantillated phrase. "
            "Dually-cantillated phrases exist only in "
            "the Exodus Decalogue, the Deuteronomy Decalogue, "
            "and Genesis 35:22. So, for example, MapM only shows the "
            "combined cantillation for this phrase from Gen 35:22:",
        )
    )
    the_img_br1 = _img_br("png/abcant-absent-OSIS.png")
    the_para2 = para(
        (
            "Whereas, MAM-WS shows not only the combined cantillation "
            "but also the “A” and “B” cantillations, which MAM-WS refers to as the "
            "פשוטה (pashutah) and מדרשית (midrashit) cantillations "
            "respectively:",
        )
    )
    the_img_br2 = _img_br("png/abcant-present-WS.png")
    return the_head, the_para1, *the_img_br1, the_para2, *the_img_br2


def _section_impmaq(heading):
    the_head = heading_level_2(heading)
    the_para1 = para(
        "Compare the maqaf in this maqaf compound in Job 3:4 in MapM " "vs MAM-WS:"
    )
    the_img_br1 = _img_br("png/impmaq-absent.png")
    the_para2 = para(
        (
            "Note that the maqaf in MAM-WS is gray. This indicates that this "
            "maqaf is supplied by MAM, although no such maqaf is present "
            "in the manuscript MAM is based on (the Aleppo Codex).",
        )
    )
    the_img_br2 = _img_br("png/impmaq-present.png")
    return the_head, the_para1, *the_img_br1, the_para2, *the_img_br2


def _img_br(img_path):
    return img({"src": img_path}), line_break()


INTRO = para(
    (
        "This document describes some notable aspects "
        "of the OSIS edition of MAM (Miqra `al pi ha-Masorah). "
        "(The SWORD module called MapM "
        "is built from the OSIS edition of MAM.) "
        "This document describes OSIS MAM "
        "in terms of notable features present "
        "and notable features absent.",
    )
)
HEADING_GE = "Good endings (4 of them)"
HEADING_SCRDFF = "Scroll difference notes (29 of them)"
HEADING_KQ = "Ketiv/qere, ketiv velo qere, & qere velo ketiv"
HEADING_PAR = "Parashot setumot & petuḥot, each of types 1 & 2"
HEADING_INVNUN = "Inverted nun markers (Numbers 10 & Psalm 107 types)"
HEADING_SHIRAH = "Shirah spaces"
HEADING_PASEQ = "Paseq marks (as distinct from legarmeih marks)"
HEADING_HUNG = "Hung letters"
#
HEADING_SLH = "Small, large, & hung letters"
HEADING_ABCANT = "“A” and “B” cantillations"
HEADING_IMPMAQ = "Implicit maqaf marks"
SH_PAIRS_FOR_FEAT_PRES = (  # SH: section (function) & heading
    (_section_ge, HEADING_GE),
    (_section_scrdff, HEADING_SCRDFF),
    (_section_kq, HEADING_KQ),
    (_section_par, HEADING_PAR),
    (_section_shirah, HEADING_SHIRAH),
    (_section_invnun, HEADING_INVNUN),
    (_section_paseq, HEADING_PASEQ),
)
SH_PAIRS_FOR_FEAT_ABS = (  # SH: section (function) & heading
    (_section_slh, HEADING_SLH),
    (_section_abcant, HEADING_ABCANT),
    (_section_impmaq, HEADING_IMPMAQ),
)
LICONTS_FOR_FEAT_PRES = tuple(
    HEADING_sec for _sec_fun, HEADING_sec in SH_PAIRS_FOR_FEAT_PRES
)
LICONTS_FOR_FEAT_ABS = tuple(
    HEADING_sec for _sec_fun, HEADING_sec in SH_PAIRS_FOR_FEAT_ABS
)
SECTIONS_FOR_FEAT_PRES = tuple(
    sec_fun(HEADING_sec) for sec_fun, HEADING_sec in SH_PAIRS_FOR_FEAT_PRES
)
SECTIONS_FOR_FEAT_ABS = tuple(
    sec_fun(HEADING_sec) for sec_fun, HEADING_sec in SH_PAIRS_FOR_FEAT_ABS
)
UL_FEAT_PRES = unordered_list(LICONTS_FOR_FEAT_PRES)
UL_FEAT_ABS = unordered_list(LICONTS_FOR_FEAT_ABS)
STR_FEAT_PRES = "Features present"
STR_FEAT_ABS = "Features absent"
UL_TOP_LEVEL = unordered_list(
    ((STR_FEAT_PRES, UL_FEAT_PRES), (STR_FEAT_ABS, UL_FEAT_ABS))
)
H1_FEAT_PRES = heading_level_1((STR_FEAT_PRES,))
H1_FEAT_ABS = heading_level_1((STR_FEAT_ABS,))
