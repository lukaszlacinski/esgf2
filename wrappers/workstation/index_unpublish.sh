#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgunpublish --dset-id $1 --no-auth >> /tmp/esgf2_log.txt

# ESGF2 prod index
# globus_index_id="d927e2d9-ccdb-48e4-b05d-adbc3d97bbc5"

# ESGF2 test index
globus_index_id="4936364c-f366-4436-8fc5-99b4beafb3c9"

/opt/esgf2/venv/bin/globus search delete-by-query -q "{\"filters\":[{\"type\":\"match_all\",\"field_name\":\"dataset_id\",\"values\":[\"$1\"]}]}" $globus_index_id
