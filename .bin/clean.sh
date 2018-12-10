#!/bin/bash
set -e # Exit with nonzero exit code if anything fails
REPO_NAME='reports'
REPO_LINK="https://github.com/wirecard/${REPO_NAME}"
REPO_ADDRESS="${REPO_LINK}.git"
TODAY=$(date +%Y-%m-%d)
TWO_WEEKS_AGO=$(date -d 'now - 2 week' +%Y-%m-%d)

echo "Starting log cleaner"

git clone ${REPO_ADDRESS}
cd ${REPO_NAME}

LAST_REPORT_DATE=''
for dir1 in paymentSDK-php/*; do
    for dir2 in $dir1/*; do
        LAST_REPORT_DATE=$(basename -- ${dir2})
        if [ "${LAST_REPORT_DATE}" == "${TWO_WEEKS_AGO}" ]; then
            echo "Removing directory ${LAST_REPORT_DATE}"
            rm -rf $dir2
        fi
    done
done

git add -A
git diff-index --quiet HEAD || git commit -m "Clean up old report files. Travis build: ${TRAVIS_BUILD_WEB_URL}"

git push https://${GITHUB_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git master
