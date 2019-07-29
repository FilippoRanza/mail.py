#! /bin/bash
set -e

FILE=$(which mail.py) 
BASE_DIR=$(dirname "$FILE")

echo "$FILE"
for d in $(echo "$PATH" | sed 's|:| |g'); do
    [[ "$d" ==  "$BASE_DIR" ]] && exit 0
done

exit 1

