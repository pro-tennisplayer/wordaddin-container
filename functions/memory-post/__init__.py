import azure.functions as func
import json
import psycopg2
import uuid
from datetime import datetime
import os

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

def create_memory_table(conn):
    """Create memory table if it doesn't exist"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_memory (
                id VARCHAR(36) PRIMARY KEY,
                tenant_id VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                session_id VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                message_type VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            )
        """)
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Table creation error: {e}")

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Create new memory entry and save to PostgreSQL"""
    try:
        # Get tenant ID from headers
        tenant_id = req.headers.get('X-Tenant-ID', 'default')
        
        # Get request body
        req_body = req.get_json()
        
        # Validate required fields
        required_fields = ['content', 'user_id', 'session_id', 'message_type']
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
        
        # Generate unique ID
        memory_id = str(uuid.uuid4())
        
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
        
        # Create table if it doesn't exist
        create_memory_table(conn)
        
        # Insert data into database
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_memory (id, tenant_id, user_id, session_id, content, message_type, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            memory_id,
            tenant_id,
            req_body['user_id'],
            req_body['session_id'],
            req_body['content'],
            req_body['message_type'],
            datetime.utcnow()
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Return success response
        response_data = {
            'id': memory_id,
            'tenant_id': tenant_id,
            'user_id': req_body['user_id'],
            'session_id': req_body['session_id'],
            'content': req_body['content'],
            'message_type': req_body['message_type'],
            'created_at': datetime.utcnow().isoformat(),
            'status': 'saved_to_database'
        }
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'message': 'Memory entry created and saved to database',
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
