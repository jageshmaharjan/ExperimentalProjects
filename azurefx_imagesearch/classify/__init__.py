import logging

import azure.functions as func
import json
from . import image_search

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    image_path = req.params.get('img')
    results = image_search.image_search(imagepath=image_path)

    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    if results:
        return func.HttpResponse(json.dumps(results), headers = headers)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
