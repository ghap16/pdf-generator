"""Handlers."""

import logging
from http import HTTPStatus
from typing import AnyStr

from fastapi import HTTPException
from jinja2 import Environment, TemplateError
from weasyprint import HTML

from .ports import S3Client
from .schemas import GeneratePDF


class PdfGeneratorHandler:
    """Handler to Generate a Pdf file

    Parameters
    ----------
    pdf_data: GeneratePDF
        The pdf_data contains the name of the template and
        the data of the pdf file.

    Attributtes
    -----------
    template_name: str
        This is where the template name is stored.
    data: dict
        This is data to render to PDF file.
    env: Enviroment instance
        This is an instance of the Jinja2 environment,
        is used to render the html template
        Read more: https://jinja.palletsprojects.com/en/3.1.x/api/#basics
    """

    def __init__(self, pdf_data: GeneratePDF):
        self.template_name = pdf_data.template_name
        self.data = pdf_data.data or {}
        self.env = Environment()
        self.s3_client = S3Client()

    def get_template_str(self) -> AnyStr:
        """Get the template from s3 in aws.

        Returns
        -------
        Template: AnyStr
        """
        return self.s3_client.read_object(self.template_name).decode("utf-8")

    def render(self) -> AnyStr:
        """Render template with data

        Raises
        ------
        TemplateError:
            When the html is wrong,
            read more:
            https://jinja.palletsprojects.com/en/3.1.x/api/#exceptions

        Returns
        -------
        Templaten rendering: AnyStr
        """
        try:
            return self.env.from_string(self.get_template_str()).render(
                **self.data
            )
        except TemplateError as error:
            logging.error(
                f"Error rendering {self.template_name} object: {error}",
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error rendering {self.template_name} object",
            )

    def build(self) -> bytes:
        """Build a PDF document
        Returns
        -------
        Pdf file: bytes
        """
        return HTML(string=self.render()).write_pdf()
