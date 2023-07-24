import boto3

ec2_client = boto3.client('ec2')
region_name = 'region_name' 

def list_total_instances(region):
    try:
        response = ec2_client.describe_instances(Filters=[{'Name': 'availability-zone', 'Values': [region + '*']}])
        instances = response['Reservations']
        
        return instances

    except Exception as e:
        print("Error listing instances:", str(e))
        return []

def add_tags_to_instance(instance_id, tags):
    try:
        ec2_client.create_tags(Resources=[instance_id], Tags=tags)
        print(f"Tags added to instance {instance_id}")
    except Exception as e:
        print(f"Error adding tags to instance {instance_id}:", str(e))

def add_tags_to_dependent_resources(instance_id, tags):
    try:
        response = ec2_client.describe_instance_attribute(InstanceId=instance_id, Attribute='blockDeviceMapping')
        volumes = response['BlockDeviceMappings']
        
        for volume in volumes:
            volume_id = volume['Ebs']['VolumeId']
            ec2_client.create_tags(Resources=[volume_id], Tags=tags)
            print(f"Tags added to volume {volume_id}")
        
        response = ec2_client.describe_iam_instance_profile_associations(Filters=[{'Name': 'instance-id', 'Values': [instance_id]}])
        iam_associations = response['IamInstanceProfileAssociations']
        
        for iam_association in iam_associations:
            instance_profile_arn = iam_association['IamInstanceProfile']['Arn']
            ec2_client.create_tags(Resources=[instance_profile_arn], Tags=tags)
            print(f"Tags added to instance profile {instance_profile_arn}")

    except Exception as e:
        print("Error adding tags to dependent resources:", str(e))

def main():
    instances = list_total_instances(region_name)

    if not instances:
        print(f"No instances found in the {region_name} region.")
        return

    for reservation in instances:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = [
                {'Key': 'application-id', 'Value': 'your_application_id'},  
                {'Key': 'environment-name', 'Value': 'your_environment_name'},  
            ]
            add_tags_to_instance(instance_id, tags)
            add_tags_to_dependent_resources(instance_id, tags)

if __name__ == "__main__":
    main()

