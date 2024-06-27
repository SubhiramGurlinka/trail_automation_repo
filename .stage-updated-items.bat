git pull
REM stage modified items to git index
git add --update

REM remove "new" files during automated builds
REM new items must be added manually
git clean -f

REM revert items that do not have version changes in title
REM updates to existing versions must be added manually
pre-commit run revert-missing-change --hook-stage manual

git add --update

pre-commit run search-and-replace

git add --update

pre-commit run trailing-whitespace

git add --update

@REM pre-commit run minimum-changes --hook-stage manual



pre-commit

REM git commit -m "new updated content"
git push
