import azure.functions as func
import json
import psycopg2
from datetime import datetime

def get_db_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(
            host="apex-psql-toebb934.postgres.database.azure.com",
            database="apexdb",
            user="psqladmin",
            password="ApexSecurePass123!",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get memory entries from PostgreSQL database"""
    try:
        # Get tenant ID from headers
        tenant_id = req.headers.get('X-Tenant-ID', 'default')
        
        # Get optional query parameters
        user_id = req.params.get('user_id')
        session_id = req.params.get('session_id')
        limit = req.params.get('limit', '100')
        
        # Connect to database
        conn = get_db_connection()
        if not conn:
            return func.HttpResponse(
                json.dumps({
                    'status': 'error',
                    'message': 'Database connection failed'
                }),
                status_code=500,
                mimetype="application/json"
            )
        
        # Build query based on parameters
        query = """
            SELECT id, tenant_id, user_id, session_id, content, message_type, created_at, metadata
            FROM chat_memory 
            WHERE tenant_id = %s
        """
        params = [tenant_id]
        
        if user_id:
            query += " AND user_id = %s"
            params.append(user_id)
            
        if session_id:
            query += " AND session_id = %s"
            params.append(session_id)
            
        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(int(limit))
        
        # Execute query
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        # Fetch results
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert to list of dictionaries
        memory_data = []
        for row in rows:
            memory_data.append({
                'id': row[0],
                'tenant_id': row[1],
                'user_id': row[2],
                'session_id': row[3],
                'content': row[4],
                'message_type': row[5],
                'created_at': row[6].isoformat() if row[6] else None,
                'metadata': row[7] if row[7] else {}
            })
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'message': 'Memory entries retrieved from database',
                'tenant_id': tenant_id,
                'count': len(memory_data),
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
