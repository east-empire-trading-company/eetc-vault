from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

from google_sheets import GoogleSheetsClient
from local_settings import GCP_SHEETS_CRED, GCP_SHEETS_SCOPE  # replace with your own Google Cloud Platform credentials

app = Flask(__name__)


@app.route("/api/config/fetch_from_google_sheets", methods=["POST"])
def fetch_from_google_sheets() -> Response:
    """
    Function represents REST API endpoint for fetching data from a specified Google Spreadsheet.
    It receives a POST request to an API endpoint called /api/config/fetch_from_google_sheets using
    :google_sheets.GoogleSheetsClient.get_all_sheets_as_dicts: method.

    :return: Flask Response object.
    """

    spreadsheet_id = request.json["spreadsheet_id"]
    sheet_names = request.json["sheet_names"]

    google_sheets_client = GoogleSheetsClient(
        creds=GCP_SHEETS_CRED,
        scope=GCP_SHEETS_SCOPE,
    )

    sheet_names_dict = {}
    for sheet_name in sheet_names:
        sheet_names_dict.update(google_sheets_client.get_all_sheets_as_dicts(spreadsheet_id, sheet_name))

    return jsonify(sheet_names_dict)
