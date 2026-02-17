#!/usr/bin/env python3

import sys
import re

file_name = sys.argv[1]
with open(file_name, "r") as file:
    print(f"[+] Opened {file_name}", file=sys.stderr)

    found_head = False
    found_local = False
    last_line_of_local = str()

    for line in file:
        line = line.rstrip()
        if line.startswith("<<<<<<<"):
            found_head = True
        elif line.startswith("======="):
            found_head = False
            found_local = True
        elif line.startswith(">>>>>>>"):
            found_local = False
            if last_line_of_local.startswith("syz_prepare_data"):
                print(last_line_of_local)
        else:
            # if we found the less-than-sign bar, then we're looking
            # at a line from HEAD (we want to edit this)
            #     if the line has parentheses, it's probably got a
            #     function call in it, and we should prepend this
            #     line with `syz_prepare_data(0x0)`
            #
            #     otherwise, just print out the line as-is
            if found_head and re.search(".+\\(.*\\).*", line) is not None:
                print("syz_prepare_data(0x0)")

            # if we found the equal-sign bar, then we finished
            # the HEAD diff and we're now looking at the local diff
            #     if the last line is `syz_prepare_data`, then keep
            #     the line (print it) because it might've been meant
            #     for the next line after the local diff
            if found_local:
                last_line_of_local = line
                continue

            # if we found the more-than-sign bar, then we finished
            # the local diff
            #
            # also, don't print empty lines if possible
            if line.isspace():
                continue

            # if none of that applies, just print the line as-is
            print(line)
