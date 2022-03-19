from flask import Flask, make_response
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


@app.route("/api/config/feature_flags", methods=["GET", "POST"])
def feature_flags_activate() -> Response:
    """
    Function represents a REST API endpoint /api/config/feature_flags.
    In Feature flags sheet, it changes active status (TRUE or FALSE) of the
    feature provided in request.
    Method :google_sheets.GoogleSheetsClient.get_single_sheet_as_dict:
    gets content of the Feature flags sheet.
    Method :google_sheets_client.sheet.values().update: updates Feature flags
    sheet with data provided in the request.

    :return: Flask Response object.
    """

    spreadsheet_id = "1EJzkRzyE-zPY_wffu2D8iECwWsWh2wTIc8cXc56PfQE"
    sheet_name = "Feature flags"

    # Google Sheets API authentication
    google_sheets_client = GoogleSheetsClient(
        creds=settings.GOOGLE_SHEETS_SERVICE_ACC_CREDENTIALS,
        scope=settings.GOOGLE_SHEETS_SCOPE,
    )

    if request.method == "GET":
        return jsonify(
            google_sheets_client.get_single_sheet_as_dict(
                spreadsheet_id=spreadsheet_id, sheet_name=sheet_name
            )
        )
    else:
        # parse request data
        request_data = request.get_json()
        feature = request_data["feature"]
        active = str(request_data["active"]).upper()

        # check if active is boolean and return Bad request if not
        if active not in ["TRUE", "FALSE"]:
            message = {
                "ERROR": f"{request_data['active']} is not a valid option, it should be true or false!"
            }
            return make_response(message, 400)

        # get all data from Feature flags sheet
        all_feature_flags_data = google_sheets_client.get_single_sheet_as_dict(
            spreadsheet_id=spreadsheet_id,
            sheet_name=sheet_name,
        )

        # check if provided feature exists in the sheet and change its status
        feature_exists = False
        for _feature in all_feature_flags_data:
            if _feature["Feature"] == feature:
                feature_exists = True
                _feature["Active"] = active

        # if feature does not exist return Bad request
        if not feature_exists:
            message = {f"ERROR": f"{feature} does not exist!"}
            return make_response(message, 400)

        # new data to be written in the Feature flags sheet
        feature_flags_list = [list(flag.values()) for flag in all_feature_flags_data]

        value_range_body = {
            "majorDimension": "ROWS",
            "values": feature_flags_list,
        }

        # update Feature flags data using Google Sheets API
        google_sheets_client.sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A2:G100",
            valueInputOption="USER_ENTERED",
            body=value_range_body,
        ).execute()

        return jsonify(all_feature_flags_data)


if __name__ == "__main__":
    app.run()
