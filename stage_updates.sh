#!/bin/bash

set -e

gh pr list

if [[ $? -ne 0 ]]; then
  echo "gh cli not configured or other error"
  exit 1
fi
# stop if exit code not 0
git checkout main

git pull

git checkout -b staging_`date +%Y%m%d`

# push new branch
git push --set-upstream origin staging_`date +%Y%m%d`

echo "Release Info:"
gh release list --limit 1 --repo bigfix/site_updates_linux_apps_middleware

# touch release_notes.md
# rm release_notes.md

# # download release notes:
# gh release download --pattern release_notes.md --repo bigfix/site_updates_linux_apps_middleware

rm -rf tmp
mkdir tmp
cd tmp

# download latest release source:
gh release download --archive=zip --repo bigfix/site_updates_linux_apps_middleware

# get newest zip file
# https://stackoverflow.com/a/5886002/861745
echo `ls -t *.zip | head -1`

# unzip ????.zip
unzip -o `ls -t *.zip | head -1`

# remove existing fixlets
rm ../Fixlets/Updates/*.bes

# copy files over
cp */Fixlets/Updates/*.bes ../Fixlets/Updates

cd ..

git add .
git commit -m "new updates `date +%Y%m%d`"
git push

# todo: increment tag
# git tag v14

# python3 .get-apps-release-notes.py > release_notes.md

# pre-commit

# add .

# git commit -m "new release notes `date +%Y%m%d`"

# git push

# gh pr create --title "New staged updates `date +%Y%m%d`" --fill --body-file release_notes.md --base main
