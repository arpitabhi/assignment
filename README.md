# Hi in this solution of the problem statement.
## I have divided it into 2 specific task. :+1:



**1. Creating a pipeline for data ingestion, transformation and loading.**

**2. Create an API to access the voucher amount for specific segment of customer.**



## Prerequisites of setting up Environment
- `Git`
- `Docker for Desktop`

## Overview

### Repository structure

In this repositary, we have following services: 

- `datapipeline`
- `web api`

### Architecture design

![Design](https://github.com/arpitabhi/assignment/blob/main/architecture.jpg/)

### Steps to run the services.

## 1. Clone git repo.
```ssh
git clone https://github.com/arpitabhi/assignment.git

// This will clone this git repo to your local machine.
```
## 2. Navigate to the repo.
```ssh
cd ./assignment

// This will change the directory.
```


## 3. Build docker images
* Using docker compose build command
```ssh
docker compose build

// This will build images for postgres, web api and datapipeline
```

## 4. Start the services and the containers
* Using docker compose up command
```ssh
docker compose up -d

// This will start the postgres server, create the pipeline and do the transformation and load operation
// It will also expose the API. Can access the swagger at 127.0.0.1:8000/docs
```

## 5. Test the services.
```ssh
access swagger on 127.0.0.1:8000/docs test with the default request.

Run the postman collection.
1. Import the json file.
2. Run the collection.
3. Check the results.


```







