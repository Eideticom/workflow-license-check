#!/usr/bin/python3

# SPDX-License-Identifer: Apache-2.0
# Copyright (c) 2022, Eidetic Communications Inc.

import argparse
import json
import subprocess
from pathlib import Path
import tempfile
import logging
import sys

def mk_copyright_list(dic):
    copyright_list = []
    for copyright_dict in dic['copyrights']:
        if 'value' in copyright_dict:
            copyright_list.append(copyright_dict['value'])
        elif 'copyright' in copyright_dict:
            copyright_list.append(copyright_dict['copyright'])
    return copyright_list

def strip_directory(directory):
    p = Path(directory)
    parts = p.parts[1:]
    return Path(*parts)

def create_cl_dict(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    final_dict = {}
    for dic in data['files']:
        if "type" in dic and dic['type'] == "file":
            tmp_dict = {}
            tmp_dict['file_type']           = dic['file_type']
            tmp_dict['license_expressions'] = dic['license_expressions']
            tmp_dict['copyrights']          = mk_copyright_list(dic)
            fpath = strip_directory(dic['path'])
            final_dict[fpath] = tmp_dict
    return final_dict

def report_differences(old_dict, new_dict):
    error_flag = False
    for fname, new in new_dict.items():
        if fname not in old_dict:
            logging.info(f"INFO: New file: {fname} detected. Checking now for license expressions and copyrights")

            eid_cpy = any("eidetic" in cpyr.lower()
                          for cpyr in new['copyrights'])

            if not eid_cpy and not new['license_expressions']:
                logging.warning(f"New file {fname} is showing no license_expressions: {new['license_expressions']}")
            else:
                logging.info(f"INFO: New file {fname} is showing license_expressions: {new['license_expressions']}")
            if not new['copyrights']:
                error_flag = True
                logging.error(f"New file {fname} is showing no copyrights: {new['copyrights']}")
            else:
                logging.info(f"INFO: New file {fname} is showing copyrights: {new['copyrights']}")
            continue
        old = old_dict[fname]
        if new['copyrights'] != old['copyrights']:
            if not new['copyrights']:
                error_flag = True
                logging.error(f"{fname} is showing no copyrights: {new['copyrights']}")
            else:
                logging.warning(f"{fname} Copyright has changed from {old['copyrights']} to {new['copyrights']}")
        if new['license_expressions'] != old['license_expressions']:
            logging.warning(f"{fname} License Expression has changed from {old['license_expressions']} to {new['license_expressions']}")
    return error_flag

def run_scancode(directory):
    with tempfile.NamedTemporaryFile() as tmp_base:
        subprocess.check_call(["scancode", "--quiet", "-cli", "--json", tmp_base.name,
                              directory], stderr=subprocess.STDOUT)
        return create_cl_dict(tmp_base.name)

def scancode_git_dir(git_hash, git_dir=None):
    with tempfile.TemporaryDirectory() as tmp_scandir:
            subprocess.check_call(f"git archive '{git_hash}' | " +
                                  f"tar -x -C '{tmp_scandir}'",
                                  shell=True, cwd=git_dir)
            return run_scancode(tmp_scandir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new license json file based upon scancode directory results")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--dirs", action="store_true")
    group.add_argument("-j", "--jsons", action="store_true")
    group.add_argument("-g", "--git", action="store_true")
    parser.add_argument("-G", "--git_dir", type=Path)
    parser.add_argument("-l", "--log", type=argparse.FileType("w"),
                        help="log messages to a file")
    parser.add_argument("-L", "--log-level",
                        default="WARN", choices=["INFO", "WARN", "ERROR"],
                        help="level to log to file")
    parser.add_argument("before")
    parser.add_argument("after")
    args = parser.parse_args()

    root = logging.getLogger()
    fmt = logging.Formatter('%(levelname)s - %(message)s')
    strmhdlr = logging.StreamHandler(sys.stdout)
    strmhdlr.setFormatter(fmt)
    root.addHandler(strmhdlr)
    root.setLevel(logging.INFO)

    if args.log:
        filehdlr = logging.StreamHandler(args.log)
        filehdlr.setLevel(getattr(logging, args.log_level.upper(), None))
        filehdlr.setFormatter(fmt)
        root.addHandler(filehdlr)

    try:
        if args.dirs:
            old_dict = run_scancode(args.before)
            new_dict = run_scancode(args.after)
        elif args.jsons:
            old_dict = create_cl_dict(args.before)
            new_dict = create_cl_dict(args.after)
        elif args.git:
            old_dict = scancode_git_dir(args.before, args.git_dir)
            new_dict = scancode_git_dir(args.after, args.git_dir)

        error_flag = report_differences(old_dict, new_dict)
        sys.exit(error_flag)
    except (subprocess.SubprocessError,
            FileNotFoundError) as e:
        print(e)
