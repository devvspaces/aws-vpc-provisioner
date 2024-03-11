from typing import Any, Dict
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.provider import AwsProvider
from decouple import config
from constructs import Construct


class MyTerraformStack(TerraformStack):
    def __init__(
        self, scope: Construct,
        name: str, vpc_data: Dict[str, Any] = None
    ):
        """
        This class is used to create a VPC in AWS using CDKTF.
        The VPC data is passed as a dictionary to the class. This can be passed
        when the class is instantiated.

        :param scope: The scope of the construct
        :type scope: Construct
        :param name: The name of the construct
        :type name: str
        :param vpc_data: The data to create the VPC, defaults to None
        :type vpc_data: Dict[str, Any], optional
        """
        super().__init__(scope, name)

        # Set the AWS provider with the access key and secret key
        AwsProvider(
            self, "aws",
            access_key=config('AWS_ACCESS_KEY_ID'),
            secret_key=config('AWS_SECRET_ACCESS_KEY'),
            region=config('AWS_REGION'),
        )

        if vpc_data is None:
            raise ValueError("VPC data is required")

        self.vpc = Vpc(
            self,
            "vpc",
            cidr_block=vpc_data.get('cidr_block'),
            instance_tenancy=vpc_data.get('instance_tenancy'),
            ipv4_ipam_pool_id=vpc_data.get('ipv4_ipam_pool_id'),
            ipv6_cidr_block=vpc_data.get('ipv6_cidr_block'),
            ipv6_ipam_pool_id=vpc_data.get('ipv6_ipam_pool_id'),
            enable_dns_support=vpc_data.get('enable_dns_support'),
            enable_dns_hostnames=vpc_data.get(
                'enable_dns_hostnames'),
            enable_network_address_usage_metrics=vpc_data.get(
                'enable_network_address_usage_metrics'),
            assign_generated_ipv6_cidr_block=vpc_data.get(
                'assign_generated_ipv6_cidr_block'),
            tags=vpc_data.get('tags'),
            ipv4_netmask_length=vpc_data.get('ipv4_netmask_length'),
            ipv6_netmask_length=vpc_data.get('ipv6_netmask_length'),
            ipv6_cidr_block_network_border_group=vpc_data.get(
                'ipv6_cidr_block_network_border_group'),
        )


# Specifying the Outdir to store the generated files, so it doesn't store it in the django root project and clutter it.
app = App(outdir="aws/cdktf.out")
