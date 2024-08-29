python markus-downus.py test-input.md >test-result.json
wsl sdiff --ignore-all-space test-expected.json test-result.json
python -c "import json; print('Jsons match.') if ( json.load(open('test-expected.json')) == json.load(open('test-result.json')) ) else print('Jsons do NOT match.')"
mypy --strict markus-downus.py --enable-incomplete-feature=NewGenericSyntax --pretty
pyright markus-downus.py
