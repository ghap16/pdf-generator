"""Settings."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    The Setting class sets the initial settings for the project.

    Attributtes
    -----------
    stage: str
        This is the stage we use to run the project.
    bucket_name: str
        This is the name of the bucket where the html template files
        are stored in s3
    """

    stage: str = "dev"
    region_name: str = "us-east-1"
    bucket_name: str = "accounts-service-dev-contract-templates"


settings = Settings()
