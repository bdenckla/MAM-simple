"""File I/O utilities."""

import os
import pathlib
import json
import time

from mb_cmn import provenance

__all__ = ["with_tmp_openw", "json_dump_to_file_path"]


def with_tmp_openw(out_path: str, kwargs_dic, write_fun, *write_fun_args):
    """Open path for writing, but through a temporary file"""
    tpath = _tmp_path(out_path)
    with _openw(tpath, **kwargs_dic) as outfp:
        retval = write_fun(*write_fun_args, outfp)
    _replace_file(tpath, out_path)
    return retval


def json_dump_to_file_path(dumpable, out_path: str, generator_file: str = None):
    """Dump JSON to a file path"""
    if generator_file is not None:
        dumpable = provenance.with_json_provenance(dumpable, generator_file)
    with_tmp_openw(out_path, {}, _json_dump_to_file_pointer, dumpable)


def _replace_file(tmp_path: str, path: str):
    fail_count = 0
    succeeded = False
    while not succeeded:
        try:
            os.replace(tmp_path, path)
            succeeded = True
        except PermissionError:
            if _too_many_fails(fail_count):
                raise
            fail_count += 1
            _sleep(fail_count)


def _too_many_fails(fail_count):
    return fail_count > 5


def _sleep(fail_count):
    sleep_time = 2**fail_count
    print(f"Sleeping {sleep_time} seconds before trying again ...")
    time.sleep(sleep_time)


def _openw(out_path: str, **kwargs):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    return open(out_path, "w", encoding="utf-8", **kwargs)


def _tmp_path(path: str):
    pathobj = pathlib.Path(path)
    # e.g. from /dfoo/dbar/stem.ext return /dfoo/dbar/stem.tmp.ext
    # where suffix = .ext
    return pathobj.parent / (str(pathobj.stem) + ".tmp" + pathobj.suffix)


def _json_dump_to_file_pointer(dumpable, out_fp):
    json.dump(dumpable, out_fp, ensure_ascii=False, indent=2)
    out_fp.write("\n")
