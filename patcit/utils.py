from patcit.config import Config


def str_to_bq_ref(s):
    """
    Return a bq.TableRef from a string like path (e.g npl-parsing.patcit.raw)
    :param s: str
    :return: bq.Tableref
    """
    project_id, dataset_id, table_id = s.split(".")
    config = Config(project_id=project_id, dataset_id=dataset_id)
    return config.table_ref(table_id)


def ref_to_bq_path(ref):
    """
    Return a string like path from a bq.TableRef object
    :param ref: bq.Tableref
    :return: str
    """
    return ".".join(ref._key())
