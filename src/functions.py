def generate_mapfile(path):
    import sys
    import uuid
    import subprocess
    publication_uuid = str(uuid.uuid4())
    mapfile = "/tmp/esgf2/" + publication_uuid + ".json"
    cp = subprocess.run(["/opt/esgf2/generate_mapfile.sh", path, mapfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)
    return publication_uuid


def run_autocurator(publication_uuid):
    import sys
    import subprocess
    mapfile = "/tmp/esgf2/" + publication_uuid + "_mapfile.json"
    scanfile = "/tmp/esgf2/" + publication_uuid + "_scanfile.json"
    cp = subprocess.run(["/opt/esgf2/run_autocurator.sh", mapfile, scanfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def make_publication_records(publication_uuid):
    import sys
    import subprocess
    mapfile = "/tmp/esgf2/" + publication_uuid + "_mapfile.json"
    scanfile = "/tmp/esgf2/" + publication_uuid + "_scanfile.json"
    pubrecfile = "/tmp/esgf2/" + publication_uuid + "_pubrec.json"
    cp = subprocess.run(["/opt/esgf2/make_publication_records.sh", mapfile, scanfile, pubrecfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def get_pid(publication_uuid):
    import sys
    import subprocess
    pubrecfile = "/tmp/esgf2/" + publication_uuid + "_pubrec.json"
    pidfile = "/tmp/esgf2/" + publication_uuid + "_pid.json"
    cp = subprocess.run(["/opt/esgf2/get_pid.sh", pubrecfile, pidfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def index_publish(publication_uuid):
    import sys
    import subprocess
    pidfile = "/tmp/esgf2/" + publication_uuid + "_pid.json"
    cp = subprocess.run(["/opt/esgf2/index_publish.sh", pidfile],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)


def index_unpublish(dataset_id):
    import sys
    import subprocess
    cp = subprocess.run(["/opt/esgf2/index_unpublish.sh", dataset_id],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    if cp.returncode:
        sys.exit(1)
