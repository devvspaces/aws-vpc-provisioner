
FROM python:3.10-alpine

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Set environment variables
ENV TERRAFORM_VERSION=1.7.4
ENV TERRAFORM_SHA256SUM="285539a6fd62fb79f05edc15cc207ca90f282901c32261085ea0642a0d638dfd"

# Install required packages (curl, unzip) for downloading and installing Terraform
RUN apk add --no-cache curl unzip

# Download and install Terraform
RUN curl -o terraform.zip -L "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" && \
    echo "${TERRAFORM_SHA256SUM} terraform.zip" | sha256sum -c - && \
    unzip terraform.zip -d /usr/local/bin && \
    rm terraform.zip

# Verify Terraform installation
RUN terraform --version

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 8000

WORKDIR /app/config

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
