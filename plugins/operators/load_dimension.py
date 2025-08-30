from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):
    """
    Loads data into a dimension table in Redshift.
    Supports truncate-insert or append-only.
    """

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_query="",
                 table="",
                 append_only=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.table = table
        self.append_only = append_only

    def execute(self, context):
        self.log.info(f"Loading dimension table {self.table}")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if not self.append_only:
            self.log.info(f"Clearing data from {self.table}")
            redshift.run(f"TRUNCATE TABLE {self.table}")

        insert_sql = f"INSERT INTO {self.table} {self.sql_query}"
        self.log.info(f"Executing SQL: {insert_sql}")
        redshift.run(insert_sql)
