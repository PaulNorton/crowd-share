#
# csaws
# Paul Norton
#

### Imports ###
import boto3
from datetime import datetime

### CSAws - Custom Class ###
# Accesses the AWS API
class CSAws():
    def __init__(self, aws_access_key_id, aws_secret_access_key, hashtag):
        self.s3 = boto3.resource('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
        self.bucket_name = self.build_bucket_name(hashtag, datetime.now())
        self.bucket = self.s3.create_bucket(Bucket=self.bucket_name)

    # retrieve_from_aws: get image from AWS
    def retrieve_from_aws(self, key):
        object = self.s3.Object(self.bucket_name,key)
        return object.get()['Body'].read()
    
    # build_bucket_name: helper method to create name for S3 bucket
    def build_bucket_name(self, hashtag, date):
        date_str = str(date).replace(' ', '-').replace(':', '-').split('.')[0]
        return hashtag + '-' + date_str

    def post_to_aws(self, file_name, bytes):
        self.bucket.put_object(Key=file_name, Body=bytes)