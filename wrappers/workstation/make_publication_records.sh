#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgmkpubrec --scan-file $2 --map-data $1 --out-file $3 --set-replica
