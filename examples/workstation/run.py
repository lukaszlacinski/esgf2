import os
from esgf2flows import Config, AuthManager, ComputeManager, FlowsManager
from settings import data_node


if __name__ == "__main__":
    # load or create an empty ~/.esgf2workstation.ini
    config_path = os.path.expanduser("~/.esgf2workstation.ini")
    config = Config(config_path)

    # set up authorizers and Globus clients
    am = AuthManager(config)
    auth_client = am.get_auth_client()
    user_info = auth_client.oauth2_userinfo()
    print("User Info:\n", user_info)

    # register ESGF compute functions that are defined in functions.py and called by ESGF2 Flows
    cm = ComputeManager(config, am)

    # check the compute endpoint specified in settings.py
    endpoint_info = cm.get_endpoint_status(data_node.get("compute_endpoint_id"))
    print("Endpoint Info:\n", endpoint_info)

    # instantiate a Flows Manager, create/update flows listed in settings.py and defined in json files
    fm = FlowsManager(config, am)
    # run a flow

    transfer_and_publish_body = {
        "source": {
            "id": "8896f38e-68d1-4708-bce4-b1b3a3405809",
            "path": "/flows/CMIP6/AerChemMIP/EC-Earth-Consortium/EC-Earth3-AerChem/hist-piAer/r1i1p1f1/AERday/maxpblz/gn"
        },
        "destination": {
            "id": data_node.get("globus_endpoint_id")
        },
        "destination_path_prefix": data_node.get("destination_path_prefix"),
        "facets": {
            "project": "CMIP6",
            "activity_drs": "AerChemMIP",
            "institution_id": "EC-Earth-Consortium",
            "dource_id": "EC-Earth3-AerChem",
            "experiment_id": "hist-piAer",
            "member_id": "r1i1p1f1",
            "table_id": "AERday",
            "variable_id": "maxpblz",
            "grid_label": "gn",
            "version": "20201006"
        },
        "compute_endpoint_id": data_node.get("compute_endpoint_id"),
        "generate_mapfile_id": config.get("functions", "generate_mapfile_id"),
        "run_autocurator_id": config.get("functions", "run_autocurator_id"),
        "get_pid_id": config.get("functions", "get_pid_id"),
        "make_publication_records_id": config.get("functions", "make_publication_records_id"),
        "index_publish_id": config.get("functions", "index_publish_id")
    }

    publish_body = {
        "facets": {
            "project": "CMIP6",
            "activity_drs": "AerChemMIP",
            "institution_id": "EC-Earth-Consortium",
            "dource_id": "EC-Earth3-AerChem",
            "experiment_id": "hist-piAer",
            "member_id": "r1i1p1f1",
            "table_id": "AERday",
            "variable_id": "maxpblz",
            "grid_label": "gn",
            "version": "20201006"
        },
        "compute_endpoint_id": data_node.get("compute_endpoint_id"),
        "generate_mapfile_id": config.get("functions", "generate_mapfile_id"),
        "run_autocurator_id": config.get("functions", "run_autocurator_id"),
        "get_pid_id": config.get("functions", "get_pid_id"),
        "make_publication_records_id": config.get("functions", "make_publication_records_id"),
        "index_publish_id": config.get("functions", "index_publish_id")
    }

    unpublish_body = {
        "dataset_id": "CMIP6.AerChemMIP.EC-Earth-Consortium.EC-Earth3-AerChem.hist-piAer.r1i1p1f1.AERday.maxpblz.gn.v20201006|eagle.alcf.anl.gov",
        "compute_endpoint_id": data_node.get("compute_endpoint_id"),
        "index_unpublish_id": config.get("functions", "index_unpublish_id")
    }
    print("Run Transfer and Publish flow")
    fm.run_flow("transfer_and_publish", body=transfer_and_publish_body, label="test1")
    #fm.run_flow("publish", body=publish_body, label="test2")
    #fm.run_flow("unpublish", body=unpublish_body, label="test3")
