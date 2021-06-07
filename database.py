import psycopg2

def fetch_data(tablename,country_code,field,value):
    #establishing the connection
    conn = psycopg2.connect(
    database="assignment", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
    )

    #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Retrieving data
    cursor.execute(f'''SELECT voucher_amount from {tablename} WHERE country_code = '{country_code}' AND {field} = {value}; ''')


    #Fetching 1st row from the table
    result = cursor.fetchall()

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

    return result
