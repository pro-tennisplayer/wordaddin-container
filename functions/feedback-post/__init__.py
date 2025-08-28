import azure.functions as func
import json
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Create new feedback entry"""
    try:
        # Get tenant ID from headers
        tenant_id = req.headers.get('X-Tenant-ID', 'default')
        
        # Get request body
        req_body = req.get_json()
        
        # Mock response - in production this would save to database
        response_data = {
            'id': 'new-feedback-id',
            'tenant_id': tenant_id,
            'user_id': req_body.get('user_id', 'unknown'),
            'feedback': req_body.get('feedback', ''),
            'created_at': datetime.utcnow().isoformat(),
            'received_data': req_body
        }
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'message': 'Feedback entry created',
                'tenant_id': tenant_id,
                'data': response_data
            }),
            status_code=201,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                'status': 'error',
                'message': 'Internal server error',
                'error': str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
