from django import forms
from ipaddress import ip_interface


# These are the choices for the instance tenancy
TENANCY_CHOICES = (
    ('default', 'Default'),
    ('dedicated', 'Dedicated'),
)


class AwsVpcForm(forms.Form):
    cidr_block = forms.CharField(max_length=18, required=False)
    instance_tenancy = forms.ChoiceField(choices=TENANCY_CHOICES, required=False)
    ipv4_ipam_pool_id = forms.CharField(max_length=36, required=False)
    ipv4_netmask_length = forms.IntegerField(required=False)
    ipv6_cidr_block = forms.CharField(max_length=150, required=False)
    ipv6_ipam_pool_id = forms.CharField(max_length=36, required=False)
    ipv6_netmask_length = forms.IntegerField(required=False)
    ipv6_cidr_block_network_border_group = forms.CharField(max_length=18, required=False)
    enable_dns_support = forms.BooleanField(required=False)
    enable_network_address_usage_metrics = forms.BooleanField(required=False)
    enable_dns_hostnames = forms.BooleanField(required=False)
    assign_generated_ipv6_cidr_block = forms.BooleanField(required=False)
    tags = forms.JSONField(required=False)

    def clean_cidr_block(self):
        """
        Clean the cidr block field

        :raises forms.ValidationError: If the CIDR block is invalid
        :return: The CIDR block
        :rtype: str
        """
        cidr_block = self.cleaned_data['cidr_block']
        try:
            if cidr_block:
                ip_interface(cidr_block)
        except ValueError:
            raise forms.ValidationError('Invalid CIDR block')
        return cidr_block

    def clean_ipv6_cidr_block(self):
        """
        Clean the ipv6 cidr block field

        :raises forms.ValidationError: If the CIDR block is invalid
        :return: The CIDR block
        :rtype: str
        """
        ipv6_cidr_block = self.cleaned_data['ipv6_cidr_block']
        try:
            if ipv6_cidr_block:
                ip_interface(ipv6_cidr_block)
        except ValueError:
            raise forms.ValidationError('Invalid CIDR block')
        return ipv6_cidr_block

    def clean_ipv4_netmask_length(self):
        """
        Validate the ipv4 netmask length

        :raises forms.ValidationError: If the netmask length is invalid
        :return: The netmask length
        :rtype: int
        """
        value = self.cleaned_data['ipv4_netmask_length']
        if value and value not in range(8, 33):
            raise forms.ValidationError('Invalid netmask length')
        return value

    def clean_ipv6_netmask_length(self):
        """
        Validate the ipv6 netmask length

        :raises forms.ValidationError: If the netmask length is invalid
        :return: The netmask length
        :rtype: int
        """
        value = self.cleaned_data['ipv6_netmask_length']
        if value and value not in range(1, 129):
            raise forms.ValidationError('Invalid netmask length')
        return value

    def clean(self):
        """
        Validate fields that depend on each other

        :raises forms.ValidationError: If the fields conflict
        """
        cleaned_data = super().clean()

        # Validate if both ipv6 cidr block and ipv6 netmask length are provided
        ipv6_cidr_block = cleaned_data.get('ipv6_cidr_block')
        ipv6_netmask_length = cleaned_data.get('ipv6_netmask_length')
        if ipv6_cidr_block and ipv6_netmask_length:
            raise forms.ValidationError({
                'ipv6_cidr_block': 'Both IPv6 CIDR block and \
netmask length should not be provided'
            })

        # Validate conflict of ipv6_ipam_pool_id and
        # assign_generated_ipv6_cidr_block
        ipv6_ipam_pool_id = cleaned_data.get('ipv6_ipam_pool_id')
        assign_generated_ipv6_cidr_block = cleaned_data.get(
            'assign_generated_ipv6_cidr_block')
        if ipv6_ipam_pool_id and assign_generated_ipv6_cidr_block:
            raise forms.ValidationError({
                'ipv6_ipam_pool_id': 'Both IPv6 IPAM pool \
ID and assign generated IPv6 CIDR block should not be provided'
            })

        return cleaned_data
