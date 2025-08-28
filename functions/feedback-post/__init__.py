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

def create_feedback_table(conn):
    """Create feedback table if it doesn't exist"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rag_feedback (
                id VARCHAR(36) PRIMARY KEY,
                tenant_id VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                response_id VARCHAR(255) NOT NULL,
                feedback TEXT NOT NULL,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            )
        """)
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Table creation error: {e}")

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Create new feedback entry and save to PostgreSQL"""
    try:
        # Get tenant ID from headers
        tenant_id = req.headers.get('X-Tenant-ID', 'default')
        
        # Get request body
        req_body = req.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'feedback', 'rating', 'response_id']
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
        
        # Validate rating
        rating = req_body['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return func.HttpResponse(
                json.dumps({
                    'status': 'error',
                    'message': 'Rating must be an integer between 1 and 5'
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Generate unique ID
        feedback_id = str(uuid.uuid4())
        
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
        create_feedback_table(conn)
        
        # Insert data into database
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rag_feedback (id, tenant_id, user_id, response_id, feedback, rating, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            feedback_id,
            tenant_id,
            req_body['user_id'],
            req_body['response_id'],
            req_body['feedback'],
            rating,
            datetime.utcnow()
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Return success response
        response_data = {
            'id': feedback_id,
            'tenant_id': tenant_id,
            'user_id': req_body['user_id'],
            'response_id': req_body['response_id'],
            'feedback': req_body['feedback'],
            'rating': rating,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'saved_to_database'
        }
        
        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'message': 'Feedback entry created and saved to database',
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
