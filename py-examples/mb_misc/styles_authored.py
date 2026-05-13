AUTHORED_STYLES_STR = """
/* Generated file - DO NOT EDIT DIRECTLY.
     Edit py/mb_misc/styles_authored.py in MAM-basics and regenerate. */
:root {
  color-scheme: light dark;
}
.element {
  color: light-dark(black, white);
  background-color: light-dark(white, black);
}
body {
    max-width: 40em;
    width: 90%;
    margin-left: auto;
    margin-right: auto;
    font-size: 14pt;
}
body.wide {
    max-width: 80em;
}
*[lang="hbo"] {
    font-family: "Taamey D WOFF2";
    font-size: 140%;
    font-feature-settings: 'ss01'; /* ss01 = xataf qamats qatan */
}
@font-face {
    font-family: "Taamey D WOFF2";
    src: url("woff2/Taamey_D.woff2");
}
em { font-style: normal; font-weight: bold; }
span.romanized { font-style: italic; }
*[lang="he"] span.book-title { font-weight: bold; font-style: normal; }
span.book-title { font-style: italic; }
abbr.small-caps { text-transform: lowercase; font-variant: small-caps; }
p { text-align: justify; }
li { text-align: justify; }
blockquote { text-align: justify; }
*.extra-letter-spacing { letter-spacing: 0.1em; } /* span or bdi */
*.gray { color: gray; }
*.big { font-size: 250%; }
table.border-collapse { border-collapse: collapse; }
table.center { margin-left: auto; margin-right: auto; }
p.center { text-align: center; }
p.center-and-spaced { text-align: center; word-spacing: 1.5em; }
img.width10em { width: 10em; }
img.width5em { width: 5em; }
th, td { padding-right: 0.4em; padding-left: 0.4em; }
img { max-width: 100%; }
"""


def make_css_file_for_authored(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(AUTHORED_STYLES_STR.lstrip())
