
from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
import pandas as pd
import requests
from datetime import datetime
import json
from pandas import json_normalize
from kafka import KafkaProducer

CITY = [
  "Tokyo",
  "New York",
  "Paris",
  "London",
  "Beijing",
  "Rio de Janeiro",
  "Sydney",
  "Moscow",
  "Ho Chi Minh City",
  "Hanoi",
  "Bangkok",
  "Berlin",
  "Istanbul",
  "Mumbai",
  "Johannesburg",
  "Mexico City",
  "Toronto",
  "Dubai",
  "Buenos Aires",
  "Los Angeles"
]

API = '331b051be7e841518ce180554231607'
URL = 'http://api.weatherapi.com/v1/current.json?aqi=yes&key=' + API + '&q='


KAFKA_HOST_IP="kafka"
TOPIC = 'weather2'

def serializer(message):
    return json.dumps(message).encode('utf-8')





default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 16 ), 
    'retries': 2,
    'retry_delay': timedelta (minutes=2)
}

def transform(a):
    new = {} 
    for i in a:
        print(i)
        for j in a[i]:
            print(" " , j)
            
            if(not type(a[i][j]) is dict):
                new[i + "_" + j] = a[i][j]
                continue

            for k in a[i][j]:
                    print("   " , k)
                    new[i +"_" +j +"_" +k] = a[i][j][k]

    return (new)

def weather_producer():
    kafka_p = KafkaProducer(
        bootstrap_servers = [f'{KAFKA_HOST_IP}:9092'],  
        value_serializer=serializer
    )
    for city in CITY:
        response = requests.get(URL + city ,
                                headers = {
      'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.34',
  })
        response = response.json()
        response = transform(response)
        kafka_p.send(TOPIC,response)
    # df = pd.DataFrame.from_records(data)

    # now = datetime.now()
    # dt_string = now.strftime("%d%m%Y%H%M%S")
    # dt_string = 'get_finfo_stock_list_' + dt_string
    # df.to_csv(f"{dt_string}.csv" , index= False)
    # kafka_p.send(TOPIC, data)
    


with DAG('weather' , default_args = default_args, schedule_interval ='*/10 * * * *', catchup=False) as dag:
    
    task_update = PythonOperator(
        task_id='task_update',
        python_callable=weather_producer,
    )
    task_update
