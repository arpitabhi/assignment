create database assignment;
\connect assignment;

create table recency_table (country_code VARCHAR(100),recency_segment VARCHAR(100), voucher_amount VARCHAR(100) );

create table frequency_table (country_code VARCHAR(100),frequent_segment VARCHAR(100), voucher_amount VARCHAR(100) );
