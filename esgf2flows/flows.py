import json
import hashlib

from settings import flows


class FlowsManager:

    def __init__(self, config, auth_manager):
        self.config = config
        self.auth_manager = auth_manager
        self.flows_client = self.auth_manager.get_flows_client()

        print(flows.items())
        for flow_name, file_name in flows.items():
            f = open(file_name, "r")
            flow = json.load(f)
            definition = flow.get("definition")
            input_schema = flow.get("input_schema")
            new_checksum = hashlib.sha256(json.dumps(flow, sort_keys=True).encode()).hexdigest()
            config_checksum = self.config.get("flows", flow_name + "_checksum")
            print(new_checksum, config_checksum)
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
            print(r)

    def run_flow(self, flow_name, body, label):
        flow_client = self.auth_manager.get_flow_client(flow_name)
        r = flow_client.run_flow(body=body, label=label)
        print(r)
