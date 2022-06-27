"""Ports"""

import logging
from http import HTTPStatus

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from .config import settings


class S3Client:
    """Port to S3 client

    Attributtes
    -----------
    client: boto3.client
        A low-level client representing Amazon Simple Storage Service (S3)
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
    """

    def __init__(self):
        self.client = boto3.client("s3")

    def get_object(self, file_name: str):
        """Get a file using s3 client.

        Parameters
        ----------
        file_name: str
            This is the file name file in s3

        Raises
        ------
        ClientError:
            When can't get object,
            read more:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
            https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
            https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html

        Returns
        -------
        Stored object
        """
        try:
            obj = self.client.get_object(
                Bucket=settings.bucket_name, Key=file_name
            ).get()
            return obj["Body"]
        except ClientError as error:
            logging.error(
                f"Error reading {file_name} object from AWS: {error}",
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.BAD_GATEWAY,
                detail=f"Error reading {file_name} object from AWS",
            )

    def read_object(self, file_name: str):
        """Read a object.

        Parameters:
        -----------
        file_name: str
            This the file name in s3

        Returns
        -------
        Object read
        """
        return self.get_object(file_name).read()
