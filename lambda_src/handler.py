import io
import os
import uuid
import boto3
from PIL import Image

s3 = boto3.client("s3")


def lambda_handler(event, context):
    destination_bucket = os.environ["DESTINATION_BUCKET"]

    for record in event["Records"]:
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = record["s3"]["object"]["key"]

        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        image_data = response["Body"].read()

        image = Image.open(io.BytesIO(image_data))
        if image.mode != "RGB":
            image = image.convert("RGB")

        pdf_buffer = io.BytesIO()
        image.save(pdf_buffer, format="PDF")
        pdf_buffer.seek(0)

        new_key = f"{uuid.uuid4()}.pdf"

        s3.put_object(
            Bucket=destination_bucket,
            Key=new_key,
            Body=pdf_buffer.getvalue(),
            ContentType="application/pdf"
        )

    return {"statusCode": 200}
