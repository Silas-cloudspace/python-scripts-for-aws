import boto3

# Create S3 resource using default credentials
s3 = boto3.resource('s3')

def sync_s3_buckets(source_bucket, destination_bucket):
    """
    Sync all objects from source bucket to destination bucket
    
    Args:
        source_bucket (str): Name of the source S3 bucket
        destination_bucket (str): Name of the destination S3 bucket
    """
    try:
        # Get all objects from the source bucket
        source_objects = list(s3.Bucket(source_bucket).objects.all())
        total_objects = len(source_objects)
        
        print(f"Found {total_objects} objects in {source_bucket}")
        
        # Copy each object to the destination bucket
        for i, obj in enumerate(source_objects, 1):
            try:
                # Define the source object
                copy_source = {
                    'Bucket': source_bucket,
                    'Key': obj.key
                }
                
                # Copy the object to the destination
                s3.Object(destination_bucket, obj.key).copy(copy_source)
                
                # Print progress
                print(f"[{i}/{total_objects}] Copied: {obj.key}")
                
            except Exception as e:
                print(f"Error copying {obj.key}: {e}")
        
        print(f"Data sync completed from {source_bucket} to {destination_bucket}")
    
    except Exception as e:
        print(f"Error syncing buckets: {e}")

# Example usage - replace with your bucket names
source_bucket = 'source-bucket-name'
destination_bucket = 'destination-bucket-name'

sync_s3_buckets(source_bucket, destination_bucket)