
# from airflow import DAG
# from datetime import timedelta, datetime
# from airflow.providers.http.sensors.http import HttpSensor
# from airflow.operators.python import PythonOperator
# import pandas as pd
# from bs4 import BeautifulSoup
# import requests
# from datetime import datetime
# import json
# from pandas import json_normalize
# from kafka import KafkaProducer

# KAFKA_HOST_IP="kafka"
# TOPIC = 'hose'
# def serializer(message):
#     return json.dumps(message).encode('utf-8')

# kafka_p = KafkaProducer(
#     bootstrap_servers = [f'{KAFKA_HOST_IP}:9092'],  
#     value_serializer=serializer
# )

# def get_html():
#     BASE_URL = 'https://s.cafef.vn/TraCuuLichSu2/3/VN30/'
#     str_today = datetime.today().strftime('%d/%m/%Y')
#     URL = BASE_URL + str_today + ".chn"
#     res = requests.get(URL)
#     soup = BeautifulSoup(res.text , 'html.parser')
#     return soup

# def get_finfo(code , size):
#     FINFO_URL = 'https://finfo-api.vndirect.com.vn/v4/stock_prices'
#     response = requests.get(FINFO_URL , params={
#         'sort' : 'date' ,
#         'size' : size,
#         'q' : 'code:' + code
#     } ,
#     headers = {
#       'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.34',
#   })
#     return response

# def get_info_stock(code):
#     print("-- GET STOCKS INFO --")
#     STOCK_URL = 'https://finfo-api.vndirect.com.vn/v4/stocks'
#     response = requests.get(STOCK_URL , params={
#         'q' : 'code:' + code
#     } ,
#     headers = {
#       'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.34',
#   })
#     return response

# def get_all_symbol_name():
#     soup = get_html()
#     sym = soup.find_all('a' , {'class': 'symbol'})
#     return [i.text for i in sym]



# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2023, 7, 4 , 20 , 33 , 0 ), 
#     'retries': 2,
#     'retry_delay': timedelta (minutes=2)
# }


# def update_hose_stocks():
#     print('TASK')
#     names = get_all_symbol_name()
#     data = []
#     for name in names:
#         response = get_info_stock(name).json()
#         response = response['data'][0]
#         print(response)
#         data.append(response)
#     # df = pd.DataFrame.from_records(data)

#     # now = datetime.now()
#     # dt_string = now.strftime("%d%m%Y%H%M%S")
#     # dt_string = 'get_finfo_stock_list_' + dt_string
#     # df.to_csv(f"{dt_string}.csv" , index= False)
#     kafka_p.send(TOPIC, data)
    


# with DAG('finfo' , default_args = default_args, schedule_interval ='@daily', catchup=False) as dag:
#     print("DAG OK Hehe")
#     task_update_hose_stocks = PythonOperator(
#         task_id='get_finfo_stock_list',
#         python_callable=update_hose_stocks,
#     )
#     task_update_hose_stocks
