from pathlib import Path
from urllib.request import urlopen

import boto3


def is_ec2_instance(timeout=5):
    """Check if an instance is running on AWS.
    https://stackoverflow.com/questions/29573081/check-if-python-script-is-running-on-an-aws-instance
    """
    result = False
    meta = "http://169.254.169.254/latest/meta-data/public-ipv4"
    try:
        result = urlopen(meta, None, timeout=timeout).status == 200
    except Exception as e:
        return result

    return result


def upload_to_s3(filepath, bucket_name):
    """Upload a file to an S3 bucket.

    Args:
        filepath (str or pathlib.Path): File to upload.
        bucket_name (str): Name of the bucket to upload the file to.

    Returns:
        bool: Success or failure.
    """

    if is_ec2_instance():
        try:
            s3 = boto3.client("s3")
            s3.upload_file(str(filepath), bucket_name, Path(filepath).name)

            return True
        except:
            pass

    return False
