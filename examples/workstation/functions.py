

def generate_mapfile(path):
    import os
    import sys
    import uuid
    import subprocess
    tmp_basedir = "/tmp/esgf2"
    wrappers_basedir = "/opt/esgf2/wrappers"
    publication_uuid = str(uuid.uuid4())
    mapfile = os.path.join(f"{tmp_basedir}", publication_uuid, "mapfile.json")
    wrapper = os.path.join(f"{wrappers_basedir}", "generate_mapfile.sh")
    cp = subprocess.run([wrapper, path, mapfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)
    return publication_uuid


def run_autocurator(path, publication_uuid):
    import os
    import sys
    import subprocess
    tmp_basedir = "/tmp/esgf2"
    wrappers_basedir = "/opt/esgf2/wrappers"
    scanfile = os.path.join(f"{tmp_basedir}", publication_uuid, "scanfile.json")
    wrapper = os.path.join(f"{wrappers_basedir}", "run_autocurator.sh")
    cp = subprocess.run([wrapper, path, scanfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def make_publication_records(publication_uuid):
    import os
    import sys
    import subprocess
    tmp_basedir = "/tmp/esgf2"
    wrappers_basedir = "/opt/esgf2/wrappers"
    mapfile = os.path.join(f"{tmp_basedir}", publication_uuid, "mapfile.json")
    scanfile = os.path.join(f"{tmp_basedir}", publication_uuid, "scanfile.json")
    pubrecfile = os.path.join(f"{tmp_basedir}", publication_uuid, "pubrec.json")
    wrapper = os.path.join(f"{wrappers_basedir}", "make_publication_records.sh")
    cp = subprocess.run([wrapper, mapfile, scanfile, pubrecfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def get_pid(publication_uuid):
    import os
    import sys
    import subprocess
    tmp_basedir = "/tmp/esgf2"
    wrappers_basedir = "/opt/esgf2/wrappers"
    pubrecfile = os.path.join(f"{tmp_basedir}", publication_uuid, "pubrec.json")
    pidfile1 = os.path.join(f"{tmp_basedir}", publication_uuid, "pid_esgf1.json")
    pidfile2 = os.path.join(f"{tmp_basedir}", publication_uuid, "pid_esgf2.json")
    wrapper = os.path.join(f"{wrappers_basedir}", "get_pid.sh")
    cp = subprocess.run([wrapper, pubrecfile, pidfile1, pidfile2],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def index_publish(publication_uuid):
    import os
    import sys
    import subprocess
    tmp_basedir = "/tmp/esgf2"
    wrappers_basedir = "/opt/esgf2/wrappers"
    pidfile1 = os.path.join(f"{tmp_basedir}", publication_uuid, "pid_esgf1.json")
    pidfile2 = os.path.join(f"{tmp_basedir}", publication_uuid, "pid_esgf2.json")
    wrapper = os.path.join(f"{wrappers_basedir}", "index_publish.sh")
    cp = subprocess.run([wrapper, pidfile1, pidfile2],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def index_unpublish(dataset_id):
    import os
    import sys
    import subprocess
    tmp_basedir = "/tmp/esgf2"
    wrappers_basedir = "/opt/esgf2/wrappers"
    wrapper = os.path.join(f"{wrappers_basedir}", "index_unpublish.sh")
    cp = subprocess.run([wrapper, dataset_id],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)
