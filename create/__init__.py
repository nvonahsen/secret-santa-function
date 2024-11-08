import logging
import json
import random
from flask import request
from pathlib import Path
from shared.optima import optima_encode

home_html = Path('create/home-template.html').read_bytes()
generated_html_string = Path('create/generated-template.html').read_text()

def main() -> str:
    logging.info('Python HTTP trigger function processed a request.')   

    # Give base page letting you create a new event on /create
    if len(request.args) < 2:
        return home_html

    seed = request.args['seed']
    names = request.args['names'].split(',')

    assert len(list(set(names))) == len(names), "Duplicate names!!!"

    # Generate event links
    random.seed(seed)
    assigned = dict()
    name_set = set(names)
    for n in names:
        # available names without assigned and my own
        available_names = name_set.difference(set([n]))
        available_names = available_names.difference(set(assigned.values()))
        selected = random.sample(available_names, 1)
        assigned[n] = selected[0]

    urls = dict()
    for me, target in assigned.items():
        encoded_arg = optima_encode([target, me], seed)
        urls[me] = request.full_path.split("?")[0].replace('/create', f'/{encoded_arg}')

    data = json.dumps(urls)
    return generated_html_string.replace('%LINKDATA%', data).encode("utf-8")
