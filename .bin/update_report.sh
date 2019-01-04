#!/bin/bash

git config --global user.name "Travis CI"
git config --global user.email "wirecard@travis-ci.org"

echo "Updating README badge..."
python .bin/process.py

git add docs/index.html
git commit -m "[skip ci] Update docs/index.html file with latest test results"
git push https://$GITHUB_TOKEN@github.com/$TRAVIS_REPO_SLUG HEAD:master
echo "Successfully updated RESULTS file"