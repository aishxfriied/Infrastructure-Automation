import boto3
import logging
import os
import unittest

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
        logging.info(f"Template {template_file} validated successfully: {response}")
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
        logging.info(f"Bucket {bucket_name} created successfully in {region}!")
        return response
    except Exception as e:
        logging.error(f"Error creating bucket: {e}")
        raise

def delete_s3_bucket(bucket_name):
    """Deletes all objects in an S3 bucket and the bucket itself."""
    client = boto3.client('s3')
    try:
        # List objects in the bucket
        response = client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                logging.info(f"Deleted object {obj['Key']} from bucket {bucket_name}.")
        
        # Delete the bucket
        client.delete_bucket(Bucket=bucket_name)
        logging.info(f"Bucket {bucket_name} deleted successfully.")
    except Exception as e:
        logging.error(f"Error deleting bucket {bucket_name}: {e}")
        raise

def delete_cloudformation_stack(stack_name):
    """Deletes a CloudFormation stack."""
    client = boto3.client('cloudformation')
    try:
        client.delete_stack(StackName=stack_name)
        logging.info(f"CloudFormation stack {stack_name} deletion initiated.")
    except Exception as e:
        logging.error(f"Error deleting CloudFormation stack {stack_name}: {e}")
        raise

if __name__ == "__main__":
    # Specify your bucket name and stack name
    bucket_name = "my-infra-automation-bucket"
    stack_name = "MyS3BucketStack"

    try:
        # Delete S3 bucket
        logging.info(f"Deleting S3 bucket: {bucket_name}")
        delete_s3_bucket(bucket_name)

        # Delete CloudFormation stack
        logging.info(f"Deleting CloudFormation stack: {stack_name}")
        delete_cloudformation_stack(stack_name)
    except Exception as e:
        logging.error(f"Cleanup script encountered an error: {e}")


if __name__ == "__main__":
    logging.info("Starting deployment script...")

    # Specify your bucket name, region, and CloudFormation template
    bucket_name = "my-infra-automation-bucket"
    region = "us-east-1"
    file_path = "example.txt"  # Replace with your file's path
    template_file = "templates/s3_bucket_template.yaml"
    stack_name = "MyS3BucketStack"

    try:
        # Validate the CloudFormation template
        logging.info(f"Validating CloudFormation template: {template_file}")
        validate_template(template_file)

        # Deploy or update CloudFormation stack
        logging.info(f"Deploying CloudFormation stack: {stack_name}")
        deploy_cloudformation_template(template_file, stack_name)

        # Upload a file to the created bucket
        logging.info(f"Uploading file {file_path} to bucket {bucket_name}")
        upload_file_to_bucket(bucket_name, file_path)

        logging.info("Deployment script completed successfully.")
    except Exception as e:
        logging.error(f"Deployment script encountered an error: {e}")

        response = client.create_stack(
    StackName=stack_name,
    TemplateBody=template_body,
    Parameters=[
        {'ParameterKey': 'BucketName', 'ParameterValue': bucket_name},
        {'ParameterKey': 'EnvironmentTag', 'ParameterValue': 'Development'}
    ],
    Capabilities=['CAPABILITY_NAMED_IAM']
)



from src.deploy import create_s3_bucket, validate_template

class TestDeploy(unittest.TestCase):
    def test_create_s3_bucket(self):
        bucket_name = "test-bucket-for-unit-tests"
        region = "us-east-1"
        response = create_s3_bucket(bucket_name, region)
        self.assertIsNotNone(response)

    def test_validate_template(self):
        template_file = "templates/s3_bucket_template.yaml"
        result = validate_template(template_file)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
