import boto3
import logging



# Configure logging
logging.basicConfig(
    filename='logs/deploy.log',  # Logs will be written to this file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_s3_bucket(bucket_name, region='us-east-1'):
    """Creates an S3 bucket in the specified region."""
    client = boto3.client('s3', region_name=region)
    try:
        if region == 'us-east-1':
            response = client.create_bucket(Bucket=bucket_name)
        else:
            response = client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        logging.info(f"Bucket {bucket_name} created successfully in {region}!")
        return response
    except Exception as e:
        logging.error(f"Error creating bucket: {e}")

def upload_file_to_bucket(bucket_name, file_path, object_name=None):
    """Uploads a file to the specified S3 bucket."""
    if object_name is None:
        object_name = file_path
    client = boto3.client('s3')
    try:
        client.upload_file(file_path, bucket_name, object_name)
        logging.info(f"File {file_path} uploaded to bucket {bucket_name} as {object_name}.")
    except Exception as e:
        logging.error(f"Error uploading file: {e}")

if __name__ == "__main__":
    # Specify your bucket name and file to upload
    bucket_name = "my-infra-automation-bucket"
    region = "us-east-1"
    file_path = "example.txt"  # Replace with your file's path

    # Create the bucket and upload a file
    create_s3_bucket(bucket_name, region)
    upload_file_to_bucket(bucket_name, file_path)

#Testing Error Handling
bucket_name = "invalid_bucket_name"  # Invalid bucket name
