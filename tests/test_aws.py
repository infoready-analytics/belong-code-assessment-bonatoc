import tempfile
from pathlib import Path

import boto3
from moto import mock_s3


@mock_s3
def test_s3():
    s3 = boto3.client("s3", region_name="us-east-1")

    # test create bucket
    s3.create_bucket(Bucket="test-bucket")
    s3_resource = boto3.resource("s3")
    assert s3_resource.Bucket("test-bucket") in s3_resource.buckets.all()

    # test upload to bucket
    s3.put_object(Bucket="test-bucket", Key="test_stats.json", Body="")
    assert isinstance(s3.head_object(Bucket="test-bucket", Key="test_stats.json"), dict)

    # test download from bucket
    with tempfile.NamedTemporaryFile() as tmp:
        s3_resource.Bucket("test-bucket").download_file("test_stats.json", tmp.name)
        assert Path(tmp.name).exists()

    # test delete bucket
    bucket = s3_resource.Bucket("test-bucket")
    bucket.objects.all().delete()
    s3.delete_bucket(Bucket="test-bucket")
    assert s3_resource.Bucket("test-bucket") not in s3_resource.buckets.all()
