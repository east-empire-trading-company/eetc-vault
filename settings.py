import base64
import json
import os


API_KEY = os.getenv("API_KEY")

if os.getenv("GOOGLE_SHEETS_SERVICE_ACC_CREDENTIALS"):
    GOOGLE_SHEETS_SERVICE_ACC_CREDENTIALS = json.loads(
        base64.b64decode(os.getenv("GOOGLE_SHEETS_SERVICE_ACC_CREDENTIALS"))
    )
else:
    # this only happens when running tests
    GOOGLE_SHEETS_SERVICE_ACC_CREDENTIALS = {}

GOOGLE_SHEETS_SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    from local_settings import *
except ImportError:
    pass
