#!/usr/bin/python3

# Copyright (c) 2022, Eidetic Communications Inc.
# All rights reserved.

import argparse
import json


def mk_copyright_list(dic):
    copyright_list = []
    for copyright_dict in dic['copyrights']:
        if 'value' in copyright_dict:
            copyright_list.append(copyright_dict['value'])
        elif 'copyright' in copyright_dict:
            copyright_list.append(copyright_dict['copyright'])
    return copyright_list

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

            final_dict[dic['path']] = tmp_dict
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
        description="Create a new license json file based upon scancode json" \
                    " results.")
    parser.add_argument("-b", "--bjson", required=True, \
                        help="The scancode baseline json file.")
    parser.add_argument("-n", "--njson", required=True, \
                        help="The scancode new json file.")
    args = parser.parse_args()

    old_dict = create_cl_dict(args.bjson)
    new_dict = create_cl_dict(args.njson)

    report_differences(old_dict, new_dict)
