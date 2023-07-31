
from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
import pandas as pd
import requests
from datetime import datetime
import json
from pandas import json_normalize
from kafka import KafkaConsumer





def serializer(message):
    return json.dumps(message).encode('utf-8')





default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 19 ), 
    'retries': 2,
    'retry_delay': timedelta (minutes=2)
}


def get_consumer():
    
    consumer = KafkaConsumer(
        'weather',                 # Tên topic cần subscribe
        bootstrap_servers='kafka:9092',  # Địa chỉ và port của Kafka broker
        auto_offset_reset='earliest',  # Đặt lại offset khi consumer mới bắt đầu
        enable_auto_commit=True,    # Tự động commit offset
    )
    print("------ KET NOI XONG")
    count = 0 
    for message in consumer:
        count += 1
        # print(message.value.decode())
    print("SO LUONG: " + count)
    print("------ PRINT XONG")
    


with DAG('consumer' , default_args = default_args, schedule_interval ='*/10 * * * *', catchup=False) as dag:
    
    task_consumer = PythonOperator(
        task_id='task_consumer',
        python_callable=get_consumer,
    )
    task_consumer
