import logging
import azure.functions as func
from pathlib import Path
from shared.optima import optima_decode

name_template_string = Path('decode/name-template.html').read_text()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')   

    encoded = req.route_params['encoded']

    (target, you), seed = optima_decode(encoded)
    name_html = name_template_string.replace("%YOU%", you[0].upper() + you[1:])
    name_html = name_html.replace("%TARGET%", target[0].upper() + target[1:])
    name_html = name_html.replace("%EVENT%", seed[0].upper() + seed[1:])
    return func.HttpResponse(
        name_html.encode('utf-8'), mimetype="text/html"
    )