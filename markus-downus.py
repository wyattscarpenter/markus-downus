#!/usr/bin/env python3

import re
import json
import sys

type Slyd = str | list[Slyd] | dict[str, Slyd]

def parse_markdown_to_json(md: str) -> dict[str, Slyd]:
    data = {}
    current_section = None
    current_subsection = None
    current_subsubsection = None
    for line in md.splitlines():
        line = line.strip()
        if line.startswith('name:'):
            current_subsubsection = slugify(line[5:])
            if current_subsection:
                data[current_section][current_subsection][current_subsubsection] = {}
            else:
                data[current_section][current_subsubsection] = {}
        if line.startswith('##'): # note that this has to come first so it doesn't match the one-# rule either
            current_subsection = slugify(line[2:])
            data[current_section][current_subsection] = {}
        elif line.startswith('#'):
            current_section = slugify(line[1:])
            data[current_section] = {}
        elif ':' in line:
            key, value = parse_key_value(line)
            if key == 'outcomes':
                data[current_section][current_subsection][current_subsubsection]['table'] = {'outcomes': {}}
            elif current_subsection and key.isdigit() or '-' in key: #todo: this is almost certainly the wrong approach
                data[current_section][current_subsection][current_subsubsection]['table']['outcomes'][key] = value
            elif current_subsection:
                data[current_section][current_subsection][current_subsubsection][key] = value
            else:
                data[current_section][current_subsubsection][key] = value
    return data


def slugify(text: str) -> str:
    return re.sub(r'\W+', '_', text.lower()).strip('_')


def parse_key_value(line: str) -> tuple[str, str|list[str]]:
    key, value = map(str.strip, line.split(':', 1))
    return key, value if key not in ['attacks', 'meta_tags'] else [v.strip() for v in value.split(',')]


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

