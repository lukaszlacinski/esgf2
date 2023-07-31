#!/usr/bin/env python

import sys
import subprocess


# ESGF2 prod index
# globus_index_id = "d927e2d9-ccdb-48e4-b05d-adbc3d97bbc5"

# ESGF2 test index
globus_index_id = "4936364c-f366-4436-8fc5-99b4beafb3c9"

def ingest(path):
    cp = subprocess.run(["/opt/esgf2/venv/bin/globus",
            "search", "ingest", globus_index_id, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return not cp.returncode


if __name__ == "__main__":
    pid_esgf2 = sys.argv[1]
    if not ingest(pid_esgf2):
        sys.exit(1)
