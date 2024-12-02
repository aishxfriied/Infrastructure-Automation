import boto3
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/deploy.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

def validate_template(template_file):
    """Validates the CloudFormation template."""
    client = boto3.client('cloudformation')
    with open(template_file, 'r') as file:
        template_body = file.read()
    try:
        response = client.validate_template(TemplateBody=template_body)
        logging.info(f"Template {template_file} validated successfully.")
        return True
    except Exception as e:
        logging.error(f"Error validating template {template_file}: {e}")
        raise

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
        logging.info(f"Bucket '{bucket_name}' created successfully in '{region}'.")
        return response
    except Exception as e:
        logging.error(f"Error creating bucket: {e}")
        raise

def upload_file_to_bucket(bucket_name, file_path):
    """Uploads a file to the specified S3 bucket."""
    client = boto3.client('s3')
    try:
        object_name = os.path.basename(file_path)
        client.upload_file(file_path, bucket_name, object_name)
        logging.info(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise

if __name__ == "__main__":
    logging.info("Starting deployment script...")

    # Specify your bucket name, region, and CloudFormation template
    bucket_name = "my-infra-automation-bucket"
    region = "us-east-1"
    file_path = "example.txt"  # Replace with your file's path
    template_file = "templates/s3_bucket_template.yaml"

    try:
        # Validate the CloudFormation template
        logging.info(f"Validating CloudFormation template: {template_file}")
        validate_template(template_file)

        # Create the S3 bucket
        logging.info(f"Creating S3 bucket: {bucket_name}")
        create_s3_bucket(bucket_name, region)

        # Upload a file to the bucket
        logging.info(f"Uploading file {file_path} to bucket {bucket_name}")
        upload_file_to_bucket(bucket_name, file_path)

        logging.info("Deployment script completed successfully.")
    except Exception as e:
        logging.error(f"Deployment script encountered an error: {e}")
