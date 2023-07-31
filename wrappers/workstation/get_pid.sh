#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgpidcitepub --pub-rec $1 --out-file $2

/opt/esgf2/wrappers/get_pid.py $2 $3
