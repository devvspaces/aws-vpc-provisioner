# aws-vpc-provisioner

This application allows you to deploy new aws vpc using a user interface. It depends on CDKTF to deploy the infrastructure.

## Prerequisites

- CDKTF installed <https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install>
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

The application uses CDKTF to deploy the infrastructure. The application creates a new directory in the `cdktf.out` folder and generates the terraform code. Then it runs `cdktf deploy` to deploy the infrastructure.

Want to know more about CDKTF? Check the documentation <https://learn.hashicorp.com/tutorials/terraform/cdktf-intro>

To deploy new VPCs a uuid4 is generated and used as the stack name. The stack name is used to create a new directory in the `cdktf.out` folder. This way, the application can deploy multiple VPCs at the same time.

The `cdktf.out` directory is located in the `aws` directory. It's placed there to separate the terraform code from the application code.
