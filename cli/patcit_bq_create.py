import typer
from google.cloud import bigquery as bq
from wasabi import Printer

from patcit.config import Config
from patcit.utils import str_to_bq_ref

app = typer.Typer()


@app.command()
def from_gs(uri: str, table_path: str, schema: str, write_mode: str = "CREATE_NEW"):
    """
    Load data from Google Storage to Big Query

    Notes:
        --write-mode: 'CREATE_NEW' or 'WRITE_APPEND'

    E.g. python cli/patcit_bq.py create from-gs 'gs://npl-parsing/serialized_tls214/*.jsonl'
    'npl-parsing.patcit.npl_v00' 'schema/npl_citation_schema.json'
    """

    msg = Printer()
    project_id, dataset_id, _ = table_path.split(".")
    config = Config(project_id=project_id, dataset_id=dataset_id)
    client = config.client()
    table_ref = str_to_bq_ref(table_path)

    load_job_config = bq.LoadJobConfig()
    load_job_config.schema = client.schema_from_json(schema)
    load_job_config.source_format = bq.SourceFormat.NEWLINE_DELIMITED_JSON
    load_job_config.ignore_unknown_values = True
    load_job_config.write_disposition = "WRITE_APPEND"
    load_job_config.max_bad_records = 100

    assert write_mode in ["CREATE_NEW", "WRITE_APPEND"]
    table_id = table_path.split(".")[-1]
    exists = any(
        [
            table_id == table.table_id
            for table in client.list_tables(client.dataset(dataset_id))
        ]
    )

    if exists and write_mode == "CREATE_NEW":
        msg.info(f"{table_path} already exists. Write_mode: {write_mode}")
        client.delete_table(table_ref)
        table = bq.Table(table_ref, schema=client.schema_from_json(schema))
        client.create_table(table)

    load_job = client.load_table_from_uri(uri, table_ref, job_config=load_job_config)
    with msg.loading("Loading data..."):
        load_job.result()
    msg.good("Data succesfully loaded!")


if __name__ == "__main__":
    app()
