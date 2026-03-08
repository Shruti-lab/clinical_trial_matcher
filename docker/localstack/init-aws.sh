#!/bin/bash

# LocalStack AWS Services Initialization Script for Clinical Trial Matcher

echo "Initializing LocalStack AWS services..."

# Set AWS CLI to use LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=ap-south-1

# Wait for LocalStack to be ready
echo "Waiting for LocalStack to be ready..."
until curl -s http://localhost:4566/_localstack/health | grep -q '"s3": "available"'; do
  echo "Waiting for LocalStack services..."
  sleep 2
done

echo "LocalStack is ready. Initializing services..."

# Create S3 bucket for document storage
echo "Creating S3 bucket..."
awslocal s3 mb s3://trialmatch-documents
awslocal s3api put-bucket-cors --bucket trialmatch-documents --cors-configuration '{
  "CORSRules": [
    {
      "AllowedOrigins": ["http://localhost:3000", "http://localhost:5173"],
      "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}'

# Create OpenSearch domain
echo "Creating OpenSearch domain..."
awslocal opensearch create-domain \
  --domain-name trialmatch-search \
  --elasticsearch-version 7.10 \
  --elasticsearch-cluster-config InstanceType=t3.small.search,InstanceCount=1 \
  --ebs-options EBSEnabled=true,VolumeType=gp2,VolumeSize=10

# Create sample Lambda function for document processing
echo "Creating Lambda function..."
cat > /tmp/lambda_function.py << 'EOF'
import json
import boto3

def lambda_handler(event, context):
    print(f"Processing document: {json.dumps(event)}")
    
    # Mock document processing
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Document processed successfully',
            'extracted_text': 'Sample extracted text from document',
            'entities': [
                {'type': 'CONDITION', 'text': 'Diabetes', 'confidence': 0.95},
                {'type': 'MEDICATION', 'text': 'Metformin', 'confidence': 0.89}
            ]
        })
    }
EOF

# Create deployment package
cd /tmp
zip lambda_function.zip lambda_function.py

# Create Lambda function
awslocal lambda create-function \
  --function-name document-processor \
  --runtime python3.9 \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip

# Create API Gateway
echo "Creating API Gateway..."
awslocal apigateway create-rest-api --name trialmatch-api --description "Clinical Trial Matcher API"

# Create IAM role for Lambda (LocalStack doesn't enforce IAM, but good practice)
awslocal iam create-role \
  --role-name lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'

# Create some sample data in S3
echo "Creating sample documents..."
echo "Sample medical report content" | awslocal s3 cp - s3://trialmatch-documents/samples/sample-report.txt
echo "Sample prescription content" | awslocal s3 cp - s3://trialmatch-documents/samples/sample-prescription.txt

echo "LocalStack initialization completed successfully!"
echo "Available services:"
echo "- S3 bucket: trialmatch-documents"
echo "- OpenSearch domain: trialmatch-search"
echo "- Lambda function: document-processor"
echo "- API Gateway: trialmatch-api"
echo ""
echo "Access LocalStack services at: http://localhost:4566"
echo "S3 Web UI: http://localhost:4566/_localstack/s3"