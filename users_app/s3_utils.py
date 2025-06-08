import boto3
from botocore.exceptions import ClientError
from django.conf import settings

def s3_file_exists(path: str) -> bool:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=path)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        raise
