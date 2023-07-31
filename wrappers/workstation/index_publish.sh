#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgindexpub --pub-rec $1 --no-auth >> /tmp/esgf2_log.txt

# ESGF2 prod index
# globus_index_id="d927e2d9-ccdb-48e4-b05d-adbc3d97bbc5"

# ESGF2 test index
globus_index_id="4936364c-f366-4436-8fc5-99b4beafb3c9"

/opt/esgf2/venv/bin/globus search ingest $globus_index_id $2
