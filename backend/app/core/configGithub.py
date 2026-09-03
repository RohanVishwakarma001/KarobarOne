import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SHIPROCKET_EMAIL = os.getenv("SHIPROCKET_EMAIL")
SHIPROCKET_PASSWORD = os.getenv("SHIPROCKET_PASSWORD")
SHIPROCKET_BASE_URL = os.getenv("SHIPROCKET_BASE_URL", "https://apiv2.shiprocket.in/v1/external")

# Shared secret configured in the Shiprocket dashboard's webhook settings,
# sent back on every tracking-update POST — see shiprocketRouter.py::webhook.
# Confirm the exact header name Shiprocket sends it under for your account
# (some Shiprocket API versions let you pick a custom header name); this
# reads whatever header name the router is wired to check.
SHIPROCKET_WEBHOOK_TOKEN = os.getenv("SHIPROCKET_WEBHOOK_TOKEN")
