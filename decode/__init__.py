import logging
from flask import request
from pathlib import Path
from shared.optima import optima_decode

name_template_string = Path('decode/name-template.html').read_text()

def main(encoded: str) -> str:
    logging.info('Python HTTP trigger function processed a request.')   

    encoded, seed = optima_decode(encoded)
    target, you = encoded[0], encoded[1]
    name_html = name_template_string.replace("%YOU%", you[0].upper() + you[1:])
    name_html = name_html.replace("%TARGET%", target[0].upper() + target[1:])
    name_html = name_html.replace("%EVENT%", seed[0].upper() + seed[1:])
    return  name_html.encode('utf-8')