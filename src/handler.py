import os

from athena.federation.lambda_handler import AthenaLambdaHandler

from athena_gsheets import GoogleSheetsDataSource

# This needs to be a valid bucket that the Lambda function role has access to
SPILL_BUCKET = os.getenv("TARGET_BUCKET")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

example_handler = AthenaLambdaHandler(
    data_source=GoogleSheetsDataSource(SHEET_ID), spill_bucket=SPILL_BUCKET
)


def lambda_handler(event, context):
    # For debugging purposes, we print both the event and the response :)
    print(event)
    response = example_handler.process_event(event)
    print(response)

    return response
