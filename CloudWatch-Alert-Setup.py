import boto3

# Create CloudWatch client using default credentials
cloudwatch = boto3.client('cloudwatch')

def create_cloudwatch_alarm(instance_id, sns_topic_arn=None, cpu_threshold=70.0):
    """
    Create a CloudWatch alarm for EC2 CPU utilization
    
    Args:
        instance_id (str): EC2 instance ID to monitor
        sns_topic_arn (str, optional): SNS topic ARN for alarm notifications
        cpu_threshold (float, optional): CPU threshold percentage to trigger alarm. Defaults to 70.0
    """
    try:
        # Create alarm name
        alarm_name = f'CPU_Utilization_{instance_id}'
        
        # Define alarm configuration
        alarm_config = {
            'AlarmName': alarm_name,
            'MetricName': 'CPUUtilization',
            'Namespace': 'AWS/EC2',
            'Statistic': 'Average',
            'Period': 300,  # 5 minutes
            'EvaluationPeriods': 1,
            'Threshold': cpu_threshold,
            'ComparisonOperator': 'GreaterThanThreshold',
            'Dimensions': [
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                }
            ],
            'ActionsEnabled': True,
            'TreatMissingData': 'missing'
        }
        
        # Add SNS notification if provided
        if sns_topic_arn:
            alarm_config['AlarmActions'] = [sns_topic_arn]
            alarm_config['InsufficientDataActions'] = [sns_topic_arn]
            
        # Create the alarm
        response = cloudwatch.put_metric_alarm(**alarm_config)
        
        print(f"CloudWatch alarm '{alarm_name}' created for instance {instance_id}")
        print(f"Alarm will trigger when CPU exceeds {cpu_threshold}% for 5 minutes")
        
        if sns_topic_arn:
            print(f"Notifications will be sent to SNS topic: {sns_topic_arn}")
        else:
            print("No SNS topic configured for notifications")
            
        return True
        
    except Exception as e:
        print(f"Error creating CloudWatch alarm: {e}")
        return False

# Example usage - replace with your values
instance_id = 'i-1234567890abcdef0'
sns_topic_arn = 'arn:aws:sns:us-east-1:123456789012:my-topic'  # Replace or set to None if not using SNS

# Create alarm with default 70% threshold
create_cloudwatch_alarm(instance_id, sns_topic_arn)

# Or create with custom threshold
# create_cloudwatch_alarm(instance_id, sns_topic_arn, cpu_threshold=80.0)