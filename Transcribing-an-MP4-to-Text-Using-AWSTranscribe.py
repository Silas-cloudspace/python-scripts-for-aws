import boto3
import time

# Replace with your S3 bucket name
BUCKET_NAME = 'your-bucket-name'

# Replace with the name of the input video file in your S3 bucket
VIDEO_FILE_NAME = 'your-video-file.mp4'

# Replace with the name of the output transcript file in your S3 bucket
TRANSCRIPT_FILE_NAME = 'transcribed'

# Create a Transcribe client using default credentials
transcribe_client = boto3.client('transcribe')

# Generate a unique job name using timestamp
job_name = f'transcription_job_{int(time.time())}'

# Start the transcription job
transcription_job = transcribe_client.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': f's3://{BUCKET_NAME}/{VIDEO_FILE_NAME}'},
    MediaFormat='mp4',  # Change this based on your video format (mp4, mp3, wav, etc.)
    LanguageCode='en-US',
    OutputBucketName=BUCKET_NAME,
    OutputKey=TRANSCRIPT_FILE_NAME
)

print(f"Started transcription job: {job_name}")

# Wait for the transcription job to complete
print("Waiting for transcription to complete...")
while True:
    job = transcribe_client.get_transcription_job(
        TranscriptionJobName=job_name
    )
    status = job['TranscriptionJob']['TranscriptionJobStatus']
    
    print(f"Current status: {status}")
    
    if status in ['COMPLETED', 'FAILED']:
        break
    
    # Wait 30 seconds before checking again
    time.sleep(30)

# Print the final transcription job status and output URL
if status == 'COMPLETED':
    print("\nTranscription completed successfully!")
    print(f"Transcript URL: {job['TranscriptionJob']['Transcript']['TranscriptFileUri']}")
    print(f"Transcript saved to: s3://{BUCKET_NAME}/{TRANSCRIPT_FILE_NAME}")
else:
    print("\nTranscription failed.")
    if 'FailureReason' in job['TranscriptionJob']:
        print(f"Reason: {job['TranscriptionJob']['FailureReason']}")