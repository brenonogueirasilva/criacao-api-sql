from google.cloud import secretmanager_v1
import os
import json

class SecretManager:
    """
    Class for interacting with Google Cloud Secret Manager.
    """
    def __init__(self):
        self.client = secretmanager_v1.SecretManagerServiceClient()

    def access_secret_value(self, project_id: str, secret_name: str, version_id: str = 'latest') -> str:
        """
        Accesses and retrieves the value of a secret.
        Args:
            project_id (str): The Google Cloud project ID.
            secret_name (str): The name of the secret.
            version_id (str, optional): The version of the secret. Defaults to 'latest'.
        Returns:
            str: The value of the secret.
        """
        name = f"projects/{project_id}/secrets/{secret_name}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def access_secret_json_file(self,  project_id: str, secret_name: str, version_id: str = 'latest') -> dict:
        """
        Retrieves the JSON-formatted content of a secret and converts it to a dictionary.
        Args:
            project_id (str): The Google Cloud project ID.
            secret_name (str): The name of the secret.
            version_id (str, optional): The version ID of the secret. Defaults to 'latest'.

        Returns:
            dict: The content of the secret in dictionary format.
        """
        response = self.access_secret_value(project_id, secret_name, version_id=version_id)
        dict_format = json.loads(response)
        return dict_format