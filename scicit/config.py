import json
import os
from google.cloud import bigquery as bq
from google.oauth2 import service_account


class Config:
    def __init__(self, credentials=None, project_id=None, dataset_id=None):
        self.config_dict = json.load(open("config.json", "rb"))
        self.credentials = (
            credentials if credentials else self.config_dict["credentials"]
        )
        self.project_id = (
            project_id if project_id else self.config_dict["project_id"]
        )
        self.dataset_id = (
            dataset_id if dataset_id else self.config_dict["dataset_id"]
        )

    def credentials(self):
        assert os.path.isfile(self.credentials)
        return service_account.Credentials.from_service_account_file(
            self.credentials,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    def client(self):
        """
        :return: bq.Client
        """
        return bq.Client(
            project=self.project_id, credentials=self.credentials()
        )

    def table_ref(self, table_id, client=None):
        """
        :param client: bq.Client or None, if None, populated with config.json attr
        :param table_id: str
        :return: table_ref
        """
        if not client:
            client = self.client()
        return client.dataset(dataset_id=self.dataset_id).table(
            table_id=table_id
        )
