#!/usr/bin/env python3

import json
import re
from typing import Dict, List, Union

def parse_markdown(markdown: str) -> Dict[str, Dict[str, Dict]]:
    result: Dict[str, Dict[str, Dict]] = {}
    lines = markdown.strip().split('\n')
    current_level = ""
    current_key = ""

    def parse_key_value(line: str) -> Dict[str, Union[str, List[str]]]:
        key, value = line.split(':', 1)
        key = key.strip().replace(' ', '_').lower()
        value = value.strip()
        if ',' in value:
            value = [v.strip() for v in value.split(',')]
        return {key: value}

    for line in lines:
        if line.startswith('# '):  # First level
            current_level = "first_level"
            result[current_level] = {}
        elif line.startswith('## '):  # Second level
            current_level = "second_level"
            result[current_level] = {}
        elif ':' in line:
            data = parse_key_value(line)
            if current_level == "first_level":
                if 'name' in data:
                    current_key = data['name'].replace(' ', '_').lower()
                    result[current_level][current_key] = data
                else:
                    result[current_level][current_key].update(data)
            elif current_level == "second_level":
                if 'name' in data:
                    current_key = data['name'].replace(' ', '_').lower()
                    result[current_level][current_key] = data
                else:
                    result[current_level][current_key].update(data)
    
    return result

def main():
    markdown = """
    # first level

    name: This is the Name
    effect: the effect
    attacks: this one, this one
    meta_tags: this, that, these

    ## second level

    name: Here We Are
    table: 
    outcomes: 
    1: one
    2: two
    3-6: a whole bunch

    name: Another more normal one
    effect: the effect
    flavor_text: flavor text
    meta_tags: this, that, this
    """
    
    json_data = parse_markdown(markdown)
    print(json.dumps(json_data, indent=2))

if __name__ == "__main__":
    main()
