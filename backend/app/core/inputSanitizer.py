# Owner: mousamdas156@gmail.com
"""
Input sanitization utility for preventing Cross-Site Scripting (XSS)
and dangerous HTML injection attacks.
"""

import re

# Dangerous tags and attributes patterns
HTML_TAG_PATTERN = re.compile(r"<[^>]*?>")
SCRIPT_TAG_PATTERN = re.compile(r"<script.*?>.*?</script>", re.DOTALL | re.IGNORECASE)
EVENT_HANDLER_PATTERN = re.compile(r"on\w+\s*=", re.IGNORECASE)
JAVASCRIPT_URI_PATTERN = re.compile(r"javascript:\s*", re.IGNORECASE)


def sanitize_text(text: str | None) -> str | None:
    """
    Strips raw HTML tags and dangerous script elements from user text inputs.
    """
    if not text or not isinstance(text, str):
        return text

    # Remove script tags and content
    cleaned = SCRIPT_TAG_PATTERN.sub("", text)
    # Remove javascript: URIs
    cleaned = JAVASCRIPT_URI_PATTERN.sub("", cleaned)
    # Remove event handlers like onerror=, onload=
    cleaned = EVENT_HANDLER_PATTERN.sub("", cleaned)
    # Remove remaining HTML tags
    cleaned = HTML_TAG_PATTERN.sub("", cleaned)

    return cleaned.strip()
