Infrastructure Automation Project
Automates AWS infrastructure deployment using Python and Boto3.
Features

Automated AWS S3 bucket deployment
File upload automation
CloudFormation template validation

Technologies

Python
AWS S3
Boto3

Prerequisites

Install Python and Boto3:
bashCopypip install boto3

Configure AWS CLI:
bashCopyaws configure
You'll need:

AWS Access Key ID
AWS Secret Access Key
Default Region


CloudFormation Template:
yamlCopyAWSTemplateFormatVersion: '2010-09-09'
Description: CloudFormation template to create an S3 bucket
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-infra-automation-bucket

Test file (example.txt) for S3 upload

Installation
bashCopygit clone <your-repo-url>
cd InfrastructureAutomation
Usage
Run the deployment script:
bashCopypython src/deploy.py
Example Output
Copy2024-12-02 12:00:00,000 - INFO - Validating CloudFormation template
2024-12-02 12:00:01,000 - INFO - Template validated successfully
2024-12-02 12:00:02,000 - INFO - Creating S3 bucket
2024-12-02 12:00:03,000 - INFO - Bucket created successfully
2024-12-02 12:00:04,000 - INFO - Uploading file
2024-12-02 12:00:05,000 - INFO - File uploaded successfully
Future Enhancements

Additional AWS service automation
Resource cleanup functionality
Parameterized bucket names for different environments

License
This project is open-source and available for educational purposes.
