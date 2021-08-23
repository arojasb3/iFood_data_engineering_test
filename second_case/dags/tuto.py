import json
import pandas as pd
import os
import datetime
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator



def getDB():
    df = pd.read_csv('https://ifood-data-architect-test-source.s3.amazonaws.com/consumer.csv.gz')

    df.to_csv('/usr/local/airflow/logs/consumer.csv')


    return 'printDB'



def printDBfun():
    """
    Upload the results data to the database
    """
    results = '/usr/local/airflow/logs/consumer.csv'

    df2 = pd.read_csv(results)

    print(df2)

    return 'endRun'


# set up DAG arguments
defaultArgs = {
    'owner': 'alejandro_rojas',
    'start_date': datetime.datetime(2021, 1, 1),
    'retries': 3,
    'retry_delay': datetime.timedelta(seconds=30)
}

with DAG('ifood_de_dag',
         schedule_interval='@daily',
         default_args=defaultArgs,
         catchup=False) as dag:

    downloadDB = PythonOperator(
        task_id='getDB',
        python_callable=getDB
    )

    printDB = BranchPythonOperator(
        task_id='printDB',
        python_callable=printDBfun,
        do_xcom_push=False
    )

    endRun = DummyOperator(
        task_id='endRun',
        trigger_rule='none_failed'
    )

    # set tasks relations 
    downloadDB >> printDB

    printDB >> endRun