import azure.functions as func
import os
import json

from dotenv import load_dotenv
from requests import get

load_dotenv()

engine_url = os.getenv("ENGINE_URL")
code = os.getenv("ENGINE_API_KEY")


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        # Bot Framework messages usually come in with this structure
        user_input = req_body.get("text")

        if user_input and "hi" in user_input.lower():
            response = get(f"{engine_url}?code={code}")
            engine_response = response.json()

            return func.HttpResponse(
                json.dumps({
                    "type": "message",
                    "text": json.dumps(engine_response, indent=2)
                }),
                mimetype="application/json",
                status_code=200
            )

        return func.HttpResponse(
            json.dumps({
                "type": "message",
                "text": "Say 'hi' to get data from ENGINE."
            }),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                "type": "message",
                "text": f"Oops! Something went wrong: {str(e)}"
            }),
            mimetype="application/json",
            status_code=500
        )
