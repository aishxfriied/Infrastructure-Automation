import boto3

def create_s3_bucket(bucket_name):
    """Creates an S3 bucket in the specified region."""
    client = boto3.client('s3')
    try:
        response = client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully!")
        return response
    except Exception as e:
        print(f"Error creating bucket: {e}")

if __name__ == "__main__":
    # Define your S3 bucket name here
    bucket_name = "my-infra-automation-bucket"
    create_s3_bucket(bucket_name)
