python markus-downus.py example.md >result.txt
wsl sdiff --ignore-all-space test.json result.txt
mypy --strict markus-downus.py --enable-incomplete-feature=NewGenericSyntax --pretty
