from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

import settings
from google_sheets import GoogleSheetsClient

app = Flask(__name__)


@app.route("/api/config/fetch_from_google_sheets", methods=["POST"])
def fetch_from_google_sheets() -> Response:
    """
    Function represents a REST API endpoint /api/config/fetch_from_google_sheets
    for fetching data from a specified Google Spreadsheet. Using
    :google_sheets.GoogleSheetsClient.get_all_sheets_as_dicts: method, it gets
    the contents of the Spreadsheet and returns it as a JSON response.

    :return: Flask Response object.
    """

    spreadsheet_id = request.json["spreadsheet_id"]
    sheet_names = request.json["sheet_names"]

    google_sheets_client = GoogleSheetsClient(
        creds=settings.GOOGLE_SHEETS_SERVICE_ACC_CREDENTIALS,
        scope=settings.GOOGLE_SHEETS_SCOPE,
    )

    sheet_names_dict = {}
    for sheet_name in sheet_names:
        sheet_names_dict.update(
            google_sheets_client.get_all_sheets_as_dicts(spreadsheet_id, sheet_name)
        )

    return jsonify(sheet_names_dict)
