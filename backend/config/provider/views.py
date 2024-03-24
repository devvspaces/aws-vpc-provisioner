from os import chdir
import json
import re
import subprocess
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import DeploySerializer
from django.conf import settings
from .helpers import print_gradually


class DeployView(GenericAPIView):
    """
    Deploy new VPC resources
    """
    serializer_class = DeploySerializer

    def write_input(self, data):
        """
        Write form data to terraform json input
        """
        file_path = settings.TERRAFORM_INPUT

        with open(file_path, 'r') as file:
            file_data = json.load(file)
            access_key = file_data['access_key']
            secret_key = file_data['secret_key']

        with open(file_path, 'w') as file:
            json.dump({
                **data,
                "access_key": access_key,
                "secret_key": secret_key
            }, file)
        return file_path

    def deploy(self, data):
        """
        Deploy the VPC resources
        """
        success = True
        error_message = None
        self.write_input(data)

        # Run the terraform apply command
        print("Deploying...")
        cmd = ["terraform", "apply", "-auto-approve"]
        chdir("tf.out")
        try:
            print_gradually(cmd)
        except subprocess.CalledProcessError as e:
            success = False
            error_message = e.stderr

            # Use regex to extract the error message
            match = re.search(r'Error: (.+)', error_message)
            if match:
                error_message = match.group(1).capitalize()

        chdir("..")

        # Read the terraform output
        output = {}
        with open(settings.TERRAFORM_OUTPUT, 'r') as file:
            state = json.load(file)
            output['vpc_id'] = state['outputs']['vpc_id']['value']
            output['subnet_ids'] = state['outputs']['subnet_ids']['value']

        if success:
            return {
                "success": success,
                "error_message": None,
                "output": output
            }
        return {
            "success": success,
            "error_message": error_message,
            "output": None
        }

    def post(self, request, *args, **kwargs):
        """
        Deploy new VPC resources
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Deploy
        data = self.deploy(data)
        return Response(data)
