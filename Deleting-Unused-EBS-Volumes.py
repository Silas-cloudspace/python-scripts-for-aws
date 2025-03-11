import boto3

def get_unused_volumes():
    ec2 = boto3.client('ec2')
    response = ec2.describe_volumes()
    unused_volumes = []
    for volume in response['Volumes']:
        if len(volume['Attachments']) == 0:
            unused_volumes.append(volume['VolumeId'])
    return unused_volumes
  
def delete_volumes(volumes):
    ec2 = boto3.client('ec2')
    for volume in volumes:
        ec2.delete_volume(VolumeId=volume)
        print(f"Deleted volume {volume}")
        
def main():
    unused_volumes = get_unused_volumes()
    print(f"Found {len(unused_volumes)} unused volumes")
    if unused_volumes:
      delete_volumes(unused_volumes)
    else:
      print("No unused volumes found")

if __name__ == '__main__':
    main()