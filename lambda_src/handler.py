import datetime
import logging
import os
import urllib.parse

import boto3
import img2pdf

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")


def build_destination_key(source_key, now=None):
    now = now or datetime.datetime.utcnow()
    base = os.path.basename(source_key)
    stem, _ext = os.path.splitext(base)
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}_{stem}.pdf"


def lambda_handler(event, context):
    destination_bucket = os.environ["DESTINATION_BUCKET"]

    for record in event.get("Records", []):
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        if source_key.lower().endswith(".pdf"):
            logger.info("Skipping PDF input: %s", source_key)
            continue

        logger.info("Converting s3://%s/%s", source_bucket, source_key)
        image_data = s3.get_object(Bucket=source_bucket, Key=source_key)["Body"].read()
        pdf_bytes = img2pdf.convert(image_data)

        dest_key = build_destination_key(source_key)
        s3.put_object(
            Bucket=destination_bucket,
            Key=dest_key,
            Body=pdf_bytes,
            ContentType="application/pdf",
        )
        logger.info("Wrote s3://%s/%s", destination_bucket, dest_key)

    return {"statusCode": 200}
