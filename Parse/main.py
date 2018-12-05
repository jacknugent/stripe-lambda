from __future__ import print_function
import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import logging

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# def resize_image(image_path, resized_path):
#     with Image.open(image_path) as image:
#         if image.format == "png":
#                 print("png found")
#                 convert = Image.new("RGB", image.size, (255,255,255))
#                 convert.paste(image, (0,0), image)
#                 convert.save(resized_path.replace("png", "jpg"), quality=95)
#         else:
#                 image.save(resized_path)
#conversion currently does not work, need to test locally

     
def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)
                     
def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name'] #stripes-in-film
        key = record['s3']['object']['key'] #test-image.jpg
        
        response = s3.head_object(Bucket=bucket, Key=key)

        logger.info('Response: {}'.format(response))

        print(response['Metadata']) #contains all the metadata
        
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key) #/tmp/f62fc7ef-10e0-4a49-81e6-6827e663e62dtest_image.jpg
        upload_path = '/tmp/resized-{}'.format(key) #/tmp/resized-test_image.jpg
        s3.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        s3.upload_file(upload_path, bucket.replace('submitted', 'clean'), key)