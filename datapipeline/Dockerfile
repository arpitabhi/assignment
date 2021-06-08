# set base image (host OS)
# ARG BASE_CONTAINER=jupyter/scipy-notebook
# FROM $BASE_CONTAINER


# ARG spark_version="3.1.2"
# ARG hadoop_version="3.2"
# ARG spark_checksum="2385CB772F21B014CE2ABD6B8F5E815721580D6E8BC42A26D70BBCDDA8D303D886A6F12B36D40F6971B5547B70FAE62B5A96146F0421CB93D4E51491308EF5D5"
# ARG openjdk_version="8"


# ENV APACHE_SPARK_VERSION="${spark_version}" \
#     HADOOP_VERSION="${hadoop_version}"

# RUN apt-get update --yes && \
#     apt-get install --yes --no-install-recommends \
#     "openjdk-${openjdk_version}-jre-headless" \
#     ca-certificates-java

# # Spark installation
# WORKDIR /tmp
# RUN wget -q "https://archive.apache.org/dist/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
#     echo "${spark_checksum} *spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" | sha512sum -c - && \
#     tar xzf "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" -C /usr/local --owner root --group root --no-same-owner && \
#     rm "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

# WORKDIR /usr/local

# # Configure Spark
# ENV SPARK_HOME=/usr/local/spark
# ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info" \
#     PATH="${PATH}:${SPARK_HOME}/bin"

# RUN ln -s "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" spark && \
#     # Add a link in the before_notebook hook in order to source automatically PYTHONPATH
#     mkdir -p /usr/local/bin/before-notebook.d && \
#     ln -s "${SPARK_HOME}/sbin/spark-config.sh" /usr/local/bin/before-notebook.d/spark-config.sh

# # Fix Spark installation for Java 11 and Apache Arrow library
# # see: https://github.com/apache/spark/pull/27356, https://spark.apache.org/docs/latest/#downloading
# RUN cp -p "${SPARK_HOME}/conf/spark-defaults.conf.template" "${SPARK_HOME}/conf/spark-defaults.conf" && \
#     echo 'spark.driver.extraJavaOptions -Dio.netty.tryReflectionSetAccessible=true' >> "${SPARK_HOME}/conf/spark-defaults.conf" && \
#     echo 'spark.executor.extraJavaOptions -Dio.netty.tryReflectionSetAccessible=true' >> "${SPARK_HOME}/conf/spark-defaults.conf"

# set the working directory in the container

# FROM python:3.7-stretch

# RUN apt-get update
# RUN apt-get install default-jdk -y

# ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
# RUN export JAVA_HOME

# # ENV POST_URL https://jdbc.postgresql.org/download/postgresql-42.2.5.jar
# # RUN wget ${POST_URL}
# # RUN mv postgresql-42.2.5.jar /opt/spark/jars



FROM python:3.8


ENV SPARK_VERSION 3.1.1
ENV SPARK_HADOOP_PROFILE 3.2
ENV SPARK_SRC_URL https://www.apache.org/dist/spark/spark-$SPARK_VERSION/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz
ENV SPARK_HOME=/opt/spark
# ENV PATH $PATH:$SPARK_HOME/bin

RUN wget ${SPARK_SRC_URL}
RUN tar -xzf spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz

RUN mv spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE} /opt/spark
RUN rm -f spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_PROFILE}.tgz

RUN apt-get update
RUN apt-get install default-jdk -y

ENV JAVA_HOME  /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

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