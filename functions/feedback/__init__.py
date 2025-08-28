import azure.functions as func
import json
from datetime import datetime
import os
import urllib.parse

def main(req: func.HttpRequest) -> func.HttpResponse:
    """GET endpoint to retrieve feedback"""
    try:
        # Get query parameters
        tenant_id = req.params.get('tenant_id')
        user_id = req.params.get('user_id')
        response_id = req.params.get('response_id')
        limit = req.params.get('limit', '10')
        
        # For now, return mock data since pg8000 needs more setup
        mock_data = [
            {
                "id": "mock-feedback-1",
                "tenant_id": tenant_id or "default-tenant",
                "user_id": user_id or "default-user",
                "response_id": response_id or "default-response",
                "rating": 5,
                "feedback_text": "This is mock feedback data - pg8000 integration in progress",
                "created_at": datetime.utcnow().isoformat(),
                "metadata": {"source": "mock", "status": "testing"}
            }
        ]
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'data': mock_data,
                'message': 'Mock feedback data returned - pg8000 integration in progress'
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }),
            status_code=500,
            mimetype="application/json"
        )
