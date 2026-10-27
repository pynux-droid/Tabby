#!/bin/bash

set -eop

echo "initiallizing..."
echo
apt-get update  -yy
echo

echo "upgrading..."
echo
apt full-upgrade -yy
echo

echo "Finished updating packages!"
exit
