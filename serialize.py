from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class requestclass(BaseModel):
   customer_id: int
   country_code: str
   last_order_ts: str = "2018-05-03 00:00:00"
   first_order_ts: str = "2017-05-03 00:00:00"
   total_orders: int
   segment_name: str


class responseclass(BaseModel):
   vocher_amount: str