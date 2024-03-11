from os import chdir
from django.http import HttpResponse
from django.views.generic import FormView
from django.contrib import messages
from sys import stderr
import subprocess
from uuid import uuid4

from aws.main import MyTerraformStack, app

from .forms import AwsVpcForm


def print_gradually(cmd):
    """
    Run a command and print the output gradually.
    This ensures that the output is printed as the
    command is running in the terminal.

    This is an utility function.

    :param cmd: The command to run
    :type cmd: list
    :raises subprocess.CalledProcessError: If the command fails
    """
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True)
    for line in process.stdout:
        print(line, end="")  # Print without newline
    error = False
    for line in process.stderr:
        error = True
        print(line, file=stderr, end="")  # Print to stderr without newline
    process.wait()  # Wait for the process to finish
    if error:
        raise subprocess.CalledProcessError(process.returncode, cmd)


class Home(FormView):
    """
    This is the form view for the VPC form.

    initial is used to set the initial values of the form.
    Setting this values ensures that we don't see `None` strings
    in the form fields.
    """
    template_name = 'provider/index.html'
    form_class = AwsVpcForm
    success_url = '/'
    initial = {
        'cidr_block': '',
        'ipv4_ipam_pool_id': '',
        'ipv6_ipam_pool_id': '',
        'ipv6_cidr_block_network_border_group': '',
        'ipv6_cidr_block': '',
    }

    def form_valid(self, form: AwsVpcForm) -> HttpResponse:
        """
        Deploy the VPC using the form data.

        :param form: The form
        :type form: AwsVpcForm
        :return: The HTTP response
        :rtype: HttpResponse
        """
        success = True

        variables = [
            'cidr_block',
            'enable_dns_support',
            'enable_dns_hostnames',
            'instance_tenancy',
            'tags',
            'ipv4_netmask_length',
            'ipv4_ipam_pool_id',
            'ipv6_cidr_block',
            'ipv6_netmask_length',
            'ipv6_ipam_pool_id',
            'ipv6_cidr_block_network_border_group',
            'assign_generated_ipv6_cidr_block',
            'enable_network_address_usage_metrics',
        ]

        clean_data = {}

        for variable in variables:
            if form.cleaned_data[variable]:
                clean_data[variable] = form.cleaned_data[variable]

        # Generate a unique stack name
        stack_name = f"aws_vpc_stack-{uuid4()}"

        # Instantiate the stack with the clean data
        MyTerraformStack(app, stack_name, clean_data)

        print("Synthesizing...")
        # Synthesize the stack, this generates the Terraform code
        app.synth()

        # Run deploy
        print("Deploying...")
        chdir("aws")
        try:
            print_gradually(["cdktf", "deploy", stack_name,
                            "--skip-synth", "--auto-approve"])
        except subprocess.CalledProcessError:
            success = False
        chdir("..")

        if success:
            messages.success(self.request, 'VPC deployed successfully')
        else:
            messages.warning(self.request, 'Failed to deploy VPC')
        return super().form_valid(form)
