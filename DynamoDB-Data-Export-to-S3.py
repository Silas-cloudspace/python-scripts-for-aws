import boto3
import json
from datetime import datetime

# Create resources using default credentials
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def export_dynamodb_to_s3(table_name, bucket_name, file_name=None):
    """
    Export all items from a DynamoDB table to an S3 bucket
    
    Args:
        table_name (str): Name of the DynamoDB table
        bucket_name (str): Name of the S3 bucket
        file_name (str, optional): Name of the file in S3. Defaults to a timestamped name.
    """
    try:
        # Create a timestamp-based filename if none provided
        if not file_name:
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            file_name = f"{table_name}-{timestamp}.json"
        
        # Get the DynamoDB table
        table = dynamodb.Table(table_name)
        
        print(f"Scanning table {table_name}...")
        
        # Scan the table (handles pagination automatically)
        items = []
        scan_kwargs = {}
        done = False
        
        while not done:
            response = table.scan(**scan_kwargs)
            items.extend(response['Items'])
            
            # Print progress
            print(f"Retrieved {len(items)} items so far")
            
            # Check if there are more items to scan
            if 'LastEvaluatedKey' in response:
                scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            else:
                done = True
        
        # Convert data to JSON
        json_data = json.dumps(items, default=str, indent=2)
        
        # Upload to S3
        print(f"Uploading {len(items)} items to S3...")
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json_data,
            ContentType='application/json'
        )
        
        print(f"Data successfully exported to s3://{bucket_name}/{file_name}")
        print(f"Total items exported: {len(items)}")
        
    except Exception as e:
        print(f"Error exporting data: {e}")

# Example usage - replace with your values
table_name = 'my-dynamodb-table'
bucket_name = 'my-s3-bucket'

# Use with default timestamped filename
export_dynamodb_to_s3(table_name, bucket_name)

# Or specify a custom filename
# export_dynamodb_to_s3(table_name, bucket_name, 'my-backup.json')