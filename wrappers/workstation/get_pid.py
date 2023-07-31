#!/usr/bin/env python

import sys
import json
from datetime import datetime


non_list = [
    "creation_date",
    "title",
    "data_node",
    "index_node",
    "master_id",
    "instance_id",
    "id",
    "replica",
    "latest",
    "type",
    "version",
    "north_degrees",
    "south_degrees",
    "east_degrees",
    "west_degrees",
    "datetime_start",
    "datetime_end",
    "number_of_files",
    "size",
    "timestamp",
]


def get_gmeta_entry(doc, now):
    for key, value in doc.items():
        if isinstance(value, list):
            continue
        if key in non_list:
            continue
        doc[key] = [value]

    doc["retracted"] = False
    doc["_timestamp"] = now

    gmeta_entry = {
        "id": "dataset" if doc.get("type") == "Dataset" else "file",
        "subject": doc.get("id"),
        "visible_to": ["public"],
        "content": doc
    }

    return gmeta_entry


def convert2esgf2(pid_esgf1):
    gmeta = []
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Transform an ESGF1 dataset entries to an ESGF2 Globus index entry
    for doc in pid_esgf1:
        gmeta_entry = get_gmeta_entry(doc, now)
        gmeta.append(gmeta_entry)

    # Create a GMetaList with a GMetaEntry for the dataset and GMetaEntries for files
    gingest = {
        "ingest_type": "GMetaList",
        "ingest_data": {
            "gmeta": gmeta
        }
    }

    return gingest


if __name__ == "__main__":
    pid_esgf1 = sys.argv[1]
    pid_esgf2 = sys.argv[2]

    with open(pid_esgf1, "r") as f1:
        d1 = json.load(f1)
        d2 = convert2esgf2(d1)
        with open(pid_esgf2, "w") as f2:
            print(json.dumps(d2), file=f2)
