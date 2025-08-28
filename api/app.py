#!/usr/bin/env python3
"""
Apex MVP - RAG Platform API
A scalable RAG (Retrieval-Augmented Generation) platform with multi-tenant architecture.
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_CONNECTION')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class Embedding(db.Model):
    __tablename__ = 'embeddings'
    __table_args__ = {'schema': 'rag_memory'}
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(255), nullable=False, index=True)
    project_id = db.Column(db.String(255), nullable=False, index=True)
    embedding = db.Column(db.JSON, nullable=False)
    content = db.Column(db.Text, nullable=False)
    metadata = db.Column(db.JSON)
    source = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class FeedbackEntry(db.Model):
    __tablename__ = 'entries'
    __table_args__ = {'schema': 'rag_feedback'}
    
    id = db.Column(db.String(36), primary_key=True)
    tenant_id = db.Column(db.String(255), nullable=False, index=True)
    user_id = db.Column(db.String(255), nullable=False, index=True)
    document_id = db.Column(db.String(36), db.ForeignKey('rag_memory.embeddings.id'), index=True)
    feedback = db.Column(db.JSON, nullable=False)
    signal = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

# Helper function to get tenant ID from headers
def get_tenant_id():
    """Extract tenant ID from X-Tenant-ID header"""
    tenant_id = request.headers.get('X-Tenant-ID')
    if tenant_id:
        logger.info(f"Request from tenant: {tenant_id}")
    else:
        logger.warning("No X-Tenant-ID header provided")
    return tenant_id

# Routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connecting',
            'message': 'Database connection in progress'
        }), 200

@app.route('/memory', methods=['GET'])
def get_memory():
    """Get RAG memory entries"""
    tenant_id = get_tenant_id()
    
    try:
        # For now, just return a stub response
        # In production, this would query the database
        return jsonify({
            'status': 'success',
            'message': 'Memory endpoint - GET (stub)',
            'tenant_id': tenant_id,
            'data': []
        }), 200
    except Exception as e:
        logger.error(f"Error in get_memory: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@app.route('/memory', methods=['POST'])
def create_memory():
    """Create new RAG memory entry"""
    tenant_id = get_tenant_id()
    
    try:
        # For now, just return a stub response
        # In production, this would save to the database
        data = request.get_json() or {}
        
        return jsonify({
            'status': 'success',
            'message': 'Memory endpoint - POST (stub)',
            'tenant_id': tenant_id,
            'data': data
        }), 201
    except Exception as e:
        logger.error(f"Error in create_memory: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@app.route('/feedback', methods=['GET'])
def get_feedback():
    """Get feedback entries"""
    tenant_id = get_tenant_id()
    
    try:
        # For now, just return a stub response
        # In production, this would query the database
        return jsonify({
            'status': 'success',
            'message': 'Feedback endpoint - GET (stub)',
            'tenant_id': tenant_id,
            'data': []
        }), 200
    except Exception as e:
        logger.error(f"Error in get_feedback: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def create_feedback():
    """Create new feedback entry"""
    tenant_id = get_tenant_id()
    
    try:
        # For now, just return a stub response
        # In production, this would save to the database
        data = request.get_json() or {}
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback endpoint - POST (stub)',
            'tenant_id': tenant_id,
            'data': data
        }), 201
    except Exception as e:
        logger.error(f"Error in create_feedback: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': str(e)
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Apex MVP API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'memory': '/memory',
            'feedback': '/feedback'
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Get port from environment or default to 8080
    port = int(os.environ.get('PORT', 8080))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
