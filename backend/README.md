# aws-vpc-provisioner

This application allows you to deploy new aws vpc using a user interface. It depends on terraform to deploy the infrastructure.

## Prerequisites

- Terraform installed
- Python 3.7 or later

## Installation

Create virtual environment

```bash
python3 -m venv venv
```

Install dependencies

```bash
pip install -r requirements.txt
```

Setup environment variables

```bash
cp env.example .env
```

Then update the .env file with your AWS credentials.

## Usage

Run the application

```bash
python manage.py runserver
```

## How it works

This application uses terraform to deploy the infrastructure. When you create a new vpc, it updates the input.json file in the tf.out directory with the new vpc details. Then it runs the terraform apply command to deploy the new vpc.
