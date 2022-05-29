# Docker file to build Django Web API image with GeoDjango and PostGIS
# Use slim variant for ligher image
FROM python:3.9-slim

# Set environment variables
# Dont store logs in buffers, send to console
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt


# Setup GEOS, PROJ and GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python3-gdal


# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

# Expose port 8000
EXPOSE 8000
# run The entrypoint script
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]