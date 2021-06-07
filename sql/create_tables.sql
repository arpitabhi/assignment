create database assignment;
create schema voucher;
create table voucher.recency_table (country_code VARCHAR(100),recency_segment VARCHAR(100), voucher_amount VARCHAR(100) );

create schema fvoucher;
create table fvoucher.frequency_table (country_code VARCHAR(100),frequent_segment VARCHAR(100), voucher_amount VARCHAR(100) );