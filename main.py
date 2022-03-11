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


@app.route("/api/config/feature_flags", methods=["POST"])
def feature_flags_activate() -> Response:

    feature = request.args.get("feature")
    switch = request.args.get("switch")

    # treba dodati jos provera za parametere, nisam video da postoji elegantno inbuilt resenje kao sa serializerima u djangu
    if switch not in ["TRUE", "FALSE"]:
        message = {"ERROR": f"{switch} is not valid option, it should be TRUE or FALSE"}
        return make_response(message, 400)

    google_sheets_client = GoogleSheetsClient(
        creds=settings.GOOGLE_SHEETS_SERVICE_ACC_CREDENTIALS,
        scope=settings.GOOGLE_SHEETS_SCOPE,
    )

    all_feature_flags_data = google_sheets_client.get_single_sheet_as_dict(
        "1EJzkRzyE-zPY_wffu2D8iECwWsWh2wTIc8cXc56PfQE", "Feature flags"
    )

    for _feature in all_feature_flags_data:
        if _feature["Feature"] == feature:
            _feature["Active"] = switch

    feature_flags_list = []
    for flag in all_feature_flags_data:
        feature_flags_list.append(list(flag.values()))

    value_range_body = {
        "majorDimension": "ROWS",
        "values": feature_flags_list,
    }

    google_sheets_client.sheet.values().update(
        spreadsheetId="1EJzkRzyE-zPY_wffu2D8iECwWsWh2wTIc8cXc56PfQE",
        range="Feature flags!A2:G100",
        valueInputOption="USER_ENTERED",
        body=value_range_body,
    ).execute()

    return jsonify(all_feature_flags_data)


if __name__ == "__main__":
    app.run()
