import boto3
import datetime

def create_ami(instance_id, ami_name=None, description=None, no_reboot=True):
    """
    Create an Amazon Machine Image (AMI) from an EC2 instance
    
    Args:
        instance_id (str): EC2 instance ID to create the image from
        ami_name (str, optional): Name for the AMI. Defaults to generated name.
        description (str, optional): Description for the AMI
        no_reboot (bool, optional): Whether to avoid rebooting the instance. Defaults to True.
    
    Returns:
        str: AMI ID if creation was successful, None otherwise
    """
    try:
        # Create EC2 client using default credentials
        ec2 = boto3.client('ec2')
        
        # Generate AMI name if not provided
        if not ami_name:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            ami_name = f"{instance_id}-{timestamp}"
        
        # Generate description if not provided
        if not description:
            description = f"AMI created from {instance_id} on {datetime.datetime.now().strftime('%Y-%m-%d')}"
        
        # Create the AMI
        print(f"Creating AMI '{ami_name}' from instance {instance_id}...")
        response = ec2.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            Description=description,
            NoReboot=no_reboot
        )
        
        ami_id = response['ImageId']
        print(f"AMI creation initiated. AMI ID: {ami_id}")
        
        # Add Name tag to the AMI
        ec2.create_tags(
            Resources=[ami_id],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': ami_name
                }
            ]
        )
        
        print(f"Added Name tag to AMI: {ami_name}")
        print(f"Note: AMI creation may take several minutes to complete.")
        print(f"Use 'aws ec2 describe-images --image-ids {ami_id}' to check the status.")
        
        if no_reboot:
            print("WARNING: AMI was created without rebooting the instance.")
            print("This may result in a less consistent image if there are pending filesystem changes.")
        
        return ami_id
    
    except Exception as e:
        print(f"Error creating AMI: {e}")
        return None

# Example usage - replace with your instance ID
instance_id = 'i-1234567890abcdef0'

# Create AMI with auto-generated name
create_ami(instance_id)

# Or create with specific name and description
# create_ami(instance_id, 'production-backup', 'Production server backup', no_reboot=True)