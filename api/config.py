# File to store all the constants and config parameters


FREQUENCY_TABLE = 'fvoucher.frequency_table'
FREQUENT_FIELD = 'frequent_segment'
RECENCY_TABLE = 'voucher.recency_table'
RECENCY_FIELD = 'recency_segment'
VOUCHER_NAME = "vocher_amount"

RECENCY_DICT = {
                0:"-1",
                30:"0",
                61:"30",
                91:"61",
                121:"91",
                181:"121",
                2147483647:"181"
                }
RECENCY_LIST = list(RECENCY_DICT.keys())
RECENCY_LIST.sort()

FREQUENCY_DICT = {
                0:"-1",
                5:"0",
                14:"5",
                38:"14",
                2147483647:"38"
                }
FREQUENCY_LIST = list(FREQUENCY_DICT.keys())
FREQUENCY_LIST.sort()