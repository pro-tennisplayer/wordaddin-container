import azure.functions as func
import json
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get feedback entries"""
    try:
        # Get tenant ID from headers
        tenant_id = req.headers.get('X-Tenant-ID', 'default')
        
        # Mock data for now
        feedback_data = [
            {
                'id': '1',
                'tenant_id': tenant_id,
                'user_id': 'user123',
                'feedback': 'Great response!',
                'created_at': datetime.utcnow().isoformat()
            }
        ]
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'message': 'Feedback endpoint - GET',
                'tenant_id': tenant_id,
                'data': feedback_data
            }),
            status_code=200,
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
