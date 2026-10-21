#!/bin/bash

SH_FILES=$( find -name "*.sh" -mtime -1 )
PY_FILES=$( find -name "*.py" -mtime -1 )

BASH_COUNT=$( find -name "*.sh" -mtime -1 | wc -l )
PY_COUNT=$( find -name "*.py" -mtime -1 | wc -l )

if [[ $BASH_COUNT -gt 0 ]] ; then
    for SH_FILE in $SH_FILES
    do
        cp -v $SH_FILE ~/backups
    done
fi

if [[ $PY_COUNT -gt 0 ]] ; then
    for PY_FILE in $PY_FILES
    do
        cp -v $PY_FILE ~/backups
    done
fi

rclone copy ~/backups Mydrive:projects

cd ~/backups
FILES=$(ls -v)
for file in $FILES
do
    cp -v $file  ~/projects
done

cd

cd ~/projects
git pull origin main
if [[ -n $( git status -s ) ]] ; then
    git add -A
    git commit -m "Automated commit"
    git push origin main
fi

cd
