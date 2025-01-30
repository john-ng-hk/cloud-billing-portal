#!/bin/bash

# Build the SAM application
sam build

# Deploy the SAM application
sam deploy

# Update Frontend scripts with Cloudformation Outputs

# Retrieve CloudFormation outputs
outputs=$(aws cloudformation describe-stacks --stack-name sam-CloudBillingPortal --query "Stacks[0].Outputs")

# Extract outputs
region=$(echo $outputs | jq -r '.[] | select(.OutputKey=="Region") | .OutputValue')
userPoolId=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalUserpool") | .OutputValue')
clientId=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalUserpoolClient") | .OutputValue')
identityPoolId=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalIdentityPool") | .OutputValue')
frontendBucket=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalFrontendBucketName") | .OutputValue')
backendBucket=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalBackendBucketName") | .OutputValue')
apiGW=$(echo $outputs | jq -r '.[] | select(.OutputKey=="CloudBillingPortalAPIGateway") | .OutputValue')

# Change directory to frontend bucket folder
cd CloudBillingPortalFrontendBucket

# Create a temporary JavaScript file with multiple lines
cat <<EOL > temp.js
const region = '$region';
const userPoolId = '$userPoolId';
const clientId = '$clientId';
const identityPoolId = '$identityPoolId';
EOL

# Append the existing JavaScript file to the temporary file
cat aws-cognito.js >> temp.js

# Replace the original JavaScript file with the temporary file
mv temp.js aws-cognito.js

# Create a temporary JavaScript file with multiple lines
cat <<EOL > temp.js
const backendBucket = '$backendBucket';
EOL

# Append the existing JavaScript file to the temporary file
cat file-upload.js >> temp.js

# Replace the original JavaScript file with the temporary file
mv temp.js file-upload.js

# Create a temporary JavaScript file with multiple lines
cat <<EOL > temp.js
const apiGW = '$apiGW';
EOL

# Append the existing JavaScript file to the temporary file
cat additional-info.js >> temp.js

# Replace the original JavaScript file with the temporary file
mv temp.js additional-info.js

# Copy the folder content to the S3 bucket
aws s3 cp . s3://$frontendBucket --recursive

# remove the added outputs
sed '1,4d' aws-cognito.js > temp.js
mv temp.js aws-cognito.js

sed '1,1d' file-upload.js > temp.js
mv temp.js file-upload.js

sed '1,1d' additional-info.js > temp.js
mv temp.js additional-info.js