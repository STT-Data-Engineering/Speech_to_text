# import the required packages
import csv
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator  
from datetime import datetime, timedelta 

default_args = {
    'owner': 'benkart',
    'depends_on_past': False,
    'start_date': datetime(2022, 7, 9),
    'email_on_failure': False,
    'email_on_retry': False,    
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
} 

def publish_untranscribed_text_to_kafka():
    # Task 1 => read the transcription_text from s3 bucket and publish it to kafka 
    try:
        f = '../data/transcription_text.csv'
        # f = '/mnt/10ac-batch-5/week9/Benkart/transcription_text.csv'
        transcription_text = open(f, 'r')
        reader = csv.DictReader(transcription_text)

        for row in reader:
            """
            Send the row to Kafka
            """
            return row['text']

    except Exception as e:
        print(str(e)) 


with DAG(  
    catchup=False, 
    dag_id='audio_transcription_scheduler', 
    schedule_interval='*/2 * * * *', # running every 2 min
    description='Amharic speech data audio processing dag', 
    default_args=default_args    
) as dag_conf:

    
  publish_untranscribed_text_to_kafka = PythonOperator(
        task_id='untranscribed_text_to_kafka',
        python_callable = publish_untranscribed_text_to_kafka,
        dag=dag_conf
  )

  publish_processed_text_audio_to_Kafka = BashOperator(
        task_id='processed_text_audio_to_Kafka', 
        bash_command='python3 store_processed_data.py', # Assuming that we have a store_processed_data.py script
        dag=dag_conf
  ) 

  store_unprocessed_text_audio_to_bucket = BashOperator(
        task_id='unprocessed_text_to_bucket', 
        bash_command='python3 store_unprocessed_data.py', # Assuming that we have store_unprocessed_data.py script
        dag=dag_conf
  ) 

  publish_unprocessed_text_audio_to_spark = SparkSubmitOperator(
        task_id='unprocessed_text_audio_to_spark', 
        conn_id='spark_local',
        dag = dag_conf,
        application = '/scripts/audio_processor.py', # I assume the spark script is located in the scripts directory, and the name is audio_processor.py
        total_executor_cores = 4,        
        executor_cores=2,
        executor_memory='5g',
        driver_memory='5g', 
        execution_timeout=timedelta(minutes=10) 
  )

  store_processed_audio_to_s3 = SparkSubmitOperator(
        task_id='processed_text_audio_to_s3', 
        conn_id='spark_local',
        dag = dag_conf,
        application = '/scripts/audio_storer.py', # I assume the spark script is located in the scripts directory, and the name is audio_storeror.py
        total_executor_cores = 4,        
        executor_cores=2,
        executor_memory='5g',
        driver_memory='5g', 
        execution_timeout=timedelta(minutes=10) 
  )
  
     
# setting task dependencies
publish_untranscribed_text_to_kafka >> \
        store_unprocessed_text_audio_to_bucket >> \
                publish_unprocessed_text_audio_to_spark >> \
                         store_processed_audio_to_s3
