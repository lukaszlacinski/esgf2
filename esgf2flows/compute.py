import hashlib
import dill
from globus_compute_sdk.serialize import ComputeSerializer
from settings import compute_functions
import functions


class ComputeManager:

    def __init__(self, config, auth_manager):
        self.config = config
        self.auth_manager = auth_manager
        self.compute_client = self.auth_manager.get_compute_client()

        compute_serializer = ComputeSerializer()
        for function_name in compute_functions:
            function = getattr(functions, function_name)
            serialized_function = compute_serializer.serialize(function)
            new_checksum = hashlib.sha256(serialized_function.encode()).hexdigest()
            config_checksum = self.config.get("functions", function_name + "_checksum")
            if config_checksum and config_checksum == new_checksum:
                config_id = self.config.get("functions", function_name + "_id")
                print(f"Function '{function_name}' already has been registered: {config_id}")
                continue
            print(f"Registering new/updated compute function '{function_name}'")
            uuid = self.compute_client.register_function(function, function_name)
            self.config.set("functions", function_name + "_id", uuid)
            self.config.set("functions", function_name + "_checksum", new_checksum)

    def get_endpoint_status(self, compute_endpoint_id):
        return self.compute_client.get_endpoint_status(compute_endpoint_id)

    def get_endpoint_metadata(self, compute_endpoint_id):
        return self.compute_client.get_endpoint_metadata(compute_endpoint_id)
