#!/bin/bash

echo "checking for new files to backup..."
echo
sleep 2

SH_FILES=$( find -name "*.sh" -mtime -1 )
PY_FILES=$( find -name "*.py" -mtime -1 )

BASH_COUNT=$( find -name "*.sh" -mtime -1 | wc -l )
PY_COUNT=$( find -name "*.py" -mtime -1 | wc -l )

if [[ $BASH_COUNT -gt 0 ]]; then
    for SH_FILE in $SH_FILES
    do
        cp $SH_FILE ~/backups
        cp $SH_FILE ~/projects
    done
fi

if [[ $PY_COUNT -gt 0 ]]; then
    for PY_FILE in $PY_FILES
    do
        cp $PY_FILE ~/backups
        cp $PY_FILE ~/projects
    done
fi

rclone copy backups Mydrive:projects

cd projects
git add -A
git commit
#git push 
