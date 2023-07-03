#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/autocurator --out_pretty --files "/opt/esgf2/data/css03_data/$1/*.nc" --out_json $2
