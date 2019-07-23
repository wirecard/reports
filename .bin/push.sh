#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

git add -A
git diff-index --quiet HEAD || git commit -m "Update versions. Travis build: ${TRAVIS_BUILD_WEB_URL}"

git push https://${GITHUB_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git TPWDCEE-4326