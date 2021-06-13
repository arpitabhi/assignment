URL_CONNECT = "jdbc:postgresql://host.docker.internal:5432/assignment"
MODE = "overwrite"

USER='postgres'
PASSWORD='postgres'
PORT= '5432'
HOST = 'host.docker.internal'
RETRY = 5
DATABASE = "assignment"

FREQUENCY_TABLE = 'fvoucher.frequency_table'
RECENCY_TABLE = 'voucher.recency_table'

POSTGRES_DRIVER = 'org.postgresql.Driver'


DROP_SCHEMA_VOUCHER = ''' DROP SCHEMA IF EXISTS voucher CASCADE; '''
DROP_SCHEMA_FVOUCHER = ''' DROP SCHEMA IF EXISTS fvoucher CASCADE; '''
CREATE_SCHEMA = ''' create schema voucher; create schema fvoucher; '''
CREATE_TABLE = '''  create table voucher.recency_table (country_code VARCHAR(100),
                                                        recency_segment VARCHAR(100), 
                                                        voucher_amount VARCHAR(100) );

                    create table fvoucher.frequency_table ( country_code VARCHAR(100),
                                                            frequent_segment VARCHAR(100), 
                                                            voucher_amount VARCHAR(100) );  '''
