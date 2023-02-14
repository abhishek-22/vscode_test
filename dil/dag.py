import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Define the default_args dictionary for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'pass_auth_arg_dag',
    default_args=default_args,
    description='Pass authentication created from task 1 to the subsequent 3 tasks',
    schedule_interval=timedelta(hours=1),
)

# Define the function for task 1 (create authentication)
def create_auth(**kwargs):
    # Example GET request to retrieve a string
    url = 'https://example.com/api/get_string'
    username = 'your_username'
    password = 'your_password'
    response = requests.get(url, auth=(username, password))
    auth = response.text
    kwargs['ti'].xcom_push(key='auth', value=auth)
    return "Auth created."

# Create the task using the PythonOperator
task_1 = PythonOperator(
    task_id='task_1',
    python_callable=create_auth,
    provide_context=True,
    dag=dag,
)

# Use the BashOperator for tasks 2, 3, and 4
task_2 = BashOperator(
    task_id='task_2',
    bash_command='python /path/to/python_file.py {{ ti.xcom_pull(key="auth", task_ids="task_1") }}',
    dag=dag,
)

task_3 = BashOperator(
    task_id='task_3',
    bash_command='python /path/to/python_file.py {{ ti.xcom_pull(key="auth", task_ids="task_1") }}',
    dag=dag,
)

task_4 = BashOperator(
    task_id='task_4',
    bash_command='python /path/to/python_file.py {{ ti.xcom_pull(key="auth", task_ids="task_1") }}',
    dag=dag,
)

# Set the order of task execution
task_1 >> task_2 >> task_3 >> task_4
