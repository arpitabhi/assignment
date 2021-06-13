from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from database import fetch_data
from serialize import requestclass,responseclass
from config import FREQUENCY_TABLE,FREQUENT_FIELD, RECENCY_TABLE,RECENCY_FIELD, VOUCHER_NAME, \
                    RECENCY_DICT, RECENCY_LIST, FREQUENCY_LIST, FREQUENCY_DICT, RETRY
from loggingfile import Logger
import re

app = FastAPI()
LOG=Logger("api_logging_file")

@app.post("/voucher/", name="voucher: get")
async def show_records(customer:requestclass) -> responseclass:
    country_code = customer.country_code
    last_order_ts = customer.last_order_ts
    first_order_ts = customer.first_order_ts
    total_orders = customer.total_orders
    segment_name = customer.segment_name
    LOG.info("request received")
    
    last_order_ts = datetime.strptime(last_order_ts,'%Y-%m-%d %H:%M:%S')
    ts = datetime.now()
    
    ts = ts-last_order_ts
    ts=ts.days

    LOG.info("Validating request")
    if re.search('frequent.*',segment_name):
        LOG.info("Request type is frequent segment")
        table = FREQUENCY_TABLE
        field = FREQUENT_FIELD
        ls=FREQUENCY_LIST
        ds=FREQUENCY_DICT

    elif re.search('recency.*',segment_name):
        LOG.info("Request type is Recent segment")
        table = RECENCY_TABLE
        field = RECENCY_FIELD
        ls=RECENCY_LIST
        ds=RECENCY_DICT

    for key in ls:
        if ts<key:
            value=ds[key]
            break


    try:
        LOG.info(f"Fetching voucher amount for frequent segment for country {country_code}")
        records = fetch_data(tablename=table,country_code=country_code,field=field,value=value,RETRY=RETRY)
        LOG.info("Fetch data. Preparing response")
        return {VOUCHER_NAME: records[0][0]}
    except Exception as E:
        LOG.error("Error in fetching voucher value")
        LOG.info(f"Exception occured with error code : {E}")
        return {VOUCHER_NAME: ''}


if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0", port=8000)


