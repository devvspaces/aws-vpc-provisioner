from rest_framework import serializers
from ipaddress import ip_interface


class DeploySerializer(serializers.Serializer):
    region = serializers.CharField(
        help_text='The region where the resources will be created.')
    name = serializers.CharField(help_text='Name of the Resources')
    cidr_block = serializers.CharField(help_text='Base CIDR block')
    subnet_length = serializers.IntegerField(
        help_text='The new prefix length for the subnet')
    subnet_count = serializers.IntegerField(
        help_text='The number of subnets to create',)
    tags = serializers.JSONField(help_text='Tags')

    def validate_cidr_block(self, value):
        """
        Validate the CIDR block

        :param value: The CIDR block
        :type value: str
        :raises serializers.ValidationError: If the CIDR block is invalid
        :return: The CIDR block
        :rtype: str
        """
        try:
            ip_interface(value)
        except ValueError:
            raise serializers.ValidationError('Invalid CIDR block')
        return value

    def validate_subnet(self, cidr_block, subnet_length):
        # Parse the CIDR block to extract the prefix length
        prefix_length = int(cidr_block.split("/")[1])

        # Calculate the available address space after subnetting
        available_address_space = 2 ** (32 - prefix_length - subnet_length)

        # Check if the available address space is positive
        return available_address_space > 0

    def validate(self, data):
        """
        Check that the subnet count is valid
        """
        if data['subnet_count'] < 1:
            raise serializers.ValidationError({
                "subnet_count": 'The number of subnets must be greater than 0'
            })

        cidr_block = data['cidr_block']
        subnet_length = data['subnet_length']
        if not self.validate_subnet(cidr_block, subnet_length):
            raise serializers.ValidationError({
                "subnet_length": 'Insufficient address space \
to extend prefix by the given subnet length.'
            })

        return data
