#! /bin/bash
set -e

FILE=$(which mail.py) 
BASE_DIR=$(dirname "$FILE")

echo "$FILE"
for d in "${PATH//:/ }"; do
    if [[ "$d" ==  "$BASE_DIR" ]]; then
        mail.py -h && exit 0
    fi
done

exit 1

