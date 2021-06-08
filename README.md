# Hi in this solution of the problem statement.
## I have divided it into 2 specific task. :+1:



**1. Creating a pipeline for data ingestion, transformation and loading.**
**2. Create an API to access the voucher amount for specific segment of customer.**


First run the backing services which include postgres.
Then run the datapipeline job.
Then start the web app and its API endpoint.


## Prerequisites of setting up Environment

## Overview

### Repository structure

In this repositary, we have following services: 

- `datapipeline`
- `web api`


### Build docker images
* Using docker compose build command
```ssh
docker compose build

// This will build images for postgres, web api and datapipeline
```

### Start the services and the containers
* Using docker compose up command
```ssh
docker compose up -d

// This will start the postgres server, create the pipeline and do the transformation and load operation
// It will also expose the API. Can access the swagger at 127.0.0.1:8000/docs
```









