from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql import Window
from pyspark.sql.types import DoubleType
import os
import psycopg2


def session():
    '''
    Spark Session for initializing the session

    '''
    # Created spark session with local mode
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    #spark.sparkContext.setLogLevel("DEBUG")
    return spark

def blank_as_null(x):
    '''
    ignoring the null values
    '''
    return f.when(f.col(x) != "", f.col(x)).otherwise(None)

def check_recency(days):
    '''
    check the condition of recency
    '''

    return f.when(days >=0,f.when(days<30,0).when(days<61,30).when(days<91,61).when(days<121,91).when(days<181,121).otherwise(181)).otherwise(-1)

def read_df(spark,path):

    '''
    Reading the file using the spark session
    '''

    # Reading the data using the csv option with header as true
    df = spark.read.parquet(path,header=True)
    return df

def format_df(df):
    '''
    to insure sanity check and type casting the columns in df

    '''

    df = df.withColumn('timestamp',f.to_timestamp(f.col('timestamp')))
    df = df.withColumn('last_order_ts',f.to_timestamp(f.col('last_order_ts')))
    df = df.withColumn('first_order_ts',f.to_timestamp(f.col('first_order_ts')))
    df = df.withColumn('total_orders',f.when(blank_as_null("total_orders").cast(DoubleType())>=0,blank_as_null("total_orders").cast(DoubleType())).otherwise(-1))

    df = df.withColumn('frequent_segment',f.expr("CASE WHEN total_orders < 0 THEN -1 "+"WHEN total_orders >= 0 AND total_orders <= 4 THEN 0 " + "WHEN total_orders >= 5 AND total_orders <= 13 THEN 5 " + "WHEN total_orders >= 14 AND total_orders <= 37 THEN 14 " + "ELSE 38 END"))
    df = df.withColumn('recency_segment',check_recency(f.datediff(f.col('timestamp'),f.col('last_order_ts'))))

    df_select = df.select(f.col('country_code'),f.col('voucher_amount'),f.col('frequent_segment'),f.col('recency_segment'))

    return df_select

def frequent_table(df_select):

    '''
    
    To create separate df for frequent segment

    '''

    df_freq = df_select.groupBy("country_code","frequent_segment","voucher_amount").agg(f.count("*").alias("count"))
    window = Window.partitionBy("country_code","frequent_segment").orderBy(f.desc(f.col('count')))
    df_freq = df_freq.select('*', f.rank().over(window).alias('rank')).filter(f.col('rank') < 2) 
    df_freq = df_freq.select(f.col('country_code'),f.col('frequent_segment'),f.col('voucher_amount'))

    return df_freq

def recent_table(df_select):

    '''
    
    To create separate df for recent segment

    '''

    df_recen = df_select.groupBy("country_code","recency_segment","voucher_amount").agg(f.count("*").alias("count"))
    window2 = Window.partitionBy("country_code","recency_segment").orderBy(f.desc(f.col('count')))
    df_recen = df_recen.select('*', f.rank().over(window2).alias('rank')).filter(f.col('rank') < 2) 
    df_recen = df_recen.select(f.col('country_code'),f.col('recency_segment'),f.col('voucher_amount'))

    return df_recen


def write_to_postgres(df,table):

    '''
    to write the df to the postgress table

    '''

    url_connect = "jdbc:postgresql://postgres:5432/assignment"
    mode = "overwrite"
    user="postgres"
    password = "postgres"
	
    df.write.format("jdbc").mode(mode) \
            .option('driver', 'org.postgresql.Driver') \
            .option("url", url_connect) \
            .option("dbtable", table) \
            .option("user", user) \
            .option("password", password) \
            .save()


def create_tables():

    conn = psycopg2.connect(
    database="assignment", user='postgres', password='postgres', host='postgres', port= '5432'
    )

    #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Retrieving data

    cursor.execute(''' DROP SCHEMA IF EXISTS voucher CASCADE; ''')

    cursor.execute(''' DROP SCHEMA IF EXISTS fvoucher CASCADE; ''')

    cursor.execute(''' create schema voucher; create schema fvoucher; ''')

    cursor.execute(''' create table voucher.recency_table (country_code VARCHAR(100),recency_segment VARCHAR(100), voucher_amount VARCHAR(100) );
                        create table fvoucher.frequency_table (country_code VARCHAR(100),frequent_segment VARCHAR(100), voucher_amount VARCHAR(100) );  ''')

    
    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()



if __name__ == "__main__":

    spark = session()
    
    # path of the input file
    path = os.path.join(os.getcwd(),"data.parquet.gzip")
    #os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.1.1 pyspark-shell'
    
    df=read_df(spark=spark,path=path)
    df=format_df(df)
    
    df_freq=frequent_table(df)
    df_recen=recent_table(df)
    
    fre_table = "fvoucher.frequency_table"
    rec_table = "voucher.recency_table"
    datafame = "dataframe"

    create_tables()
    write_to_postgres(df_freq,fre_table)
    write_to_postgres(df_recen,rec_table)
    #write_to_postgres(df,datafame)
    
    spark.stop()
