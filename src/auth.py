from globus_sdk import TransferClient, FlowsClient, SpecificFlowClient, NativeAppAuthClient, AuthClient, RefreshTokenAuthorizer
from globus_sdk.scopes.data import AuthScopes, TransferScopes, FlowsScopes
from globus_compute_sdk import Client as ComputeClient

from settings import settings, flows


class AuthManager:
    scopes = [
        AuthScopes.openid,
        AuthScopes.view_identities,
        AuthScopes.view_identity_set,
        TransferScopes.all,
        FlowsScopes.manage_flows,
        FlowsScopes.view_flows,
        FlowsScopes.run,
        FlowsScopes.run_status,
        FlowsScopes.run_manage,
        ComputeClient.FUNCX_SCOPE,
    ]

    def __init__(self, config):
        self.config = config
        self.native_client = NativeAppAuthClient(settings.get("client_id"))
        self.services = [
            "auth.globus.org",
            "transfer.api.globus.org",
            "flows.globus.org",
            "funcx_service"
        ]

        self.authorizer = {}
        self.client = {}

        for f in flows:
            flow_id = self.config.get("flows", f + "_id")
            if flow_id:
                self.services.append(flow_id)
                flow_scope = self.config.get("flows", f + "_scope")
                AuthManager.scopes.append(flow_scope)

        self.set_up_services(AuthManager.scopes, self.services)

    def set_up_services(self, scopes, services):

        for service in services:
            access_token = self.get_token(service, "access_token")
            if not access_token:
                self.run_login_flow(scopes)
                access_token = self.get_token(service, "access_token")
            refresh_token = self.get_token(service, "refresh_token")
            expires_at = self.get_token(service, "expires_at")
            self.authorizer[service] = RefreshTokenAuthorizer(
                refresh_token,
                self.native_client,
                access_token=access_token,
                expires_at=int(expires_at),
                on_refresh=self.on_refresh
            )
            if service == "auth.globus.org":
                self.client[service] = AuthClient(authorizer=self.authorizer.get(service))
            elif service == "transfer.api.globus.org":
                self.client[service] = TransferClient(authorizer=self.authorizer.get(service))
            elif service == "flows.globus.org":
                self.client[service] = FlowsClient(authorizer=self.authorizer.get(service))
            elif service == "funcx_service":
                self.client[service] = ComputeClient(
                    openid_authorizer=self.authorizer.get("auth.globus.org"),
                    fx_authorizer=self.authorizer.get(service)
                )
            else:
                self.client[service] = SpecificFlowClient(
                    flow_id=service,
                    authorizer=self.authorizer.get(service)
                )

    def run_login_flow(self, scopes):
        self.native_client.oauth2_start_flow(requested_scopes=scopes, refresh_tokens=True)
        authorize_url = self.native_client.oauth2_get_authorize_url()
        print("Please go to this URL and login: {0}".format(authorize_url))

        auth_code = input("Please enter the code you get after login here: ").strip()
        token_response = self.native_client.oauth2_exchange_code_for_tokens(auth_code)
        by_rs = token_response.by_resource_server
        for service in self.services:
            tokens = by_rs.get(service)
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            expires_at = tokens.get("expires_at_seconds")
            self.save_tokens(service, access_token, refresh_token, expires_at)

    def get_token(self, service, token):
        return self.config.get("tokens", service + "__" + token)

    def save_tokens(self, service, access_token, refresh_token, expires_at):
        self.config.set("tokens", service + "__access_token", access_token)
        self.config.set("tokens", service + "__refresh_token", refresh_token)
        self.config.set("tokens", service + "__expires_at", str(expires_at))

    def on_refresh(self, token_response):
        for service, tokens in token_response.by_resource_server.items():
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            expires_at = tokens.get("expires_at_seconds")
            self.save_tokens(service, access_token, refresh_token, expires_at)

    def get_client(self, service):
        return self.client.get(service)

    def get_auth_client(self):
        return self.get_client("auth.globus.org")

    def get_transfer_client(self):
        return self.get_client("transfer.api.globus.org")

    def get_compute_client(self):
        return self.get_client("funcx_service")

    def get_flows_client(self):
        return self.get_client("flows.globus.org")

    def get_flow_client(self, flow_name):
        flow_id = self.config.get("flows", flow_name + "_id")
        flow_client = self.client.get(flow_id)
        if flow_client:
            return flow_client
        flow_scope = self.config.get("flows", flow_name + "_scope")
        self.set_up_services([flow_scope], flow_id)
        return self.client.get(flow_id)
