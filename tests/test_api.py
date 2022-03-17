def test_valid_post_request(client):
    # given
    post_data = {
        "spreadsheet_id": "1EJzkRzyE-zPY_wffu2D8iECwWsWh2wTIc8cXc56PfQE",
        "sheet_names": ["API Clients", "Customers"],
    }
    api_endpoint = "/api/config/fetch_from_google_sheets"

    # when
    rv = client.post(api_endpoint, json=post_data)

    # then
    assert rv.status_code == 200


def test_get_request_method_not_allowed(client):
    # given
    api_endpoint = "/api/config/fetch_from_google_sheets"

    # when
    rv = client.get(api_endpoint)

    # then
    assert rv.status_code == 405


def test_valid_post_request_feature_flags(client):
    # given
    post_data = {"feature": "test_feature", "active": "true"}
    api_endpoint = "/api/config/feature_flags"

    # when
    rv = client.post(api_endpoint, json=post_data)

    # then
    assert rv.status_code == 200


def test_bad_request_feature_flags(client):
    # given
    post_data = {"feature": "123", "active": "true"}
    api_endpoint = "/api/config/feature_flags"

    # when
    rv = client.post(api_endpoint, json=post_data)

    # then
    assert rv.status_code == 400, {"ERROR": "123 does not exist!"}


def test_get_request_method_not_allowed_feature_flags(client):
    # given
    api_endpoint = "/api/config/feature_flags"

    # when
    rv = client.get(api_endpoint)

    # then
    assert rv.status_code == 405
