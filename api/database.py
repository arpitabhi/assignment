import psycopg2
from config import USER,PASSWORD, PORT, HOST, RETRY, DATABASE

def connect_to_db(database):

    #establishing the connection
    while RETRY !=0 :
        try:
            conn = psycopg2.connect(database=database, user=USER, password=PASSWORD, host=HOST, port= PORT)
            conn.autocommit = True
            return conn

        except Exception as E:
            print(f"Database connection failed, retring for {RETRY} time : {E}")
            RETRY-=1
    
def query_to_fetch_coucher(tablename,country_code,field,value):
    
    query = f'''SELECT voucher_amount from {tablename} WHERE country_code = '{country_code}' AND {field} = {value}; '''

    return query

def fetch_data(tablename,country_code,field,value):

    conn = connect_to_db(DATABASE)
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Retrieving data
    query = query_to_fetch_coucher(tablename=tablename,country_code=country_code,field=field,value=value)
    cursor.execute(query)

    #Fetching 1st row from the table
    result = cursor.fetchall()

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

    return result

