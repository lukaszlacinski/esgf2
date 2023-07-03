#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgmkpubrec --map-data $1 --scan-file $2 --out-file $3 --set-replica
