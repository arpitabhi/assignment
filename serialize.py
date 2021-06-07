from typing import Optional
from pydantic import BaseModel


class requestclass(BaseModel):
   customer_id: int = 123
   country_code: str = "Peru"
   last_order_ts: str = "2018-05-03 00:00:00"
   first_order_ts: str = "2017-05-03 00:00:00"
   total_orders: int = 15
   segment_name: str = "recency_segment"


class responseclass(BaseModel):
   vocher_amount: str = ""
