# Overview
Workflow-license-check will allow you to review any project files to check for
license expressions and copyrights. The project file review can be performed
using the spdx_review.py file.

# Basic Use Case: Reporting SPDX License or Copyright Changes
- Download and install ScanCode-Toolkit
- Use the ScanCode-Toolkit on the project folder to produce a json output file
- Store this json output file as your baseline json
- Make changes to files in the project folder over time. In particular, license
  expressions or copyrights
- Use the ScanCode-Toolkit on the project folder to produce a new json file
- Store this json output file as your new json
- Use the spdx_review.py script on both baseline and new json files
- This will report the license and/or copyright differences

# Prerequisites
1. Python 3.6 or higher
2. Download the ScanCode-Toolkit from github:
https://github.com/nexB/scancode-toolkit
3. For installation, using pip is the recommended way:
- https://scancode-toolkit.readthedocs.io/en/latest/getting-started/install.html#installation-as-a-library-via-pip
```
$ sudo pip install scancode-toolkit
```
4. Verify that scancode works on the command line:
```
# Basic scancode usage test after installed with pip
$ scancode --help
```
# How to Perform ScanCode to Create a JSON File
Choose a destination file or folder that contains your project you want to scan.

Example to create a baseline json file before any files are change:
```
$ scancode -cli --json baseline_project.json /home/project_files/
```
Example to create a new json file after there are changes to the files:
```
$ scancode -cli --json new_project.json /home/project_files/
```
# How to Report License/Copyright Differences using spdx_review.py
Requires you to have a baseline json and a new json file for the comparison.

Example:
```
...
usage: spdx_review.py [-h] -b BJSON -n NJSON
spdx_review.py: error: the following arguments are required: -b/--bjson, -n/--njson
```
Run the python script using the two json files as arguments:
```
$ python3 spdx_review.py -b baseline_project.json -n new_project.json
```
This will produce stdout messages reporting any differences with licenses or
copyrights. It will also report when a new file has been added along with those
basic checks as well.

Below is a list of example comparison reports based upon the differences.

Example of when a file is removed:
```
The removed file is not checked and nothing is reported.
```
Example results for added files:
```
# A new file is added which has a license expression and a copyright
INFO: New file: old_files/new_file_w_both.c detected. Checking now for license expressions and copyrights
INFO: New file old_files/new_file_w_both.c is showing license_expressions: ['mit', 'gpl-2.0']
INFO: New file old_files/new_file_w_both.c is showing copyrights: ['Copyright (c) 2009-2017 Dave Gamble and cJSON contributors']
# A new file is added with license expression and NO copyright
INFO: New file: old_files/new_file_w_lic.c detected. Checking now for license expressions and copyrights
INFO: New file old_files/new_file_w_lic.c is showing license_expressions: ['gpl-2.0']
WARN: New file old_files/new_file_w_lic.c is showing no copyrights: []
# A new file is added with NO license expression and NO copyright
INFO: New file: old_files/no_lic_no_cr.c detected. Checking now for license expressions and copyrights
WARN: New file old_files/no_lic_no_cr.c is showing no license_expressions: []
WARN: New file old_files/no_lic_no_cr.c is showing no copyrights: []
# A new file is added with NO license expression but has copyright
INFO: New file: old_files/none_to_added_cr.sh detected. Checking now for license expressions and copyrights
WARN: New file old_files/none_to_added_cr.sh is showing no license_expressions: []
INFO: New file old_files/none_to_added_cr.sh is showing copyrights: ['Copyright (c) 2022, Eidetic Communications Inc.']
```

Example results for existing files with changes:
```
# Existing file copyright removal
WARN: Diff in file: old_files/cr_to_no_cr.java field: copyrights old: ['Copyright (c) 2021. Eidetic Communications Inc.'] new: []
# license expression changed
WARN: Diff in file: old_files/lic_changed.cpp field: license_expressions old: ['gpl-2.0'] new: ['mit']
# license expression removed
WARN: Diff in file: old_files/lic_to_no_lic.py field: license_expressions old: ['mit'] new: []
# copyright removed
WARN: Diff in file: old_files/no_lic_yes_cr.c field: copyrights old: ['Copyright (c) 2019. Eidetic Communications Inc.'] new: []
# copyright from none to added
WARN: Diff in file: old_files/none_to_added_cr.sh field: copyrights old: [] new: ['Copyright (c) 2019. Eidetic Communications Inc.']
# An existing file is renamed
WARN: Diff in file: old_files/no_lic_no_cr.c field: file_name old: old_files/no_lic_no_cr.c new: old_files/new_file_w_cr.h
```

