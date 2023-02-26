cd tests/
python test_userroutue.py
cd ..
pytest -v
pytest --cov="."
pytest -v --cov="."
pytest -v --cov="." --cov-report html
