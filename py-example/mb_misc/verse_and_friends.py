"""Exports VerseAndFriends"""

from dataclasses import dataclass


@dataclass
class VerseAndFriends:
    """Holds verse, maybe a next CP, & maybe a good ending."""

    verse: tuple
    vaf_next_cp: tuple
    good_ending: tuple

    def map_over(self, fun):
        """
        Make a new veraf by mapping fun over the fields of this veraf.
        """
        if isinstance(fun, tuple):
            return VerseAndFriends(
                fun[0](*fun[1:], self.verse),
                fun[0](*fun[1:], self.vaf_next_cp),
                fun[0](*fun[1:], self.good_ending),
            )
        return VerseAndFriends(
            fun(self.verse),
            fun(self.vaf_next_cp),
            fun(self.good_ending),
        )
