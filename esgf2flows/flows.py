import json
import hashlib

from settings import flows


class FlowsManager:

    def __init__(self, config, auth_manager):
        self.config = config
        self.auth_manager = auth_manager
        self.flows_client = self.auth_manager.get_flows_client()

        for flow_name, file_name in flows.items():
            f = open(file_name, "r")
            flow = json.load(f)
            definition = flow.get("definition")
            input_schema = flow.get("input_schema")
            new_checksum = hashlib.sha256(json.dumps(flow, sort_keys=True).encode()).hexdigest()
            config_checksum = self.config.get("flows", flow_name + "_checksum")
            if config_checksum:
                if config_checksum == new_checksum:
                    config_id = self.config.get("flows", flow_name + "_id")
                    print(f"Flow '{flow_name}' already has been registered: {config_id}")
                    continue
                print(f"Updating flow {flow_name}")
                flow_id = self.config.get("flows", flow_name + "_id")
                r = self.flows_client.update_flow(
                    flow_id=flow_id,
                    definition=definition,
                    input_schema=input_schema
                )
                self.config.set("flows", flow_name + "_checksum", new_checksum)
            else:
                print(f"Creating new flow {flow_name}")
                r = self.flows_client.create_flow(
                    title=flow_name,
                    definition=definition,
                    input_schema=input_schema
                )
                self.config.set("flows", flow_name + "_id", r.get("id"))
                self.config.set("flows", flow_name + "_checksum", new_checksum)
                self.config.set("flows", flow_name + "_scope", r.get("globus_auth_scope"))

    def get_flow_id(self, flow_name):
        return self.config.get("flows", flow_name + "_id")

    def run_flow(self, flow_name, body, label):
        flow_client = self.auth_manager.get_flow_client(flow_name)
        r = flow_client.run_flow(body=body, label=label)
        return r

    def list_runs(self, flow_name, query_params):
        flow_id = self.config.get("flows", flow_name + "_id")
        runs = []
        marker = None
        while True:
            r = self.flows_client.list_runs(
                    filter_flow_id=flow_id,
                    marker=marker,
                    query_params=query_params)
            runs.extend(r.get("runs"))
            if not r.get("has_next_page"):
                break
            marker = r.get("marker")

        return runs

    def cancel_run(self, run_id):
        return self.flows_client.cancel_run(run_id)
