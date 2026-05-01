import argparse
import os

from mb_cmn import bib_locales as tbn


def get_bk39_tuple_from_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--book39")  # e.g. 1Samuel not I Samuel
    parser.add_argument("--section6")  # e.g. SifEm
    args = parser.parse_args()
    if args.book39:
        # I think there's a way to tell the argument parser that two arguments
        # are exclusive; if so perhaps I should use that instead of the assert
        # below.
        assert not args.section6
        return (args.book39,)
    if args.section6:
        return tbn.bk39s_of_sec(args.section6)
    return tbn.ALL_BK39_IDS


def show_progress_g(uufileuu, *rest):
    # label is usually some sort of book name
    bn_uufileuu = os.path.basename(uufileuu)
    bn_and_rest = " ".join((bn_uufileuu, *rest))
    print(bn_and_rest)
