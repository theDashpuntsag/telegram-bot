activate:
	python3 -m venv venv
	source venv/bin/activate

install:
	pip install -r requirements.txt

run: 
	python3 src/main.py

test:
	pytest tests --disable-warnings -q --tb=short

lint:
	flake8 src/