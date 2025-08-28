import azure.functions as func
import json
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get memory entries"""
    try:
        # Get tenant ID from headers
        tenant_id = req.headers.get('X-Tenant-ID', 'default')
        
        # Mock data for now
        memory_data = [
            {
                'id': '1',
                'tenant_id': tenant_id,
                'content': 'Sample memory content',
                'created_at': datetime.utcnow().isoformat()
            }
        ]
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'message': 'Memory endpoint - GET',
                'tenant_id': tenant_id,
                'data': memory_data
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
