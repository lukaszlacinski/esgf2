#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/autocurator --out_pretty --files "/home/lukasz/globus-shared-files/css03_data/$1/*.nc" --out_json $2
