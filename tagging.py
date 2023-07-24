# Import the Boto3 library to interact with AWS services
import boto3

# Create a client for the EC2 service
ec2 = boto3.client('ec2')

# Specify the region where you want to list the instances
region = 'us-east-1'

# List the instances in the specified region
instances = ec2.describe_instances(
    Filters=[
        {
            'Name': 'region',
            'Values': [region]
        }
    ]
)

# Add the application-id and environment-name tags to the instances
for instance in instances['Reservations']:
    for i in instance['Instances']:
        # Create tags for the EC2 instance
        ec2.create_tags(
            Resources=[i['InstanceId']],
            Tags=[
                {'Key': 'application-id', 'Value': 'my-app'},
                {'Key': 'environment-name', 'Value': 'dev'}
            ]
        )

# Add tags to the instance-dependent resources
for instance in instances['Reservations']:
    for i in instance['Instances']:
        # Get the volume ID for the instance
        volume_id = i['BlockDeviceMappings'][0]['Ebs']['VolumeId']

        # Add the application-id and environment-name tags to the volume
        ec2.create_tags(
            Resources=[volume_id],
            Tags=[
                {'Key': 'application-id', 'Value': 'my-app'},
                {'Key': 'environment-name', 'Value': 'dev'}
            ]
        )

        # Get the instance profile ID for the instance
        instance_profile_id = i['IamInstanceProfile']['Id']

        # Add the application-id and environment-name tags to the instance profile
        ec2.create_tags(
            Resources=[instance_profile_id],
            Tags=[
                {'Key': 'application-id', 'Value': 'my-app'},
                {'Key': 'environment-name', 'Value': 'dev'}
            ]
        )
