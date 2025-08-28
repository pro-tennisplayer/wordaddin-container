import azure.functions as func
import json
from datetime import datetime
import asyncio
import os
import urllib.parse

async def get_db_connection():
    """Get database connection using asyncpg"""
    conn_str = os.environ.get('POSTGRES_CONNECTION')
    if not conn_str:
        raise Exception("Database connection string not found")
    
    parsed = urllib.parse.urlparse(conn_str)
    return await asyncio.wait_for(
        asyncio.create_task(
            asyncio.get_event_loop().create_connection(
                lambda: asyncio.StreamReaderProtocol(asyncio.StreamReader()),
                parsed.hostname,
                parsed.port or 5432
            )
        ),
        timeout=10.0
    )

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """GET endpoint to retrieve chat memory"""
    try:
        # Get query parameters
        tenant_id = req.params.get('tenant_id')
        user_id = req.params.get('user_id')
        session_id = req.params.get('session_id')
        limit = req.params.get('limit', '10')
        
        # For now, return mock data since asyncpg needs more setup
        mock_data = [
            {
                "id": "mock-1",
                "tenant_id": tenant_id or "default-tenant",
                "user_id": user_id or "default-user",
                "session_id": session_id or "default-session",
                "message": "This is mock memory data - asyncpg integration in progress",
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {"source": "mock", "status": "testing"}
            }
        ]
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'data': mock_data,
                'message': 'Mock data returned - asyncpg integration in progress'
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
