import click
from google.cloud import bigquery as bq
from wasabi import Printer

from scicit.config import Config
from scicit.utils import str_to_bq_ref


@click.command(
    help="python bin/CreateBQTable --uri 'gs://npl-parsing/serialized_tls214/*.jsonl' "
    "--table_id 'npl-parsing.patcit.beta' --schema 'schema/npl_citation_schema.md' "
    "--write_mode 'CREATE_NEW'"
)
@click.option(
    "--uri", help="E.g. 'gs://npl-parsing/serialized_tls214/*.jsonl'"
)
@click.option(
    "--table_path",
    help="BQ path of the target table (e.g 'npl-parsing.patcit.beta').",
)
@click.option("--schema", help="json file defining the table schema")
@click.option(
    "--write_mode",
    default="CREATE_NEW",
    help="'CREATE_NEW' to create a new table, "
    "disregarding pre-existence; "
    "'WRITE_APPEND' to append data to the "
    "pre-existing table (if any)",
)
def main(uri, table_path, schema, write_mode):
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
    load_job_config.max_bad_records = 10

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

    load_job = client.load_table_from_uri(
        uri, table_ref, job_config=load_job_config
    )
    with msg.loading("Loading data..."):
        load_job.result()
    msg.good("Data succesfully loaded!")


if __name__ == "__main__":
    main()
