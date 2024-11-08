import logging
import json
import random
import azure.functions as func
from pathlib import Path
from shared.optima import optima_encode

home_html = Path('create/home-template.html').read_bytes()
generated_html_string = Path('create/generated-template.html').read_text()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')   

    # Give base page letting you create a new event on /create
    if len(req.params) < 2:
        return func.HttpResponse(home_html, mimetype="text/html")

    seed = req.params['seed']
    names = req.params['names'].split(',')

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
        urls[me] = req.url.split("?")[0].replace('/create', f'/{encoded_arg}')

    data = json.dumps(urls)
    return func.HttpResponse(
        generated_html_string.replace('%LINKDATA%', data).encode("utf-8"), mimetype="text/html"
    )
