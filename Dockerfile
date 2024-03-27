# Use the official Python image with version 3.10.6-alpine3.16 as the base image
FROM python:3.10.6-alpine3.16

# Set the working directory inside the container
WORKDIR /app

# Install build dependencies
RUN apk update && apk add mariadb-dev gcc musl-dev
# RUN apk update && \
#     apk add mysql mysql-client && \
#     rm -f /var/cache/apk/* && \
#     addgroup mysql mysql && \
#     mkdir run/mysqld && \
#     touch /var/run/mysqld/mysqld.sock && \
#     touch /var/run/mysqld/mysqld.pid && \
#     chown -R mysql:mysql /var/run/mysqld/mysqld.sock && \
#     chown -R mysql:mysql /var/run/mysqld/mysqld.pid && \
#     chmod -R 644 /var/run/mysqld/mysqld.sock && \
#     apk add openrc --no-cache
# RUN apk update install python3-dev default-libmysqlclient-dev build-essential pkg-config

# Copy the contents of the local Django_New directory to the container at /app
COPY . /app

# Set environment variable to ensure that Python outputs logs in a readable format
ENV PYTHONUNBUFFERED 1

# Install any dependencies specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that Django will run on
EXPOSE 8000

# Command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
