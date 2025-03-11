import boto3
import datetime
import time

# Create RDS client using default credentials
rds = boto3.client('rds')

def create_rds_snapshot(db_instance_identifier, snapshot_id=None):
    """
    Create a snapshot of an RDS database instance
    
    Args:
        db_instance_identifier (str): ID of the RDS database instance
        snapshot_id (str, optional): ID for the snapshot. Defaults to a timestamped name.
    
    Returns:
        str: The snapshot ID if creation was successful
    """
    try:
        # Create a timestamp-based snapshot ID if none provided
        if not snapshot_id:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            snapshot_id = f"{db_instance_identifier}-{timestamp}"
        
        # Create the snapshot
        print(f"Creating snapshot {snapshot_id} for database {db_instance_identifier}...")
        response = rds.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_id,
            DBInstanceIdentifier=db_instance_identifier
        )
        
        # Wait for the snapshot to complete
        print("Waiting for snapshot to complete... (This may take a while)")
        waiter = rds.get_waiter('db_snapshot_available')
        waiter.wait(
            DBSnapshotIdentifier=snapshot_id,
            WaiterConfig={
                'Delay': 30,  # Check every 30 seconds
                'MaxAttempts': 60  # Wait up to 30 minutes
            }
        )
        
        print(f"Snapshot {snapshot_id} created successfully for {db_instance_identifier}")
        return snapshot_id
        
    except rds.exceptions.DBSnapshotAlreadyExistsFault:
        print(f"Error: Snapshot {snapshot_id} already exists.")
    except Exception as e:
        print(f"Error creating snapshot: {e}")

# Example usage - replace with your database instance ID
db_instance_id = 'my-db-instance'

# Create snapshot with auto-generated name
create_rds_snapshot(db_instance_id)

# Or specify a custom snapshot name
# create_rds_snapshot(db_instance_id, 'my-custom-snapshot-name')