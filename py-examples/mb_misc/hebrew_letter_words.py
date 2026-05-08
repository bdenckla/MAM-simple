"""Exports letters_and_maqafs"""

import re


def letters_and_maqafs(string: str):
    """Return only the letters and maqaf marks in the given string"""
    # I.e. strip any the vowel points and/or accents
    # Another approach would be to filter based on
    # unicodedata.category(char) == 'Lo'.
    pattern = r"[^א-ת־]*"
    return re.sub(pattern, "", string)
