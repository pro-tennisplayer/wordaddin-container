import azure.functions as func
import json
from datetime import datetime
import os
import urllib.parse

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Test dependencies and database connectivity"""
    results = {
        'status': 'testing',
        'timestamp': datetime.utcnow().isoformat(),
        'python_version': '3.13.5',  # Simplified version check
        'imports': {}
    }
    
    # Test pg8000 import
    try:
        import pg8000
        results['imports']['pg8000'] = 'SUCCESS'
    except Exception as e:
        results['imports']['pg8000'] = f'FAILED: {str(e)}'
    
    # Test uuid import
    try:
        import uuid
        results['imports']['uuid'] = 'SUCCESS'
    except Exception as e:
        results['imports']['uuid'] = f'FAILED: {str(e)}'
    
    # Test datetime import
    try:
        from datetime import datetime
        results['imports']['datetime'] = 'SUCCESS'
    except Exception as e:
        results['imports']['datetime'] = f'FAILED: {str(e)}'
    
    # Test database connection
    try:
        # Get connection string from environment
        conn_str = os.environ.get('POSTGRES_CONNECTION')
        if conn_str:
            # Parse connection string to get individual components
            # Format: postgresql://username:password@host:port/database
            parsed = urllib.parse.urlparse(conn_str)
            
            # Test connection with pg8000
            import pg8000
            conn = pg8000.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:] if parsed.path else 'postgres'
            )
            conn.close()
            results['imports']['database_connection'] = 'SUCCESS'
        else:
            results['imports']['database_connection'] = 'FAILED: No connection string found'
    except Exception as e:
        results['imports']['database_connection'] = f'FAILED: {str(e)}'
    
    return func.HttpResponse(
        json.dumps(results, indent=2),
        status_code=200,
        mimetype="application/json"
    )
