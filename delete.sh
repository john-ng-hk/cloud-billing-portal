#!/bin/bash

# Retrieve CloudFormation outputs
outputs=$(aws cloudformation describe-stacks --stack-name sam-CloudBillingPortal --query "Stacks[0].Outputs")

# Extract outputs
frontendBucket=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalFrontendBucketName") | .OutputValue')
backendBucket=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalBackendBucketName") | .OutputValue')

# Delete all objects in the bucket
aws s3 rm s3://$frontendBucket --recursive
aws s3 rm s3://$backendBucket --recursive

# Delete stack
sam delete