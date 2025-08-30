from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):
    """
    Runs data quality checks against Redshift.
    Accepts a list of tests in the format:
    [{'check_sql': ..., 'expected_result': ...}, ...]
    """

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tests=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tests = tests

    def execute(self, context):
        self.log.info("Running Data Quality Checks")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for test in self.tests:
            sql = test['check_sql']
            expected = test['expected_result']

            self.log.info(f"Running test: {sql}")
            records = redshift.get_records(sql)[0]

            if records[0] != expected:
                raise ValueError(
                    f"Data quality check failed: {sql}. "
                    f"Expected {expected} but got {records[0]}"
                )

            self.log.info(f"Data quality check passed: {sql}")
