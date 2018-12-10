#!/bin/bash
set -e # Exit with nonzero exit code if anything fails
export REPO_NAME='reports'
export REPO_LINK="https://github.com/wirecard/${REPO_NAME}"
export REPO_ADDRESS="${REPO_LINK}.git"

echo "Starting log cleaner"
git clone ${REPO_ADDRESS}

cd ${REPO_NAME}
git checkout tatsta-patch-1

TODAY=$(date +%Y-%m-%d)
TWO_WEEKS_AGO=$(date -d 'now - 2 week' +%Y-%m-%d)

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
#echo "Before add"
#git status
git add -A
echo "After add"
git status
#git diff-index  HEAD 
git diff-index --quiet HEAD || git commit -m "Clean up old report files. Travis build: ${TRAVIS_BUILD_WEB_URL}" 
echo "After commit"
git status

git push https://${GITHUB_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git tatsta-patch-1
echo "After push"
git status
