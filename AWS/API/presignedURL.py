import logging
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = 'handboll-ai-coach'
EXPIRATION = 3600

def decorator(func):
    def wrapper(*args, **kwargs):
        response = {}
        response['url'] = func(*args, **kwargs)
        response['filename'] = kwargs['filename']
        response['mode'] = kwargs['mode']
        response['expiration'] =  EXPIRATION
        response['bucket_name'] =  BUCKET_NAME
        return response
    return wrapper

@decorator
def presignedURL(filename: str, mode: str) -> str:
    """Generate a presigned URL to get/post an S3 object

    Parameters
    ----------
        filename: str
            Name of the file
        mode: str
            Type of operation (get_object or put_object)
    
    Returns
    -------
        presigned_URL: str
            Presigned url for AWS S3 bucket object
    """

    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(mode,
                                                    Params={'Bucket': BUCKET_NAME,
                                                            'Key': filename},
                                                    ExpiresIn=EXPIRATION)
    except ClientError as e:
        logging.error(e)
        return None

    return response



presignedURL(filename='index.html', mode='get_object')