from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadFactOperator(BaseOperator):
    """
    Loads data into a fact table in Redshift.
    Always runs in append mode (no truncate).
    """

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_query="",
                 table="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.table = table

    def execute(self, context):
        self.log.info(f"Loading fact table {self.table}")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        insert_sql = f"INSERT INTO {self.table} {self.sql_query}"
        self.log.info(f"Executing SQL: {insert_sql}")
        redshift.run(insert_sql)
