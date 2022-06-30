#!/bin/bash

# Add a new file to the project
cp hello_world.py new_file.py

# Change the license from MIT to GPL-2.0
sed -i -e 's/MIT/GPL-2.0/g' hello_world.go

# Add a copyright
sed -i '/\SPDX-License-Identifier/i # Copyright (c) 2022, Eidetic Communications Inc.' hello_world.py
