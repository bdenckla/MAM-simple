"""Exports etel_ons, nsqual"""

import xml.etree.ElementTree as ET


def etel_ons(tag: str, *rest):
    """Return an ET.Element with tag in the OSIS namespace."""
    return ET.Element(_ons(tag), *rest)


def nsqual(namespace: str, tag: str):
    """Namespace-qualify the tag using curly-brackets notation"""
    return "{" + namespace + "}" + tag


def _ons(tag: str):
    return nsqual(NS_URL_FOR_OSIS, tag)


NS_URL_FOR_OSIS = "http://www.bibletechnologies.net/2003/OSIS/namespace"
XSD_URL_FOR_OSIS = "http://www.bibletechnologies.net/osisCore.2.1.1.xsd"
