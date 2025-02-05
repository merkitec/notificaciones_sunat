import json
import requests

class EstudioContableService():
    def __init__(self, config=None):
        self.config = config

    def get_rucs_by_estudio_contable(self, numero_ruc):
        # Call the endpoint and get the response
        response = self.__call_get_estudios_contables_by_ruc_endpoint(numero_ruc)

        # Return the list of RUCs
        return [{"RUC": r['numero_ruc'], 
                 "USER":r['usuario_buzon'], 
                 "PSW": r['password_buzon']} for r in response['rucs']]

    def __call_get_estudios_contables_by_ruc_endpoint(self, numero_ruc):
        # Construct the endpoint URL
        base_url = self.config["URLS"]["persist_base_url"]
        url = f"{base_url.rstrip('/')}/estudios_contables/ruc/{numero_ruc}"

        # Send the GET request
        response = requests.get(url)

        # Raise an exception for HTTP error responses
        response.raise_for_status()

        # Return the response as JSON
        return json.loads(response.text)
