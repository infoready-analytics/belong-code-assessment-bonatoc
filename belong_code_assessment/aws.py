from urllib.request import urlopen

import boto3


def is_ec2_instance():
    """Check if an instance is running on AWS.
    https://stackoverflow.com/questions/29573081/check-if-python-script-is-running-on-an-aws-instance
    """

    result = False
    meta = "http://169.254.169.254/latest/meta-data/public-ipv4"
    try:
        result = urlopen(meta).status == 200
    except ConnectionError:
        return result
    return result


def upload_to_s3(filepath, bucket_name):
    if is_ec2_instance():
        s3 = boto3.resource("s3")

        if s3.Bucket(bucket_name) in s3.buckets.all():
            s3.put_object(Bucket=bucket_name, Key=filepath, Body="")

            return True

    return False
