#!/usr/bin/env python3
import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

response = ec2.describe_instances(
    Filters=[{'Name': 'tag:Name', 'Values': ['jenkins-demo-servers']}]
)

ips = []
for res in response['Reservations']:
    for inst in res['Instances']:
        ips.append(inst['PrivateIpAddress'])

with open('../inventories/hosts.template', 'w') as f:
    f.write("[all]\n")
    for ip in ips:
        f.write(f"{ip} ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/id_rsa\n")

print("Inventory updated:", ips)
