# Athena Google Sheets Example

An example of using the [Unofficial Athena Query Federation Python SDK](https://github.com/dacort/athena-federation-python-sdk/) to query data from a Google Sheet!

## Overview

This is a little bit of a hard-coded example, but it shows how to query Google Sheets data using Amazon Athena.

## How to use

- Go to the Google Developer Console and enable the Google Sheets API and create an API key
- Follow the instructions in the [Python SDK](https://github.com/dacort/athena-federation-python-sdk#creating-your-lambda-function) repo for building the Docker image and creating your Lambda function.
- Update `athena_gsheets.py` with your desired sheet name (`All` in my case)
- Provide your desired sheet ID and API key as environment variables to your Lambda function

```shell
aws lambda create-function \
    --function-name athena-gsheets \
    --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/athena-example-execution-role \
    --code ImageUri=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/athena_gsheets:${IMAGE_TAG} \
    --environment 'Variables={TARGET_BUCKET=<S3_BUCKET_NAME>,GOOGLE_SHEET_API_KEY=<API_KEY>,GOOGLE_SHEET_ID=<SHEET_ID>}' \
    --description "Athena GSheet Example" \
    --timeout 60 \
    --package-type Image
```
