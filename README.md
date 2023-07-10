# esgf2
ESGF2 Publication Flows

## ESG Publisher

The ESGF2 Flows use the ESG Publisher to extract metadata from climate files,
autocurate them and create metadata entries about datasets and files to publish
to the ESGF2 and/or ESGF index. It is assumed that the ESG Publisher is set up
on the data node.

Step-by-step instructions for setting up the ESG Publisher on a test Linux workstation can be found [here](docs/workstation.md).


## Globus Compute Endpoint

The ESGF2 Publication flows call Globus Compute functions on the data node to
run the ESGF Publisher. A Globus Compute Endpoint must be set up on the data
node. The documentation that describes the process is available at
https://funcx.readthedocs.io/en/latest/endpoints.html.

## Globus Flows

The ESGF2 Publication flows is a set of three flows:
 - Transfer and Publish - the flow transfers climate files to the data node to a correct directory that matches facets specified as the flow input, and runs the publication steps:
   - GenerateMapfile
   - RunAutocurator
   - MakePublicationRecords
   - GetPID
   - IndexPublish
 - Publish - the flow runs the publication steps on climate data that already have been transferred to the data node
 - Unpublish - the flow unpublishes a climate dataset/files

The flows and compute functions called in the flow are managed by the esgf2
Python module. The module is divided to several components:
 - LoginManager - a class that is responsible for logging into the Globus Auth to get access/refresh tokens needed to call Globus Services like Transfer, Compute, Flows, etc. that are needed to deploy compute functions, flows and run the flows. 
 - ComputeManager - a class that is responsible for registering functions run by the publication flows. The compute functions are defined in functions.py and listed in settings.py.
 - FlowsManager - a class responsible for registering publication flows and running them. The flows are defined in json files listed in settings.py
 - ConfigManager - a class that is responsible for storing access/refresh tokens, compute functions UUIDs, flows UUIDs, scopes, etc.

## Globus Index

The flows interact with the Globus Search service to publish/unpublish
metadata. A Globus index UUID must be specified in settings.py and is hardcoded
into the compute functions body when the functions are registered.

