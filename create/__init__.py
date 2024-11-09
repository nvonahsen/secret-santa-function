import logging
import json
import random
from flask import request
from pathlib import Path
from shared.optima import optima_encode, optima_code

home_html = Path('create/home-template.html').read_bytes()
generated_html_string = Path('create/generated-template.html').read_text()

def main() -> str:
    logging.info('Python HTTP trigger function processed a request.')   

    # Give base page letting you create a new event on /create
    if len(request.args) < 2:
        return home_html

    seed = request.args['seed']
    padding = int(request.args['padding'])
    names = request.args['names'].split(',')

    assert len(list(set(names))) == len(names), "Duplicate names!!!"

    # Generate event links
    random.seed(seed)
    assigned = dict()

    # Randomise list until no-one is assigned their own name
    random_names = [name for name in names]
    while True:
        random.shuffle(random_names)
        assigned = dict(zip(names, random_names))
        if all([a != b for a, b in assigned.items()]):
            break

    urls = dict()
    max_len = max([len(name) for name in names])
    for me, target in assigned.items():
        encoded_arg = optima_encode([target, me, generate_padding(target, max_len, padding)], seed)
        urls[me] = f"{request.root_url}{encoded_arg}"

    data = json.dumps(urls)
    return generated_html_string.replace('%LINKDATA%', data).encode("utf-8")


def generate_padding(target, max_len, max_padding):
    # The average padding length for a target name is the difference between it and the longest name
    # This favours longer padding on shorter names
    avg_padding = max_len - len(target)
    
    # Generate a random number of padding characters centered around the average padding
    num_padding_chars = round(random.gauss(avg_padding, max_padding))  # Gaussian distribution
    num_padding_chars = max(0, min(num_padding_chars, max_padding))  # Ensure within range [0, max_padding]

    # Generate the padding characters
    padding = ''.join(random.choices(optima_code, k=num_padding_chars))

    return padding