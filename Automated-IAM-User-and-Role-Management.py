import boto3
import secrets
import string

# Create IAM client using default credentials
iam = boto3.client('iam')

def create_iam_user(username, create_access_key=False, create_console_access=False):
    """
    Create an IAM user with optional access key and console access
    
    Args:
        username (str): Name for the new IAM user
        create_access_key (bool): Whether to create an access key for the user
        create_console_access (bool): Whether to create console access for the user
    
    Returns:
        dict: User information including any credentials created
    """
    user_info = {'UserName': username}
    
    try:
        # Create the user
        response = iam.create_user(UserName=username)
        print(f"IAM user '{username}' created successfully")
        
        # Create access key if requested
        if create_access_key:
            key_response = iam.create_access_key(UserName=username)
            user_info['AccessKey'] = {
                'AccessKeyId': key_response['AccessKey']['AccessKeyId'],
                'SecretAccessKey': key_response['AccessKey']['SecretAccessKey']
            }
            print(f"Access key created for user '{username}'")
            print(f"Access Key ID: {user_info['AccessKey']['AccessKeyId']}")
            print(f"Secret Access Key: {user_info['AccessKey']['SecretAccessKey']}")
            print("IMPORTANT: Save these credentials now - the secret key cannot be retrieved again!")
        
        # Create console access if requested
        if create_console_access:
            # Generate a random password
            password_chars = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(secrets.choice(password_chars) for i in range(12))
            
            # Create login profile with the generated password
            iam.create_login_profile(
                UserName=username,
                Password=password,
                PasswordResetRequired=True
            )
            
            user_info['ConsoleAccess'] = {
                'Password': password,
                'PasswordResetRequired': True
            }
            
            print(f"Console access created for user '{username}'")
            print(f"Temporary Password: {password}")
            print("User will be required to change this password on first login")
        
        return user_info
        
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Error: IAM user '{username}' already exists")
    except Exception as e:
        print(f"Error creating IAM user: {e}")
    
    return None

# Example usage - replace with your desired username
username = 'new-iam-user'

# Create a basic user
user_info = create_iam_user(username)

# Or create user with access key and console access
# user_info = create_iam_user(username, create_access_key=True, create_console_access=True)