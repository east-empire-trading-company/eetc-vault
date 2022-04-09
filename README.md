# EETC Vault
Service that acts as a simple interface for interacting with data stored in
Google Sheets.
## System requirements
To run the project locally and work on it, you need the following:
- Python 3.8+
- Docker
- docker-compose
- make

## Project setup
```commandline
sudo apt-get install build-essential
make update_and_install_python_requirements
```

## Adding a new Python package
1. Add the package name to `requirements.in`
2. Run:
```commandline
make update_and_install_python_requirements
```

## Adding a new environment variable/secret
1. Create a new secret in `Secret Manager`
2. Create a new environment variable in `local_settings.py` under the same name
3.Add it to `service.yaml`, use existing ones as example.

## Use Google Cloud Platform Service account credentials
1. Download the JSON file from Google Cloud Platform
TODO screenshot(s)
2. Run this Python code:
```python
import base64
import json

creds = {  # copy the contents of the JSON file here
  "type": "service_account",
  "project_id": "eetc-data-hub",
  "private_key_id": "dummy",
  "private_key": "dummy",
  "client_email": "google-cloud-storage@eetc-data-hub.iam.gserviceaccount.com",
  "client_id": "dummy",
  "auth_uri": "dummy",
  "token_uri": "dummy",
  "auth_provider_x509_cert_url": "dummy",
  "client_x509_cert_url": "dummy"
}
encrypted_creds = base64.b64encode(json.dumps(creds).encode())
print(encrypted_creds)
```
3. Create a new secret in `Secret Manager` and use the output of the script above as the value
4. Create a new environment variable in `local_settings.py` with the same name and value
5. In `settings.py` make sure the env var is read properly:
```python
import base64
import json
from google.oauth2 import service_account


# to load it and decrypt it
SERVICE_ACC_CREDENTIALS = service_account.Credentials.from_service_account_info(
    json.loads(
        base64.b64decode("SERVICE_ACC_CREDENTIALS"),
    ),
)
```
# Deployment
```commandline
make deploy
```