import unittest
from unittest.mock import MagicMock

import main


class TestGeneratePdfMixin(unittest.TestCase):
    def test_is_the_body_empty_without_empty_body(self):
        result = main.GeneratePDFHandlerMixin.is_the_body_empty("not empty")

        self.assertFalse(result)

    def test_is_the_body_empty_with_empty_body(self):
        main.GeneratePDFHandlerMixin.set_status = MagicMock()
        main.GeneratePDFHandlerMixin.write = MagicMock()

        result = main.GeneratePDFHandlerMixin.is_the_body_empty(None)

        self.assertTrue(result)

        delattr(main.GeneratePDFHandlerMixin, "set_status")
        delattr(main.GeneratePDFHandlerMixin, "write")

    def test_generate_the_pdf_from_body(self):
        result = main.GeneratePDFHandlerMixin.generate_the_pdf_from_body(
            "Hello, World!"
        )

        self.assertIsInstance(result, bytes)
