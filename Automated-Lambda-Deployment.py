import boto3
import os

# Create Lambda client using default credentials
lambda_client = boto3.client('lambda')

def deploy_lambda(function_name, zip_file_path):
    """
    Update an existing AWS Lambda function with new code
    
    Args:
        function_name (str): Name or ARN of the Lambda function
        zip_file_path (str): Path to the ZIP file containing the function code
    """
    try:
        # Check if the ZIP file exists
        if not os.path.exists(zip_file_path):
            print(f"Error: ZIP file not found at {zip_file_path}")
            return False
            
        # Check file size
        file_size = os.path.getsize(zip_file_path) / (1024 * 1024)  # Size in MB
        print(f"Deploying {function_name} with ZIP file: {zip_file_path} ({file_size:.2f} MB)")
        
        # Open and read the ZIP file
        with open(zip_file_path, 'rb') as f:
            zip_content = f.read()
            
            # Update the Lambda function code
            print(f"Updating Lambda function {function_name}...")
            response = lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content,
                Publish=True  # Create a new version
            )
            
            # Wait for the update to complete
            print("Waiting for the update to complete...")
            waiter = lambda_client.get_waiter('function_updated')
            waiter.wait(
                FunctionName=function_name,
                WaiterConfig={
                    'Delay': 5,
                    'MaxAttempts': 30
                }
            )
            
            # Print success information
            print(f"Lambda function {function_name} updated successfully!")
            print(f"Version: {response.get('Version', 'Unknown')}")
            print(f"Last Modified: {response.get('LastModified', 'Unknown')}")
            return True
            
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"Error: Lambda function {function_name} not found")
    except Exception as e:
        print(f"Error updating Lambda function: {e}")
    
    return False

# Example usage - replace with your values
function_name = 'my-lambda-function'
zip_file_path = './lambda.zip'

deploy_lambda(function_name, zip_file_path)