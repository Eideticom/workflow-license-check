# Overview
This example will show you how to produce a copyright and
license difference report using spdx_review.py. The procedure
below will produce sample messages for:
- a new file added to the project and checked for licenses
  and copyrights
- a GO file with a license change
- a Python file with a copyright being added

# Procedure
- Run the ScanCode-Toolkit program against the example directory
  to create a baseline json file.
```
/path/to/scancode -cli --json baseline.json /path/to/example
```
- Run the /path/to/workflow-license-check/example/modify_files.sh script.
```
./modify_files.sh
```
- Run the ScanCode-Toolkit program again on the example directory
  to create a new json file.
```
/path/to/scancode -cli --json new.json /path/to/example
```
- Run /path/to/workflow-license-check/spdx_review.py script using
  the two json files as arguments to produce the differences.
```
python3 spdx_review.py -b /path/to/baseline.json -n /path/to/new.json
```
- Observe the stdout messages that report the differences.
```
INFO: New file: example/new_file.py detected. Checking now for license expressions and copyrights
INFO: New file example/new_file.py is showing license_expressions: ['gpl-3.0-plus']
WARN: New file example/new_file.py is showing no copyrights: []
WARN: Diff in file: example/hello_world.go field: license_expressions old: ['mit'] new: ['gpl-2.0']
WARN: Diff in file: example/hello_world.py field: copyrights old: [] new: ['Copyright (c) 2022, Eidetic Communications Inc.']
```
