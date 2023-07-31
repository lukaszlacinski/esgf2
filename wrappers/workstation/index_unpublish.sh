#!/bin/bash

/home/lukasz/miniconda3/envs/esgf-pub/bin/esgunpublish --dset-id $1 --no-auth >> /tmp/esgf2_log.txt
/opt/esgf2/venv/bin/globus search delete-by-query -q "{\"filters\":[{\"type\":\"match_all\",\"field_name\":\"dataset_id\",\"values\":[\"$1\"]}]}" 4936364c-f366-4436-8fc5-99b4beafb3c9
