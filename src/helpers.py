"""Helpers."""


async def pdf_streamer(pdf_file: bytes):
    """Iterator for pdf_file.

    Parameters
    ----------
    pdf_file: bytes
        This is the Pdf file

    Returns
    -------
    Pdf file fragment: bytes
    """
    for i in range(10):
        yield pdf_file
