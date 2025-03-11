import boto3
import json

def update_s3_bucket_policy(bucket_name, policy=None, policy_file=None):
    """
    Update an S3 bucket policy
    
    Args:
        bucket_name (str): Name of the S3 bucket
        policy (str or dict, optional): Policy document as JSON string or dictionary
        policy_file (str, optional): Path to a JSON file containing the policy
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        # Create S3 client using default credentials
        s3 = boto3.client('s3')
        
        # Get policy from file if specified
        if policy_file and not policy:
            try:
                with open(policy_file, 'r') as f:
                    policy = f.read()
                print(f"Loaded policy from file: {policy_file}")
            except Exception as e:
                print(f"Error reading policy file: {e}")
                return False
        
        # Convert dictionary to JSON string if necessary
        if isinstance(policy, dict):
            policy = json.dumps(policy)
        
        # Validate policy is proper JSON
        try:
            json.loads(policy)
        except Exception as e:
            print(f"Error: Invalid JSON policy: {e}")
            return False
        
        # Get current policy (if any) before updating
        try:
            current_policy = s3.get_bucket_policy(Bucket=bucket_name)
            print("Current policy exists and will be replaced")
        except s3.exceptions.NoSuchBucketPolicy:
            print("No existing policy found - creating new policy")
        
        # Update the bucket policy
        s3.put_bucket_policy(Bucket=bucket_name, Policy=policy)
        print(f"Policy successfully updated for bucket: {bucket_name}")
        return True
        
    except s3.exceptions.NoSuchBucket:
        print(f"Error: Bucket '{bucket_name}' does not exist")
    except Exception as e:
        print(f"Error updating bucket policy: {e}")
    
    return False

# Example usage - replace with your bucket name
bucket_name = 'my-s3-bucket'

# Example policy - replace with your actual policy
example_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }
    ]
}

# Update with inline policy
update_s3_bucket_policy(bucket_name, example_policy)

# Or update with policy from file
# update_s3_bucket_policy(bucket_name, policy_file='policy.json')