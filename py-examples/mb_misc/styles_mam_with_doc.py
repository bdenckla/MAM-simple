MWD_STYLES_STR = """
:root {
  color-scheme: light dark;
}
.element {
  color: light-dark(black, white);
  background-color: light-dark(white, black);
}
body {
    font-size: 14pt;
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
span.mam-dqq-unstressed { font-feature-settings: 'ss01', 'ss02'; }
/* ss01 = xataf qamats qatan */
/* ss02 = qamats qatan with small meteg */
span.mam-letter-small { font-size: 85%; }
span.mam-letter-large { font-size: 125%; }
span.mam-letter-hung { vertical-align: super; }
span.mam-lp-legarmeih { font-weight: bold; }
span.mam-lp-paseq { font-size: 85%; }
span.mam-implicit-maqaf { color: gray; }
span.mam-note-callout { color: light-dark(red, pink); }
span.mam-doc-callout { color: light-dark(red, pink); }
span.mam-doc-lemma { color: light-dark(blue, lightblue); }
span.mam-doc-target-without-callout { color: light-dark(blue, lightblue); }
table.border-collapse { border-collapse: collapse; }
th, td { padding-right: 0.4em; padding-left: 0.4em; }
*.bordered { border: 1px solid; }
*.top-n-bot-bordered { border-top: 1px solid; border-bottom: 1px solid; }
*.small { font-size: 85%; }
*.end-aligned { text-align: end; }
"""


def make_css_file_for_mwd(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(MWD_STYLES_STR.lstrip())

