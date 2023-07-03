#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgunpublish --dset-id $1 --no-auth >> /tmp/esgf2_log.txt
