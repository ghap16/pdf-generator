"""Schemas."""

from pydantic import BaseModel


class GeneratePDF(BaseModel):
    """
    GeneratePDF class contain data for generate pdf file

    Attributes
    ----------
    template_name: str
        This the template name in s3
    data: dict
        This is a data dictionary, it is used to render to the pdf file
    """

    template_name: str
    data: dict
