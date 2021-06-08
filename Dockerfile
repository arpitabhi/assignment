# set base image (host OS)
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# set the working directory in the container
WORKDIR /code

COPY /requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# Keeping port 8000 for FastAPI
EXPOSE 8000
# command to run on container start
CMD [ "python", "main.py" ]