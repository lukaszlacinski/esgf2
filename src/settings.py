"""
dashboard.globus.org
    "globus_endpoint_id": "3ec77f8a-bcfd-11ed-b206-d150fa9edad1",
    "destination_path_prefix": "/~/globus-shared-files/css03_data",
    "compute_endpoint_id": "b360aacf-6c02-418c-97da-56a8468b8db2",
z440
    "globus_endpoint_id": "a2b8733a-172c-11ee-aa61-63e0d97254cd",
    "destination_path_prefix": "/opt/esgf2/data/css03_data",
    "compute_endpoint_id": "37381592-7429-463e-967b-dc3b705d618a",
"""

settings = {
    "client_id": "2cd4a09d-8d85-4e65-9f20-1b83bd73ba7e",
    "globus_endpoint_id": "a2b8733a-172c-11ee-aa61-63e0d97254cd",
    "destination_path_prefix": "/opt/esgf2/data/css03_data",
    "compute_endpoint_id": "37381592-7429-463e-967b-dc3b705d618a",
}

compute_functions = [
    "generate_mapfile",
    "run_autocurator",
    "make_publication_records",
    "index_publish",
    "get_pid",
    "index_unpublish",
]

flows = {
    "transfer_and_publish": "transfer_and_publish.json",
    "publish": "publish.json",
    "unpublish": "unpublish.json",
}
