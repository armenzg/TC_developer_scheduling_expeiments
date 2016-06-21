import os
import boto3

from taskcluster.sync import Auth

BUCKET = 'tc-gp-public-31d'
PREFIX = 'ateam/pulse-action-dev/'


def main():
    # This is to make sure that TASKCLUSTER_CLIENT_ID and
    # TASKCLUSTER_ACCESS_TOKEN are set
    # The client you're referring to should have this in its scopes:
    #     auth:aws-s3:read-write:tc-gp-public-31d/ateam/pulse-action-dev/*
    os.environ['TASKCLUSTER_CLIENT_ID']
    os.environ['TASKCLUSTER_ACCESS_TOKEN']

    # Obtain temporary S3 credentials via TaskCluster's API
    # https://docs.taskcluster.net/reference/platform/auth/api-docs#awsS3Credentials
    credentials = Auth().awsS3Credentials(
        level='read-write',
        bucket=BUCKET,
        prefix=PREFIX,
    )
    url = upload_to_s3(
        credentials=credentials,
        file=open(os.path.join('artifacts', 'hello_world_task.json'), 'r+'),
        bucket=BUCKET,
        prefix=PREFIX + "garbage/",
        region='us-west-2',
    )
    print url


def upload_to_s3(credentials, file, bucket, prefix, region):
    """ Uploads file to the AWS S3 bucket and key specified.
    """
    filepath = file.name
    filename = filepath.split('/')[-1]
    remote_file_path = os.path.join(prefix, filename)

    s3_client = boto3.client(
        service_name='s3',
        region_name=region,
        aws_access_key_id=credentials['credentials']['accessKeyId'],
        aws_secret_access_key=credentials['credentials']['secretAccessKey'],
        aws_session_token=credentials['credentials']['sessionToken'],
    )

    # Upload the file to S3
    # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.upload_file
    s3_client.upload_file(
        Filename=filepath,
        Bucket=bucket,
        Key=remote_file_path)

    # A signed URL allows anyone to grab the file
    # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.generate_presigned_url
    # XXX: It seems that it expires in an hour
    # ExpiresIn (int) -- The number of seconds the presigned url is valid for. By default it
    # expires in an hour (3600 seconds)
    return s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': remote_file_path
        }
    )


if __name__ == "__main__":
    main()
