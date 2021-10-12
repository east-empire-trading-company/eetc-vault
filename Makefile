reformat_code:
	black .

install_python_requirements:
	pip install pip-tools
	pip install -r requirements.txt

update_python_requirements:
	pip install pip-tools
	pip-compile --upgrade

update_and_install_python_requirements: update_python_requirements install_python_requirements

build_and_deploy_docker_image:
	gcloud config set run/region us-east1
	gcloud config set project eetc-vault
	gcloud builds submit --tag gcr.io/eetc-vault/eetc-vault-service

deploy: build_and_deploy_docker_image
	gcloud beta run services replace service.yaml --platform managed
	gcloud beta run deploy eetc-vault-service --platform managed --port 8080 --image gcr.io/eetc-vault/eetc-vault-service --allow-unauthenticated
