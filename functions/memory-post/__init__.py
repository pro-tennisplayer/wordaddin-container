import azure.functions as func
import json
from datetime import datetime
import os
import urllib.parse

def main(req: func.HttpRequest) -> func.HttpResponse:
    """POST endpoint to save chat memory"""
    try:
        # Parse request body
        req_body = req.get_json()
        
        # Validate required fields
        required_fields = ['tenant_id', 'user_id', 'session_id', 'content']
        for field in required_fields:
            if field not in req_body:
                return func.HttpResponse(
                    json.dumps({
                        'status': 'error',
                        'message': f'Missing required field: {field}'
                    }),
                    status_code=400,
                    mimetype="application/json"
                )
        
        # For now, return success with mock data since pg8000 needs more setup
        mock_response = {
            'status': 'success',
            'message': 'Memory saved successfully (mock) - pg8000 integration in progress',
            'data': {
                'id': 'mock-generated-id',
                'tenant_id': req_body['tenant_id'],
                'user_id': req_body['user_id'],
                'session_id': req_body['session_id'],
                'content': req_body['content'],
                'message_type': req_body.get('message_type', 'chat'),
                'created_at': datetime.utcnow().isoformat(),
                'metadata': req_body.get('metadata', {})
            }
        }
        
        return func.HttpResponse(
            json.dumps(mock_response),
            status_code=201,
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
