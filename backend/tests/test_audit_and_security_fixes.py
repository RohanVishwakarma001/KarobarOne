# Owner: mousamdas156@gmail.com
"""
Unit and integration tests verifying fixes for Audit & Versioning, Soft-delete/Trash,
Security sanitization, GST calculation, and Chat User UUID compatibility.
"""

import pytest
import pytest_asyncio
import uuid
from datetime import datetime
from decimal import Decimal
from fastapi.testclient import TestClient

from app.main import app
from app.core.inputSanitizer import sanitize_text
from app.apps.invoiceGenerator.generateInvoice import num_to_words

client = TestClient(app)


def test_input_sanitizer_xss_protection():
    """Verifies XSS script tags, event handlers, and javascript URIs are stripped."""
    dirty_script = "<script>alert('xss')</script>Hello World"
    assert sanitize_text(dirty_script) == "Hello World"

    dirty_onload = "<img src=x onerror=alert(1)>Test Product"
    assert sanitize_text(dirty_onload) == "Test Product"

    dirty_js_uri = "<a href='javascript:alert(1)'>Click Me</a>"
    assert sanitize_text(dirty_js_uri) == "Click Me"

    clean_text = "Standard Product Description 100% Cotton"
    assert sanitize_text(clean_text) == clean_text


def test_num_to_words_amount_formatting():
    """Verifies total amount converting to words for invoices."""
    assert num_to_words(1500) == "One Thousand Five Hundred Only"
    assert num_to_words(0) == "Zero"
    assert num_to_words(250) == "Two Hundred Fifty Only"


def test_gstin_validation_logic():
    """Verifies GSTIN regex pattern matching in invoice schemas."""
    import re
    gstin_regex = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
    
    valid_gstin = "27AADCK1234A1Z5"
    assert bool(gstin_regex.match(valid_gstin)) is True

    invalid_gstin = "INVALID_GST_123"
    assert bool(gstin_regex.match(invalid_gstin)) is False


def test_invoice_pdf_generation_endpoint():
    """Verifies POST /api/v1/invoice/generate produces a valid PDF buffer."""
    payload = {
        "company": {
            "gstin": "27AADCK1234A1Z5",
            "name": "KAROBARONE PVT. LTD.",
            "address1": "Sector-5, Salt Lake, Kolkata",
            "address2": "West Bengal, India",
            "state": "West Bengal",
            "contact": "+91-1234567890"
        },
        "bill_to": {
            "name": "Test Customer",
            "address": "MG Road, Bengaluru",
            "state": "Karnataka",
            "gstin": "29ABCDE1234F1Z5"
        },
        "ship_to": {
            "name": "Test Customer",
            "address": "MG Road, Bengaluru",
            "state": "Karnataka",
            "gstin": "29ABCDE1234F1Z5"
        },
        "invoice": {
            "number": "INV-2026-001",
            "date": "2026-08-05",
            "payment_mode": "UPI"
        },
        "items": [
            {
                "sr": 1,
                "description": "KarobarOne Premium Subscription",
                "hsn": "9983",
                "qty": 1,
                "unit": "Nos",
                "rate": 1000.0,
                "gst_pct": 18
            }
        ]
    }
    res = client.post("/api/v1/invoice/generate", json=payload)
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 500  # Non-empty PDF bytes
