FROM python:3.8


ENV SPARK_VERSION 3.1.1
ENV SPARK_HADOOP_PROFILE 3.2
ENV SPARK_SRC_URL https://www.apache.org/dist/spark/spark-$SPARK_VERSION/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz
ENV SPARK_HOME=/opt/spark

RUN wget ${SPARK_SRC_URL}
RUN tar -xzf spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz

RUN mv spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE} /opt/spark
RUN rm -f spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz

RUN apt-get update
RUN apt-get install default-jdk -y

ENV POST_URL https://jdbc.postgresql.org/download/postgresql-42.2.5.jar
RUN wget ${POST_URL}
RUN mv postgresql-42.2.5.jar /opt/spark/jars


WORKDIR /code

COPY /requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

COPY /data.parquet.gzip /code/

# command to run on container start
CMD [ "python", "datapipeline.py" ]