import azure.functions as func
import json
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    try:
        return func.HttpResponse(
            json.dumps({
                'status': 'ok',
                'timestamp': datetime.utcnow().isoformat(),
                'message': 'Apex APIs are running!'
            }),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                'status': 'error',
                'timestamp': datetime.utcnow().isoformat(),
                'message': str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
