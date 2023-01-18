lint:
	black  --check  main.py 
	flake8 main.py

format:
	black main.py

install_dependencies:
	pip install -r requirements.txt -r requirements_dev.txt