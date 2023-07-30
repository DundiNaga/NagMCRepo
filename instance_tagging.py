# Import the Boto3 library to interact with AWS services
import boto3
from pprint import pprint

# Create a session
session = boto3.Session(profile_name='default', region_name='us-east-1')

# Create a client for the EC2 service
ec2_client = session.client('ec2', 'us-east-1')

def get_instances_with_tags():
    instances_list = []

    response = ec2_client.describe_instances()
    for reservations in response['Reservations']:
        for instances in reservations['Instances']:
            instance_id = instances['InstanceId']
            instance_tags = instances.get('Tags', [])
            instance_tags_dict = {tag['Key']: tag['Value'] for tag in instance_tags}
            instances_list.append({'InstanceId': instance_id, 'Tags': instance_tags_dict})

    return instances_list

def add_tags_to_instance(instance_id, tags):
    try:
        ec2_client.create_tags(Resources=[instance_id], Tags=tags)
        print(f"Tags added successfully to InstanceId: {instance_id}")
    except Exception as e:
        print(f"Failed to add tags to InstanceId: {instance_id}")
        print(f"Error: {str(e)}")

def main():
    instances_list = get_instances_with_tags()
    pprint(instances_list)

    instance_ids = input("Enter the Instance ID(s) to add tags (comma-separated): ").split(',')
    tags_key = input("Enter the tag key: ")
    tags_value = input("Enter the tag value: ")

    tags_to_add = [{'Key': tags_key, 'Value': tags_value}]
    for instance_id in instance_ids:
        add_tags_to_instance(instance_id.strip(), tags_to_add)

if __name__ == "__main__":
    main()
