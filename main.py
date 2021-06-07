import requests
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import fetch_data
from serialize import requestclass,responseclass
import re

app = FastAPI()


@app.post("/voucher/", name="voucher: get")
async def show_records(customer:requestclass) -> responseclass:
    country_code = customer.country_code
    last_order_ts = customer.last_order_ts
    first_order_ts = customer.first_order_ts
    total_orders = customer.total_orders
    segment_name = customer.segment_name
    
    last_order_ts = datetime.strptime(last_order_ts,'%Y-%m-%d %H:%M:%S')
    ts = datetime.now()
    
    ts = ts-last_order_ts
    ts=ts.days

    
    if re.search('frequent.*',segment_name):
        table = 'fvoucher.frequency_table'
        field = 'frequent_segment'
        if total_orders<0:
            value = '-1'
        elif total_orders>=0 and total_orders<=4:
            value = '0'
        elif total_orders>=5 and total_orders<=13:
            value = '5'
        elif total_orders>=14 and total_orders<=37:
            value = '14'
        else:
            value = '38'

    elif re.search('recency.*',segment_name):
        table = 'voucher.recency_table'
        field = 'recency_segment'
        if ts<0:
            value='-1'
        elif ts<30:
            value='0'
        elif ts<61:
            value='30'
        elif ts<91:
            value='61'
        elif ts<121:
            value='91'
        elif ts<181:
            value='121'
        else:
            value='181'

    try:
        print(table,field,value)
        records = fetch_data(tablename=table,country_code='Peru',field=field,value=value)
        print(records)
        
        if len(records)>0:
            return {"vocher_amount": records[0][0]}
        else:
            return {"vocher_amount": ''}
    except:
        return {"vocher_amount": ''}





