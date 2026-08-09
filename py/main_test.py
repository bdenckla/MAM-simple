"""Run this repo's test suite.

Examples:
    .venv/Scripts/python.exe py/main_test.py
    .venv/Scripts/python.exe py/main_test.py --list
    .venv/Scripts/python.exe py/main_test.py -v
    .venv/Scripts/python.exe py/main_test.py tests.test_h_dot_below_nfc

With no arguments this runs everything under py/tests. Naming one or more
modules (dotted, as unittest spells them) runs just those.

WHY THIS FILE EXISTS

Until 2026-08-09 it did not, and py/tests/test_h_dot_below_nfc.py was reachable
only by someone choosing to run that one file by name. An unregistered test file
does not skip and does not warn: it reports nothing at all, so the suite looks
green having executed none of it. MAM-basics and holman-ketiv-qere each had two
such files, found 2026-07-30, one of them edited four times over seven weeks
while never once running.

WHY DISCOVERY, AND NOT A REGISTRY OF MODULE NAMES

A hand-maintained tuple of test modules would reintroduce exactly the failure
this file exists to end, one file later. MAM-basics dropped its registry for
that reason on 2026-08-01, and al-hatorah's py/main_test.py discovers for the
same reason. unittest finds the files itself here, so there is nothing to fall
out of sync; --list says what it found.

WHY unittest AND NOT pytest

MAM-basics runs pytest, but this repo's venv holds black and nothing else, and
there is no requirements.txt to record a second dependency in. The one test file
here is a unittest.TestCase already, so the stdlib runner costs nothing and a
fresh clone needs no install to run the suite.

NOTHING IS IMPORTED FROM py/ HERE, AND THAT IS THE POINT

CPython puts a script's directory at sys.path[0], so running py/main_<x>.py puts
py/ on the path with nothing added by hand. This repo happens to keep no library
modules under py/ for a test to import -- py-examples/ is where its vendored
Python lives, and that is not on the path. So no conftest.py, pytest.ini
pythonpath, .pth file, exported PYTHONPATH or sitecustomize.py belongs here
either; the count of those is zero, not one.
"""

import sys
import unittest
from pathlib import Path

PY_DIR = Path(__file__).resolve().parent
TESTS_DIR = PY_DIR / "tests"


def _discover():
    """Every test module under py/tests, imported as tests.test_<x>."""
    return unittest.defaultTestLoader.discover(
        start_dir=str(TESTS_DIR),
        pattern="test_*.py",
        top_level_dir=str(PY_DIR),
    )


def _module_names(suite):
    names = set()
    for test in _flatten(suite):
        names.add(type(test).__module__)
    return sorted(names)


def _flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _flatten(item)
        else:
            yield item


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--list" in args:
        suite = _discover()
        # A discovery failure arrives as a synthetic test whose module is
        # unittest.loader, so say what was found rather than only how many.
        for name in _module_names(suite):
            print(name)
        print(f"{suite.countTestCases()} tests in {len(_module_names(suite))} modules")
        return 0
    verbosity = 2 if "-v" in args else 1
    names = [arg for arg in args if not arg.startswith("-")]
    if names:
        suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    else:
        suite = _discover()
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
