#!/bin/bash
echo "Starting log cleaner"
TODAY=$(date +%Y-%m-%d)

TWO_WEEKS_AGO=$(date -d 'now - 2 week' +%Y-%m-%d)

LAST_REPORT_DATE=''
for dir1 in paymentSDK-php/*; do
    for dir2 in $dir1/*; do
        LAST_REPORT_DATE=$(basename -- ${dir2})
        if [ ${LAST_REPORT_DATE} == ${TWO_WEEKS_AGO} ]; then
            echo "Removing directory ${LAST_REPORT_DATE}"
            rm -rf $dir2
        fi
    done
done