import boto3

# Initialize the EC2 client using your default credentials
ec2 = boto3.client('ec2')

# Get all regions
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Track unused IPs we delete
unused_ips = {}

# Check each region for unused Elastic IPs
for region_name in regions:
    try:
        # Create EC2 client for the current region
        ec2conn = boto3.client('ec2', region_name=region_name)
        
        # Get all Elastic IPs in the region
        addresses = ec2conn.describe_addresses(
            Filters=[{"Name": "domain", "Values": ["vpc"]}]
        )["Addresses"]
        
        # Find and release unused Elastic IPs
        for address in addresses:
            if "AssociationId" not in address and address["AllocationId"] not in unused_ips:
                unused_ips[address["AllocationId"]] = region_name
                ec2conn.release_address(AllocationId=address["AllocationId"])
                print(f"Deleted unused Elastic IP {address['PublicIp']} in region {region_name}")
    
    except Exception as e:
        print(f"No access to region {region_name}: {e}")

# Print summary
print(f"Found and deleted {len(unused_ips)} unused Elastic IPs across all regions:")
print(unused_ips)