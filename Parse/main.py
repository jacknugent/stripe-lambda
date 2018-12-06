from __future__ import print_function
import boto3
import uuid
from PIL import Image
from PIL import ImageChops

s3 = boto3.client('s3')

def resize_image(image_path, resized_path, response):
    """crop/compress image and add it's metadata to dict

    :param image_path: path of the original file
    :param resized_path: path for the cropped/compressed file
    :param response: metadata
    :return: none
    """

    with Image.open(image_path) as image:
        # if a png, convert to a jpg
        if image.format == "PNG":
            image = image.convert('RGB')

        #get black borders and remove them from the image
        bg = Image.new(image.mode, image.size, color=0)
        diff = ImageChops.difference(image, bg)
        bbox = diff.getbbox()
        cropped = image.crop(bbox)

        #save new image size, save image
        response['width'] = str(cropped.size[0])
        response['height'] = str(cropped.size[1])
        cropped.save(resized_path, quality=97)

def handler(event, context):
    """
    move image from stripes-submitted and move to stripes-clean

    :param event: file upload event
    :param context:
    :return: nothing
    """
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        #contains all the metadata
        response = s3.head_object(Bucket=bucket, Key=key)['Metadata']

        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key).replace("png", "jpg")

        s3.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path, response)
        s3.upload_file(upload_path, bucket.replace('submitted', 'clean'), key, ExtraArgs={'Metadata': response})

# resize_image('test.png', 'result.jpg', {})
