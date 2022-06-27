"""Test"""

from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.main import app


class TestGeneratePdf(TestCase):
    """Test Pdf generator

    Attributtes
    -----------
    client: boto3.client
        A low-level client representing Amazon Simple Storage Service (S3)
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
    payload: dict
        Data to send to create pdf file
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = TestClient(app)
        self.payload = {
            "template_name": "template_name_example",
            "data": {
                "title": "Title example",
                "message": "This is a message example",
                "items": ["Item 1", "Item 2", "Item 3"],
            },
        }

    @patch("src.ports.S3Client.read_object")
    def test_generate_a_pdf(self, mock_read_object):
        """Assert that generate a pdf file sucessfully"""
        mock_read_object.return_value = """<html>
        <head></head>
        <body>
        <h1>{{title}}</h1>
        <p>{{message}}</p>
        <ul>
            {% for item in items %}
                <li>{{item}}</li>
            {% endfor %}
        </ul>
        </body>
        </html>""".encode()

        response = self.client.post("/", json=self.payload)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.payload["data"]["title"], response.text)
        mock_read_object.assert_called_with("template_name_example")

    @patch("src.ports.S3Client.read_object")
    def test_generate_a_pdf_with_wrong_template(self, mock_read_object):
        """Assert that it fails if the template is wrong"""
        mock_read_object.return_value = """<html>
        <head></head>
        <body>
        <h1>{{title}</h1>
        <p>{{message}}</p>
        <ul>
            {% for item in items }
                <li>{{item}</li>
            {% endfor %}
        </ul>
        </body>
        </html>""".encode()

        response = self.client.post("/", json=self.payload)
        self.assertEqual(
            response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR
        )
        self.assertEqual(
            response.json()["detail"],
            f"Error rendering {self.payload['template_name']} object",
        )
        mock_read_object.assert_called_with("template_name_example")

    @patch("src.ports.S3Client.read_object")
    def test_generate_a_pdf_with_template_failed(self, mock_read_object):
        """assert a 502 error if there is a problem with the s3 client"""
        mock_read_object.side_effect = HTTPException(
            HTTPStatus.BAD_GATEWAY,
            f"Error reading {self.payload['template_name']} object from AWS",
        )

        response = self.client.post("/", json=self.payload)
        self.assertEqual(response.status_code, HTTPStatus.BAD_GATEWAY)
        self.assertEqual(
            response.json()["detail"],
            f"Error reading {self.payload['template_name']} object from AWS",
        )
        mock_read_object.assert_called_with("template_name_example")
