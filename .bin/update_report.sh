#!/bin/bash

git config --global user.name "Travis CI"
git config --global user.email "wirecard@travis-ci.org"

echo "Check if there is more then 3 versions of every plugin..."
python .bin/remove.py

echo "Updating README badge..."
python .bin/process.py

git add -A
git diff-index --quiet HEAD || git commit -m "[skip ci] Update docs/index.html file with latest test results"
git push https://$GITHUB_TOKEN@github.com/$TRAVIS_REPO_SLUG HEAD:master
echo "Successfully updated RESULTS file"