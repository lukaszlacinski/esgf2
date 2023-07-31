#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgindexpub --pub-rec $1 --no-auth >> /tmp/esgf2_log.txt

/opt/esgf2/wrappers/index_publish.py $2
