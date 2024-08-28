#!/usr/bin/env python3

import re
import json
import sys
import os
from typing import Any, Union


def parse_markdown_to_json(md: str) -> dict[str, Any]:
    data = {}
    current_section = None
    current_subsection = None
    for line in md.splitlines():
        line = line.strip()
        if line.startswith('# '):
            current_section = slugify(line[2:])
            data[current_section] = {}
        elif line.startswith('## '):
            current_subsection = slugify(line[3:])
            data[current_section][current_subsection] = {}
        elif ':' in line:
            key, value = parse_key_value(line)
            if key == 'outcomes':
                data[current_section][current_subsection]['table'] = {'outcomes': {}}
            elif current_subsection and key.isdigit() or '-' in key:
                data[current_section][current_subsection]['table']['outcomes'][key] = value
            elif current_subsection:
                data[current_section][current_subsection][key] = value
            else:
                data[current_section][key] = value
    return data


def slugify(text: str) -> str:
    return re.sub(r'\W+', '_', text.lower()).strip('_')


def parse_key_value(line: str) -> Union[dict[str, Any], tuple[str, str]]:
    key, value = map(str.strip, line.split(':', 1))
    if key in ['attacks', 'meta_tags']:
        value = [v.strip() for v in value.split(',')]
    return key, value


def lf_print(s: str) -> None:
  with open(1, "wb") as o:
    o.write(bytes(s, encoding='utf-8'))

def process_input(md_input: str) -> None:
    json_output = parse_markdown_to_json(md_input)
    lf_print(json.dumps(json_output, indent=2))


def main() -> None:
    if len(sys.argv) > 1:
        for filepath in sys.argv[1:]:
            with open(filepath, 'r', encoding='utf-8') as file:
                md_input = file.read()
                process_input(md_input)
    elif not sys.stdin.isatty():
        md_input = sys.stdin.read()
        process_input(md_input)
    else:
        print("Usage: python markus-downus.py [file1.md file2.md ...] or cat file.md | python script.py", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

