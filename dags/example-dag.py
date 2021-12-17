from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.version import version
from datetime import datetime, timedelta


def my_custom_function(ts,**kwargs):
    """
    This can be any python code you want and is called from the python operator. The code is not executed until
    the task is run by the airflow scheduler.
    """
    print(f"I am task number {kwargs['task_number']}. This DAG Run execution date is {ts} and the current time is {datetime.now()}")
    print('Here is the full DAG Run context. It is available because provide_context=True')
    print(kwargs)


default_args = {
    'owner': 'a3data',
    'start_date': datetime(2021, 12, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'depends_on_past':False
}

with DAG(dag_id='DAG_Twitter', schedule_interval = "0 22 * * *",
default_args=default_args, catchup = False, tags=['analytics', 'reclamacoes', 'interacoes', 'redes_sociais']) as dag:

    create_table_gold_reclamacoes_redes_sociais = BashOperator(
        task_id = 'DTG_PEX_reclamacoes_redes_sociais',
        bash_command = "python /usr/local/airflow/scripts/data_processing/Gold/DTG_PEX_reclamacoes_redes_sociais.py '''{{var.value.AWS_SECRET_KEY_ID}}''' '''{{var.value.AWS_SECRET_ACCESS_KEY}}'''"
    )

create_table_gold_reclamacoes_redes_sociais