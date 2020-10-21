#!/bin/sh
COLUMN=$2
NAME=$(echo $1| cut -d'_' -f 3 | cut -d'.' -f 1)
cut -f $COLUMN $1 | sort -u -o "${NAME}_col${COLUMN}.txt"