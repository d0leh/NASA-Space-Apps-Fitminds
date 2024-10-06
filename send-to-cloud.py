import boto3
import time
from botocore.exceptions import ClientError

bucket_name = 'muscles-nasa'
file_name = 'exercise.json'  
s3_file_name = 'uploaded_file.json' 

# Initialize a session using Amazon S3
s3 = boto3.client('s3')

def upload_to_s3(file_name, bucket, s3_file_name):
    try:
        s3.upload_file(
            file_name,
            bucket,
            s3_file_name,
            ExtraArgs={'ContentType': 'application/json'}  # Set Content-Type to application/json
        )
        print(f"File {file_name} uploaded to {bucket} as {s3_file_name}")
    except ClientError as e:
        print(f"Error occurred: {e}")
        raise

cnt = 0
while True:
    try:
        upload_to_s3(file_name, bucket_name, s3_file_name)
        time.sleep(5)
        print(cnt)
        cnt += 1 
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)