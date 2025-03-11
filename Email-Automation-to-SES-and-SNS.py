import boto3

def send_email_sns_ses(subject, message, recipient):
    # Create SNS and SES clients using default credentials
    sns = boto3.client('sns')
    ses = boto3.client('ses')
    
    # Create an SNS topic for the email
    topic_response = sns.create_topic(Name='email-topic')
    topic_arn = topic_response['TopicArn']
    
    # Your email that has been verified in SES
    email_from = "your-email@example.com"  # Replace with your verified email
    
    try:
        # Send email via SES
        ses_response = ses.send_email(
            Source=email_from,
            Destination={
                'ToAddresses': [
                    recipient,
                ]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': message
                    }
                }
            }
        )
        print(f"Email sent via SES: {ses_response['MessageId']}")
        
        # Send notification via SNS
        sns_response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        print(f"Notification sent via SNS: {sns_response['MessageId']}")
        
        print("Email and notification sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Replace with your subject, message, and recipient
    subject = "Test Email from AWS"
    message = "Hello, This is a test email sent using Amazon SNS and SES"
    recipient = "recipient@example.com"  # Replace with the recipient's email
    
    send_email_sns_ses(subject, message, recipient)