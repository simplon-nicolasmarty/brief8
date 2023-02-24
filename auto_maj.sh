#!/usr/bin/env bash
# coding: utf-8
# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4

set -e

PATCH=$(ag --nonumbers '^ver =' azure-vote/main.py | sed -re 's/ver = "1\.0\.([0-9]+)"/\1/')

while true; do
    PATCH=$((PATCH+1))
    sed -i -re "s/(ver = \"1\.0\.).(.*)$/\1${PATCH}\2/" azure-vote/main.py
    git commit -a -m "new vers" && git push
done

exit 0
