#!/bin/sh
cut -f 4,5 data/dataset_TIST2015_Cities.txt | sort -u -k1 -o data/dataset_TIST2015_Countries.txt