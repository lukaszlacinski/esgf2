# ESG Publisher on Linux Workstation

The ESG Publisher is documented at https://esg-publisher.readthedocs.io/en/v5.1.0b13/index.html. This page describes the process of setting up the ESG Publisher on a Linux workstation.

Download and install Miniconda, https://conda.io/projects/conda/en/latest/user-guide/install/linux.html:
```
bash Miniconda3-latest-Linux-x86_64.sh
yes
yes
```
Turn off conda autoactivation:
```
~/miniconda3/bin/conda config --set auto_activate_base false
```
and restart the shell. Follow the esg-publisher installation instructions:
```
conda create -n esgf-pub -c conda-forge -c esgf-forge pip libnetcdf cmor autocurator esgconfigparser
Y
conda activate esgf-pub
pip install esgfpid
pip install esgcet==5.1.0b13
```
Download CMOR tables. In our case, we will keep the ESGF related config files and scripts in `/opt/esgf2`.
```
mkdir /opt/esgf2
cd /opt/esgf2
git clone https://github.com/PCMDI/cmip6-cmor-tables.git
```
Create a config file (~/.esg/esg.ini). In our case, CMIP6 climate files will be 
```
[DEFAULT]
data_node = test.esgf-data.anl.gov
index_node = esgf-fedtest.llnl.gov
cmor_path = /opt/esgf2/cmip6-cmor-tables/Tables
data_roots = {"/opt/esgf2/data/css03_data": "css03_data"}
cert = ~/.globus/certificate-file
[user]
pid_creds = [{"url": "207.38.94.86", "port": "32272", "vhost": "esgf-pid", "user": "esgf-publisher", "password": "<secret>", "ssl_enabled": true, "priority": 1}, {"url": "handle-esgf-trusted.dkrz.de", "port": "5671", "vhost": "esgf-pid", "user": "esgf-publisher", "password": "<secret>", "ssl_enabled": true, "priority": 2}, {"url": "pcmdi10.llnl.gov", "port": "5671", "vhost": "esgf-pid", "user": "esgf-publisher", "password": "<secret>", "ssl_enabled": true, "priority": 3}]
globus_uuid = "8896f38e-68d1-4708-bce4-b1b3a3405809"
user_project_config = {"cmip6": {"DRS": ["mip_era", "activity_drs", "institution_id", "source_id", "experiment_id", "member_id", "table_id", "variable_id", "grid_label"], "CONST_ATTR": {"project": "CMIP6"}}}
data_transfer_node  = g-52ba3.fd635.8443.data.globus.org
```
To get PIDs, you will need to set `pid_creds` to real credentials.

To get URLs correctly set in publication records, you will also need to change `URL_Templates` in `~/miniconda3/envs/esgf-pub/lib/python3.<N>/site-packages/esgcet/sttings.py` to:
```
URL_Templates = [
    "https://{}/{}/{}|application/netcdf|HTTPServer",
    "globus:{}/{}/{}|Globus|Globus"
]
```
