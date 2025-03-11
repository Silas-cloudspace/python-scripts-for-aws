import boto3

# Create EC2 client using default credentials
ec2 = boto3.client('ec2')

def manage_ec2(action, instance_ids):
    """
    Start or stop EC2 instances
    
    Args:
        action (str): 'start' or 'stop'
        instance_ids (list): List of EC2 instance IDs to manage
    """
    try:
        if action == 'start':
            response = ec2.start_instances(InstanceIds=instance_ids)
            print(f"Starting instances: {instance_ids}")
        elif action == 'stop':
            response = ec2.stop_instances(InstanceIds=instance_ids)
            print(f"Stopping instances: {instance_ids}")
        else:
            print(f"Invalid action: {action}. Use 'start' or 'stop'")
            return
        
        # Print the status change for each instance
        for instance in response['StartingInstances' if action == 'start' else 'StoppingInstances']:
            print(f"Instance {instance['InstanceId']}: {instance['PreviousState']['Name']} -> {instance['CurrentState']['Name']}")
            
    except Exception as e:
        print(f"Error managing instances: {e}")

# Example usage - replace with your instance IDs
instance_ids = ['i-1234567890abcdef0']
manage_ec2('stop', instance_ids)

# To start instances, use:
# manage_ec2('start', instance_ids)