#!/usr/bin/env python

import os
import sys
import glob
import hashlib
import uuid
import json


def sha256sum(path):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(path, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def generate_mapfile(dataset_id, dataset_path, mapfile_path):

    map_list = []

    for nc_file in glob.glob(dataset_path + "/*.nc"):
        stats = os.stat(nc_file)
        mod_time = int(stats.st_mtime)
        checksum = sha256sum(nc_file)
        nc_file_map = [
            dataset_id,
            nc_file,
            f"{stats.st_size}",
            f"mod_time={mod_time}.0",
            f"checksum={checksum}",
            "checksum_type=SHA256"
        ]
        map_list.append(nc_file_map)

    publication_dir = os.path.dirname(mapfile_path)
    os.makedirs(publication_dir, exist_ok=True)

    with open(mapfile_path, "w") as f:
        json.dump(map_list, f)
        print("", file=f)


if __name__ == "__main__":

    dataset_id = "#".join(sys.argv[1].rsplit("/v", 1)).replace("/", ".")
    dataset_path = "/home/lukasz/globus-shared-files/css03_data/" + sys.argv[1]
    mapfile_path = sys.argv[2]

    generate_mapfile(dataset_id, dataset_path, mapfile_path)
