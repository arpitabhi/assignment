create database assignment;
\connect assignment;

IF (NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'voucher' OR name = 'fvoucher')) 
BEGIN
    EXEC ('CREATE SCHEMA voucher ; CREATE SCHEMA fvoucher;')
END

create table voucher.recency_table (country_code VARCHAR(100),recency_segment VARCHAR(100), voucher_amount VARCHAR(100) );

create table fvoucher.frequency_table (country_code VARCHAR(100),frequent_segment VARCHAR(100), voucher_amount VARCHAR(100) );
