"""Routers"""

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from .handlers import PdfGeneratorHandler
from .helpers import pdf_streamer
from .schemas import GeneratePDF

router = APIRouter()


@router.post("/", response_class=FileResponse)
def generate_pdf(pdf_data: GeneratePDF):
    """Generate a pdf file

    Parameters
    ----------
    pdf_data: GeneratePDF
        The pdf_data contains the name of the template and
        the data of the pdf file.

    Returns
    -------
    Pdf file
    """
    pdf_file = PdfGeneratorHandler(pdf_data).build()
    return StreamingResponse(
        pdf_streamer(pdf_file), media_type="application/pdf"
    )
