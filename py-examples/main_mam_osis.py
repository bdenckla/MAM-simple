"""Convert MAM data to OSIS (Open Scripture Information Standard) XML format."""

import xml.etree.ElementTree as ET
import copy
import lxml.etree as lxml_etree

from mb_misc import my_utils_for_mainish as my_utils_fm
from mb_misc import mb_html
from mb_cmn import bib_locales as tbn
from mb_misc import two_col_css_styles as tcstyles
from mb_misc import osis_book_abbrevs
from mb_cmn import my_utils
from mb_cmn import file_io
from mb_cmn import provenance
from mb_cmn import shrink
from osis import osis_namespace as osisn
from osis import osis_handlers
from osis import osis_index_html


def _handle(handlers, etel):  # etel: ElementTree element
    tag_and_class = etel.tag, etel.attrib.get("class")
    attr_text = etel.attrib.get("text")
    ofc1_raw = []  # output for all children, summed together
    ofc2 = {}  # output for all children, per child
    child_handlers = osis_handlers.child_handlers(tag_and_class)
    for child in etel:
        output_for_child = _handle(child_handlers, child)
        ofc1_raw.extend(output_for_child)
        ofc2[child] = output_for_child
    ofc1 = shrink.shrink_xml(ofc1_raw)
    if attr_text is not None:
        assert not ofc1
        ofc1 = [attr_text]
    handler = handlers[tag_and_class]
    return handler(etel, ofc1, ofc2)


def _process_bk24(root):
    singleton = _handle(osis_handlers.HANDLERS, root)
    sing0 = my_utils.first_and_only(singleton)
    stem = sing0.attrib.get("scope") or sing0.attrib.get("osisID")
    assert stem  # e.g. Gen or 1Chr-2Chr
    return sing0, stem


def _write_xml(root, out_path):
    xml_elementtree = ET.ElementTree(root)
    xml_elementtree2 = copy.deepcopy(xml_elementtree)
    # Above, we make a copy because otherwise, during indent(), constants
    # are mutated to have tails!
    ET.indent(xml_elementtree2)
    ET.register_namespace("", osisn.NS_URL_FOR_OSIS)
    ET.register_namespace("xml", _NS_URL_FOR_XML)
    ET.register_namespace("xsi", _NS_URL_FOR_XSI)
    file_io.with_tmp_openw(out_path, {}, _write_callback, xml_elementtree2)


def _write_callback(xml_elementtree2, out_fp):
    xml_elementtree2.write(out_fp, encoding="unicode", xml_declaration=True)
    out_fp.write("\n")


def _do_one_book_group(bkg):
    bkg_name = bkg["bkg-name"]
    xml_path = f"../MAM-simple/out/xml-vtrad-bhs/{bkg_name}.xml"
    tree = ET.parse(xml_path)
    root = tree.getroot()
    proot, filename_stem = _process_bk24(root)
    out_path = f"../MAM-OSIS/MAPM-24/{filename_stem}.xml"
    _write_xml(proot, out_path)
    return proot


def _read_header():
    xml_path = "../MAM-OSIS/header.xml"
    tree = ET.parse(xml_path)
    return tree.getroot()


def _write_osis(header, proots):
    osis_text_attrs = {
        osisn.nsqual(_NS_URL_FOR_XML, "lang"): "he",
        "osisIDWork": "MapM",
        "osisRefWork": "Bible",
    }
    osis_text = osisn.etel_ons("osisText", osis_text_attrs)
    osis_text.append(header)
    osis_text.extend(proots)
    out_path = "../MAM-OSIS/mapm.osis.xml"
    schema_loc_key = osisn.nsqual(_NS_URL_FOR_XSI, "schemaLocation")
    schema_loc_val = osisn.NS_URL_FOR_OSIS + " " + osisn.XSD_URL_FOR_OSIS
    root = osisn.etel_ons("osis", {schema_loc_key: schema_loc_val})
    root.append(osis_text)
    _write_xml(root, out_path)
    _assert_is_valid_osis_according_to_xsd(out_path)


def _assert_is_valid_osis_according_to_xsd(xml_path: str):
    xsd_path = "in/osisCore.2.1.1-cw6.xsd"
    xmlschema_doc = lxml_etree.parse(xsd_path)
    xmlschema = lxml_etree.XMLSchema(xmlschema_doc)
    #
    xml_doc = lxml_etree.parse(xml_path)
    xmlschema.assertValid(xml_doc)


def _write_index_dot_html():
    body_contents = osis_index_html.body()
    # Write into the repository's GitHub Pages publish directory.
    title = "MAM OSIS: features present and features absent"
    out_dir_path = "../MAM-OSIS/gh-pages"
    css_href = "two_col_style.css"
    tcstyles.make_css_file_for_mwd(f"{out_dir_path}/{css_href}")
    write_ctx = mb_html.WriteCtx(
        title,
        f"{out_dir_path}/index.html",
        css_hrefs=(css_href,),
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(body_contents, write_ctx)


def almost_main(bkids=None):
    """Create MAM-OSIS from MAM-XML."""
    if bkids is None:
        bkids = tbn.ALL_BK39_IDS
    _write_index_dot_html()
    bkgs = osis_book_abbrevs.bk24_bkgs(bkids)
    proots = tuple(map(_do_one_book_group, bkgs))
    header = _read_header()
    _write_osis(header, proots)


def main():
    """Create MAM-OSIS from MAM-XML."""
    bkids = my_utils_fm.get_bk39_tuple_from_argparse()
    almost_main(bkids)


_NS_URL_FOR_XSI = "http://www.w3.org/2001/XMLSchema-instance"
_NS_URL_FOR_XML = "http://www.w3.org/XML/1998/namespace"
if __name__ == "__main__":
    main()
