import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Simple test function with minimal code"""
    try:
        result = {
            'status': 'simple_test_success',
            'message': 'Basic Azure Functions are working',
            'test_data': {
                'string': 'test',
                'number': 42,
                'boolean': True
            }
        }
        
        return func.HttpResponse(
            json.dumps(result, indent=2),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                'status': 'error',
                'error': str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
