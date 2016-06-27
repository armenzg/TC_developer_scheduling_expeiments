import os
from tc_s3_uploader import TC_S3_Uploader

if __name__ == "__main__":
    uploader = TC_S3_Uploader(bucket_prefix='ateam/pulse-action-dev/')
    file = open(os.path.join('artifacts', 'hello_world_task.json'), 'r+')
    url = uploader.upload(file)
    print url
