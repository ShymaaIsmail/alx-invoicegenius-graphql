from django.test import TestCase
from ai_parser.utils import parse_invoice_text

class AIParserTest(TestCase):
    def test_parse_invoice_text(self):
        sample = "Invoice Number: 12345\nVendor: ACME\nTotal: $250.00"
        parsed = parse_invoice_text(sample)
        self.assertEqual(parsed.get("invoice_number"), "12345")
        self.assertEqual(parsed.get("vendor_name"), "ACME") 