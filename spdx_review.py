#!/usr/bin/python3

# Copyright (c) 2022, Eidetic Communications Inc.
# All rights reserved.

import argparse
import json
import subprocess
import shlex
from pathlib import Path
import tempfile


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
        if "type" in dic or dic['type'] == "file":
            tmp_dict = {}
            tmp_dict['file_type']           = dic['file_type']
            tmp_dict['license_expressions'] = dic['license_expressions']
            tmp_dict['copyrights']          = mk_copyright_list(dic)
            fpath = strip_directory(dic['path'])
            final_dict[fpath] = tmp_dict
    return final_dict

def report_differences(old_dict, new_dict):
    for fname, new in new_dict.items():
        if fname not in old_dict:
            print(f"INFO: New file: {fname} detected." \
                " Checking now for license expressions and copyrights")
            if not new['license_expressions']:
                print(f"WARN: New file {fname} is showing no" \
                      f" license_expressions: {new['license_expressions']}")
            else:
                print(f"INFO: New file {fname} is showing" \
                      f" license_expressions: {new['license_expressions']}")
            if not new['copyrights']:
                print(f"WARN: New file {fname} is showing no" \
                      f" copyrights: {new['copyrights']}")
            else:
                print(f"INFO: New file {fname} is showing" \
                      f" copyrights: {new['copyrights']}")
            continue
        old = old_dict[fname]
        if new['copyrights'] != old['copyrights']:
            print(f"WARN: {fname} Copyright has changed from " \
                  f"{old['copyrights']} to {new['copyrights']}")
        if new['license_expressions'] != old['license_expressions']:
            print(f"WARN: {fname} License Expression has changed from " \
                  f"{old['license_expressions']} to {new['license_expressions']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new license json file based upon scancode \
                        directory results.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--dirs", action="store_true")
    group.add_argument("-j", "--jsons", action="store_true")
    parser.add_argument("before")
    parser.add_argument("after")
    args = parser.parse_args()

    if args.dirs:
        with tempfile.NamedTemporaryFile() as tmp_base:
            subprocess.run(shlex.split(f"scancode -cli --json {tmp_base.name} \
                           {args.before}"), stderr=subprocess.STDOUT)
            old_dict = create_cl_dict(tmp_base.name)
        with tempfile.NamedTemporaryFile() as tmp_new:
            subprocess.run(shlex.split(f"scancode -cli --json {tmp_new.name} \
                           {args.after}"), stderr=subprocess.STDOUT)
            new_dict = create_cl_dict(tmp_new.name)
    elif args.jsons:
        old_dict = create_cl_dict(args.before)
        new_dict = create_cl_dict(args.after)

    report_differences(old_dict, new_dict)
