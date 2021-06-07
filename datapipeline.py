from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql import Window
from pyspark.sql.types import DoubleType
from pyspark.sql import DataFrameWriter


# Created spark session with local mode
spark = SparkSession.builder.master("local[*]").getOrCreate()
#spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")

# path of the input file
path = "C:/Users/arpit/Desktop/EMR/data.parquet.gzip"
# Create SparkCOntext as sc

def blank_as_null(x):
    return f.when(f.col(x) != "", f.col(x)).otherwise(None)

def check_recency(days):
    return f.when(days >=0,f.when(days<30,0).when(days<61,30).when(days<91,61).when(days<121,91).when(days<181,121).otherwise(181)).otherwise(None)


# Reading the data using the csv option with header as true
df = spark.read.parquet(path,header=True)

#df.show()



df = df.withColumn('timestamp',f.to_timestamp(f.col('timestamp')))
df = df.withColumn('last_order_ts',f.to_timestamp(f.col('last_order_ts')))
df = df.withColumn('first_order_ts',f.to_timestamp(f.col('first_order_ts')))
df = df.withColumn('total_orders',f.when(blank_as_null("total_orders").cast(DoubleType())>=0,blank_as_null("total_orders").cast(DoubleType())).otherwise(0))

df = df.withColumn('frequent_segment',f.expr("CASE WHEN total_orders >= 0 AND total_orders <= 4 THEN 0 " + "WHEN total_orders >= 5 AND total_orders <= 13 THEN 5 " + "WHEN total_orders >= 14 AND total_orders <= 37 THEN 14 " + "ELSE 38 END"))

#df = df.withColumn('frequent_segment',f.when(f.col('total_orders')>=0 & f.col('total_orders')<=4,0).when(f.col('total_orders')>=5 & f.col('total_orders')<=13,5).when(f.col('total_orders')>=14 & f.col('total_orders')<=37,14).otherwise(38))

#df = df.withColumn('recency_segment',f.expr("CASE WHEN DATEDIFF(day,last_order_ts,timestamp) <30 THEN 0 " + "WHEN DATEDIFF(day,last_order_ts,timestamp) >=30 AND DATEDIFF(day,last_order_ts,timestamp) <=60 THEN 30  " + "WHEN DATEDIFF(day,last_order_ts,timestamp) >60 AND DATEDIFF(day,last_order_ts,timestamp) <=90 THEN 61  " + "WHEN DATEDIFF(day,last_order_ts,timestamp) >90 AND DATEDIFF(day,last_order_ts,timestamp) <=120 THEN 91  " + "WHEN DATEDIFF(day,last_order_ts,timestamp) >120 AND DATEDIFF(day,last_order_ts,timestamp) <=180 THEN 121  " + "ELSE 181 END"))
df = df.withColumn('recency_segment',check_recency(f.datediff(f.col('timestamp'),f.col('last_order_ts'))))

df_select = df.select(f.col('country_code'),f.col('voucher_amount'),f.col('frequent_segment'),f.col('recency_segment'))

df.printSchema()
#df.show()
#df_select.show()


df_freq = df_select.groupBy("country_code","frequent_segment").agg(f.max("voucher_amount").alias("voucher_amount"))
df_recen = df_select.groupBy("country_code","recency_segment").agg(f.max("voucher_amount").alias("voucher_amount"))

df_freq.show()
df_recen.show()



#my_writer = DataFrameWriter(df_freq)

url_connect = "jdbc:postgresql://0.0.0.0:5432/assignment"
table = "frequency_table"
mode = "overwrite"
properties = {"user":"postgres", "password":"postgres"}

#my_writer.option('driver', 'org.postgresql.Driver').jdbc(url=url_connect, table=table,mode= mode,properties= properties)

df_freq.write \
    .format("jdbc") \
    .option("url", url_connect) \
    .option("dbtable", table) \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .save()


'''

df_freq.write.format("jdbc").mode("overwrite") \
  .option('driver', 'org.postgresql.Driver') \
  .option("url", url_connect) \
  .option("dbtable", "frequency_table") \
  .option("user", "postgres") \
  .option("password", "postgres") \
  .save()


df_freq.write.format('jdbc').mode("overwrite") \
     .options(
      url='jdbc:mysql://127.0.0.1:3306',
      driver='com.mysql.jdbc.Driver',
      dbtable='begin.df_freq',
      user='root',
      password='password').save()

'''

