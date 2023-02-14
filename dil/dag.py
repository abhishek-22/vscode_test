from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# Define the default_args dictionary for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'pass_string_dag',
    default_args=default_args,
    description='Pass a string generated from a Python file in task 1 to the subsequent 2 tasks',
    schedule_interval=timedelta(hours=1),
)

# Use the BashOperator for task 1
task_1 = BashOperator(
    task_id='task_1',
    bash_command='python /path/to/python_file_1.py',
    xcom_push=True,
    dag=dag,
)

# Use the BashOperator for tasks 2 and 3
task_2 = BashOperator(
    task_id='task_2',
    bash_command='python /path/to/python_file_2.py {{ ti.xcom_pull(task_ids="task_1") }}',
    dag=dag,
)

task_3 = BashOperator(
    task_id='task_3',
    bash_command='python /path/to/python_file_3.py {{ ti.xcom_pull(task_ids="task_1") }}',
    dag=dag,
)

# Set the order of task execution
task_1 >> task_2 >> task_3