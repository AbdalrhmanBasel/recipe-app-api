# Dockerfile

# Use an official Python runtime as the parent image
FROM python:3.9-alpine3.13

# Label for metadata
LABEL maintainer="abdelrhman.info1@gmail.com"

# Set environment variable to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for building Python packages
RUN apk update && \
    apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        python3-dev \
        build-base \
        postgresql-client && \
    # Clean up apk cache to reduce image size
    rm -rf /var/cache/apk/*

# Copy requirements.txt and requirements.dev.txt to the container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the application code to the container
COPY ./app /app

# Set the working directory
WORKDIR /app

# Set state of development mode
ARG DEV=false

# Set up a virtual environment for Python packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base \
        postgresql-dev \
        musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Install additional development dependencies if in development mode
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps 

# Add non-root user for better security
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

# Set the PATH to include the virtual environment's binaries
ENV PATH="/py/bin:$PATH"

# Expose the port your application will run on
EXPOSE 8000

# Change to the non-root user
USER django-user

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
