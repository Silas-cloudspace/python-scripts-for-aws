import boto3

def cleanup_snapshots():
    # Get all regions
    ec2 = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    
    # Track total deleted snapshots
    total_deleted = 0
    
    # Process each region
    for region in regions:
        print(f"Cleaning up snapshots in {region}")
        ec2 = boto3.client('ec2', region_name=region)
        
        try:
            # Get all snapshots owned by the account
            response = ec2.describe_snapshots(OwnerIds=['self'])
            snapshots = response['Snapshots']
            region_count = 0
            
            # Delete each snapshot
            for snapshot in snapshots:
                try:
                    print(f"Deleting snapshot {snapshot['SnapshotId']}")
                    ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    region_count += 1
                    total_deleted += 1
                except Exception as e:
                    print(f"Error deleting snapshot {snapshot['SnapshotId']}: {e}")
            
            print(f"Deleted {region_count} snapshots in {region}")
        except Exception as e:
            print(f"Error processing region {region}: {e}")
    
    print(f"Total snapshots deleted across all regions: {total_deleted}")

if __name__ == '__main__':
    cleanup_snapshots()