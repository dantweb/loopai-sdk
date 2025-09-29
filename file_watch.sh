#!/bin/bash

echo -e "TIME\t\t\tPATH\t\t\tFIRST 30 CHARACTERS"
echo "---------------------------------------------------------------"

WATCH_DIR="/Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops"
fswatch --event Created "$WATCH_DIR" | while read NEWFILE
do
    # Get the current time
    TIME=$(date '+%Y-%m-%d %H:%M:%S')

    # Get the relative path by stripping the WATCH_DIR prefix
    RELATIVE_PATH=$(echo "$NEWFILE" | sed 's|'"$WATCH_DIR"'||')

    # Get the first 100 characters of the file content (if readable)
    if [[ -f "$NEWFILE" ]]; then
        CONTENT=$(head -c 200 "$NEWFILE")
    else
        CONTENT="File is not readable or unavailable"
    fi

    # Format output with fixed-width columns for time and path, allowing multiline for content
    printf "%-20s %-40s %-s\n" "$TIME" "$RELATIVE_PATH" "$CONTENT"
done
